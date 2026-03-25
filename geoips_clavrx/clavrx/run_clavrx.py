# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Run clavrx processing on given input files.

Sensors available for processing:
- ABI L1B netcdf
- AHI HSD
- MODIS
- VIIRS
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

# geoips libs
from geoips.filenames.base_paths import PATHS as gpaths

# datetime string with inst: re_datetime pattern, datetime parse
dt_pattern = {
    "ABI": (r"e\d{13}", "%Y%j%H%M%S"),
    "AHI": (r"_\d{8}", "%Y%m%d"),
    "MODIS": (r"A\d{7}", "%Y%j"),
    "VIIRS": (r"d\d{8}", "%Y%m%d"),
}

# possibles instrument search patterns
inst_mapping = {
    "ABI": "ABI",
    "HS": "AHI",
    "MOD": "MODIS",
    "MYD": "MODIS",
    "NPP": "VIIRS",
    "J02": "VIIRS",
    "J01": "VIIRS",
}

fmap = {"ABI": "C01_", "AHI": "HS_", "MODIS": "KM", "VIIRS": "GMTCO"}


def get_inst(filelist):
    """Get instrument and datetime from filelist."""
    inst_types = []
    for f in filelist:
        basefile = os.path.basename(f)
        # iterate through all possible patterns
        for s in inst_mapping.keys():
            res = re.search(s, basefile.upper())
            if res is not None:
                inst_types.append(inst_mapping[s])

    inst_avail = list(set(inst_types))
    if len(inst_avail) > 1:
        print("More than one instrument detected")
        raise ValueError("Multi-instrument detected {}".format(inst_avail))
    inst_avail = inst_avail[0]
    fsort = sorted(list(map(os.path.basename, filelist)))
    first_file = fsort[0]
    datetime_start = re.search(dt_pattern[inst_avail][0], first_file)
    if datetime_start is None:
        raise ValueError("No datetime string found")
    datetime_res = datetime.strptime(
        datetime_start.group(0)[1:], dt_pattern[inst_avail][1]
    ).strftime("%Y%m%d")

    return inst_avail, datetime_res


def proc_wrap(
    filelist,
    inst,
    clavrx_exec,
    runtime_directory,
    level2_list,
    template_options_file,
    ancillary_data_directory,
    outdir,
):
    """Run clavrx processing for the instrument.

    Assumes options file and dynamic data are setup.
    """
    # Create runtime_directory if it doesn't exist.
    if not os.path.isdir(runtime_directory):
        os.makedirs(runtime_directory, exist_ok=True)
    if not os.path.exists(clavrx_exec):
        raise FileNotFoundError(f"Cannot find clavrx executable: {args.clavrx_exec}")
    if not os.path.exists(level2_list):
        raise FileNotFoundError(f"Cannot find level2_list: {level2_list}")
    if not os.path.exists(template_options_file):
        raise FileNotFoundError(
            f"Cannot find template_options_file: {template_options_file}"
        )
    if not os.path.isdir(ancillary_data_directory):
        raise FileNotFoundError(
            f"Cannot find ancillary_data_directory: {ancillary_data_directory}"
        )
    # setup input filelist
    flist = os.path.join(runtime_directory, "file_list")
    # setup output dir
    # Ensure we have a trailing '/' at the end of the outdir path
    # Otherwise CLAVR-X will treat the final subdir as part of the file name.
    outdir += "/"
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    # get input dir
    indir = set(map(os.path.dirname, filelist))
    if len(list(indir)) > 1:
        raise NameError(
            "Multi-dir processing not supported, input dirs are {}".format(indir)
        )
    indir = list(indir)[0] + "/"

    # get specific input file
    fsort = sorted(list(map(os.path.basename, filelist)))
    infile = [i for i in fsort if fmap[inst] in i]
    if len(infile) == 0:
        raise ValueError(
            f"No proper input file found, searched for {fmap[inst]} in filelist {fsort}"
        )
    # input file lists are specific for each inst
    infile = infile[0]
    # combined to output list
    filelist_lines = [indir + "\n", outdir + "\n", infile + "\n"]
    print(
        "\n**Writing file_list to runtime_directory\n"
        f"        file_list to {runtime_directory}"
    )
    with open(flist, "w") as f:
        f.writelines(filelist_lines)

    # setup options file
    # This is the required location for the clavrx_options file that is used by
    # run_clavrxorb.  We are using our passed in template file, which may contain
    # comments (any line preceded by '#'), environment variables, and the specific
    # [run_clavrx_ancillary_data_directory_command_line_argument] line (which will
    # be replaced with the
    # --ancillary_data_directory command line argument).  Comments
    # will be stripped, environment variables expanded, and --ancillary_data_directory
    # updated prior to writing the template options file to this mandatory
    # --runtime_directory location.
    ofile = os.path.join(runtime_directory, "clavrx_options")
    if not os.path.exists(template_options_file):
        print(
            f"Template options file not found: {template_options_file} "
            "Please pass in valid template_options_file."
        )
        raise FileNotFoundError("CLAVR-x template options file doesn't exist")

    with open(template_options_file, "r") as template_fobj:
        olines = template_fobj.readlines()
    # Remove commented lines, and expand environment variables
    olines = [os.path.expandvars(line) for line in olines if line[0] != "#"]
    # Replace ancillary data directory and empty lines. Make sure ancillary data
    # directory has a trailing /!
    olines = [
        line.replace(
            "[run_clavrx_ancillary_data_directory_command_line_argument]",
            ancillary_data_directory + "/",
        )
        for line in olines
        if line.strip() != ""
    ]
    print(
        "\n**Writing template to final clavrx_options in runtime_directory\n"
        f"        {template_options_file} {ofile}"
    )
    # Write out the final clavrx_options file, to the clavrx runtime directory.
    # CLAVR-x requires clavrx_options to exist in the same directory it runs from.
    with open(ofile, "w") as final_fobj:
        final_fobj.writelines(olines)

    print(
        "\n**Copying level2_list to runtime_directory\n"
        f"        {level2_list} to {runtime_directory}"
    )
    shutil.copy(level2_list, runtime_directory)
    # run processing. run_clavrxorb requires running from the directory it lives in.
    os.chdir(runtime_directory)
    print(
        "\n**Running clavrx executable from runtime_directory\n"
        f"        {clavrx_exec}\n"
        "runtime_directory contents:\n"
    )
    print(os.listdir(runtime_directory))
    retval = 0
    with Popen([clavrx_exec], stdout=PIPE, stderr=STDOUT) as proc:
        for sr in iter(proc.stdout.readline, b""):
            logline = sr.decode("utf-8").rstrip()
            print(logline)
            if "STOP" in logline:
                print("Found STOP in log line, probably failed")
                retval = 1

    sys.exit(retval)


if __name__ == "__main__":
    """Setup processing wrapper."""
    parser = argparse.ArgumentParser(
        description="""The GeoIPS run_clavrx.py wrapper for driving the
          University of Wisconsin Cooperative Institude for Meteorological Satellite
          Studies (CIMSS) Clouds for AVHRR Extended (CLAVR-x) pre-processing.

          Please see run_clavrx.py options below for more information on the
          details of running CLAVR-x.

          The output of this CLAVR-x pre-processing can be post-processed through the
          Geolocated Information Processing System (GeoIPS) to produce additional
          products and outputs.
          """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--input_files",
        action="extend",
        nargs="+",
        required=True,
        help="""List of full paths to all input files. These are used to populate the
        mandatory clavrx file_list, which is used when calling clavrx_exec.""",
    )
    parser.add_argument(
        "--runtime_directory",
        required=False,
        default=os.path.join(gpaths["GEOIPS_OUTDIRS"], "scratch", "clavrx_run"),
        help="""CLAVR-x runtime directory.  This is a temporary directory that will
          contain all the CLAVR-x configuration files as well as the pre-built
          run_clavrxorb executable.  CLAVR-x requires all configuration files to
          exist in the same directory as the executable, so we copy all required
          files, including the run_clavrxorb executable, into this --runtime_directory.
          The following files must all exist, and must be named as specified below:

          * 'run_clavrxorb' Copied in place from:

            * --clavrx_exec
          * 'clavrx_options' Auto-generated using:

            * --template_options_file
            * --ancillary_data_directory
            * Environment variables as needed.
          * 'file_list'  Auto-generated using:

            * --input_files
            * --output_directory
          * 'level2_list' manually generated, copied in place from:

            * --level2_list""",
    )
    parser.add_argument(
        "--level2_list",
        required=False,
        default=os.path.join(
            gpaths["GEOIPS_PACKAGES_DIR"], "geoips_clavrx", "clavrx", "level2_list"
        ),
        help="""List of level 2 products specifying what outputs clavrx should produce.
          This should be a fully valid clavrx level 2 list - run_clavrx.py will
          copy this file into the --runtime_directory as 'level2_list'. The clavrx
          executable expects 'level2_list' in the same directory as the executable""",
    )
    parser.add_argument(
        "--template_options_file",
        type=str,
        required=False,
        default=os.path.join(
            gpaths["GEOIPS_PACKAGES_DIR"],
            "geoips_clavrx",
            "clavrx",
            "clavrx_options_template",
        ),
        help="""Template CLAVR-x options file that allows optional references to
          environment variables, commented lines preceded by '#', and
          optional [run_clavrx_ancillary_data_directory_command_line_argument]
          line that will be replaced with the
          --ancillary_data_directory argument.

          run_clavrx.py will:

          * remove commented lines
          * remove empty lines
          * expand environment variables
          * replace '[run_clavrx_ancillary_data_directory_command_line_argument]'
            with --ancillary_data_directory argument

          prior to writing to the run_clavrxorb --runtime_directory (run_clavrxorb
          requires the clavrx_options  file to be in the same directory as the
          executable). Otherwise this is a completely valid clavrx_options file.

          Note ancillary_data_directory must match the data path specified when
          calling update_ancildata_dynamic and get_ancildata_static. To facilitate
          ensuring these paths match, we support using the command line
          --ancillary_data_directory argument directly, an explicitly defined full
          path in the clavrx_options file, or a full path in the clavrx_options file
          defined using environment variables.""",
    )
    parser.add_argument(
        "--ancillary_data_directory",
        type=str,
        required=False,
        default=os.path.join(gpaths["GEOIPS_ANCILDAT"], "clavrx"),
        help="""Ancillary data directory used by the clavrx executable, as passed into
          * update_ancildata_dynamic.py
          * get_ancildata_static.py
          * run_clavrx.py
          And as included in
          * clavrx_options_template

          The run_clavrxorb executable expects the first line of the clavrx_options
          file to the be full path to the clavrx ancillary data directory.

          run_clavrx.py will replace
          '[run_clavrx_ancillary_data_directory_command_line_argument]' with the
          --ancillary_data_directory command line argument if
          * [run_clavrx_ancillary_data_directory_command_line_argument]
            exists in clavrx_options_template, and
          * --ancillary_data_directory is passed into run_clavrx.py at the command line.

          If [run_clavrx_ancillary_data_directory_command_line_argument]
          does not exist in clavrx_options_template, or
          --ancillary_data_directory is not passed in at the command line, then the
          first non-commented/non-empty line of clavrx_options_template must be a
          valid path to the ancillary data directory (with or without environment
          variables).

          The run_clavrxorb executable also expects the ancillary_data_directory to
          contain both explicitly named 'dynamic' and 'static' subdirectories.
          update_ancildata_dynamic.py and get_ancildata_static.py both ensure the
          correct subdirectory names within ancillary_data_directory.""",
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        required=False,
        default=os.path.join(gpaths["GEOIPS_OUTDIRS"], "preprocessed", "clavrx"),
        help="""Output directory for all run_clavrxorb level 2 outputs.
            All outputs will be written directly to this directory, no
            subdirectories are created prior to writing the outputs.""",
    )
    parser.add_argument(
        "--clavrx_exec",
        type=str,
        required=False,
        default=os.path.join(
            gpaths["GEOIPS_DEPENDENCIES_DIR"], "clavrx", "run_clavrxorb"
        ),
        help="""Pre-built clavrx executable. This file will be copied to the
          --runtime_directory, along with all required clavrx configuration files

          * clavrx_options (template file used to generate final clavrx_options, full
                            path to clavrx_options_template passed into run_clavrx.py)
          * level2_list (manually generated prior to calling run_clavrx.py,
                         full path to level2_list explicitly passed into run_clavrx.py)
          * file_list (auto-generated within run_clavrx.py)""",
    )
    args = parser.parse_args()

    inst, sdt = get_inst(args.input_files)
    # start processing
    proc_wrap(
        args.input_files,
        inst,
        args.clavrx_exec,
        args.runtime_directory,
        level2_list=args.level2_list,
        template_options_file=args.template_options_file,
        ancillary_data_directory=args.ancillary_data_directory,
        outdir=args.output_directory,
    )
