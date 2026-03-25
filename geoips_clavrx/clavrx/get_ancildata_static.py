# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Downloads CLAVR-x static ancillary data."""

import argparse
import shutil
import os
import sys
import subprocess
from geoips.filenames.base_paths import PATHS as gpaths


def fetch_static(ancillary_data_directory, validate_only=False):
    """Fetch CLAVR-x static ancillary data.

    This includes static ancillary datasets required to run CLAVR-x.  This does not
    include any dynamic datasets, there is a separate script for fetching dynamic
    ancillary datasets.
    """
    # This is a clavrx requirement - explicit "dynamic" and "static" subdirectories
    # must both be contained in the ancillary_data_directory.
    static_data_directory = os.path.join(ancillary_data_directory, "static")

    if os.path.isdir(static_data_directory) and validate_only:
        print("SUCCESS Static data directory already available and validate_only True!")
        sys.exit(0)
    elif validate_only:
        print("FAILED static data dir does not exist, and requested validate only")
        print("Please run this script again without the validate_only flag.")
        raise FileNotFoundError(
            "CLAVR-x static data directory does not exist, and validate_only True"
        )

    if os.path.isdir(static_data_directory):
        print("FAILED static data directory exists, and did NOT request validate only")
        print("This script will not update existing static ancillary data")
        print("Remove the static directory and re-run this script to update")
        print(f"# rm -rfv {static_data_directory}")
        print(
            f"Or manually link an existing static data dir to '{static_data_directory}'"
        )
        raise IOError("CLAVR-x static data directory exists, and validate_only False")

    """
    Download static data for CLAVRx
    """
    # download from CSPP (much more reliable)
    static_prompt = str(input("""\nStatic data for CLAVRx utilizes roughly
            410 GiB of space, we highly recommend using a shared clone of the static
            ancillary datasets whenever possible. If you link an existing static data
            directory to '{static_data_directory}, this script will recognize it as
            already existing, and will not attempt to download it again, and pass
            without error.
            Do you want to proceed with local install? (y/n): """))

    if static_prompt == "n":
        print("\nEither link static data or install on system.")
        sys.exit(1)
    elif static_prompt == "y":
        print("Started downloading static data, this may take a while....")

    static_url = "ftp://epscloud.ssec.wisc.edu/clavrx_ancil_data/static"
    print("Downloading static data from {}".format(static_url))
    # GFS data http://tyr.ssec.wisc.edu/gfs/

    subprocess.run(
        ["wget", "-vr", static_url], capture_output=True, cwd=ancillary_data_directory
    )

    # This is where the wget ends up.
    wget_static_path = (
        f"{ancillary_data_directory}/epscloud.ssec.wisc.edu/clavrx_ancil_data/static/"
    )
    # Move the downloaded static directory into the ancillary_data_directory.
    # Note the subdirectory under ancillary_data_directory *must* be 'static'
    shutil.move(wget_static_path, ancillary_data_directory)
    # Clean up the wget folders.
    os.rmdir(
        os.path.join(
            ancillary_data_directory, "epscloud.ssec.wisc.edu", "clavrx_ancil_data"
        )
    )
    os.rmdir(os.path.join(ancillary_data_directory, "epscloud.ssec.wisc.edu"))

    # ??
    subprocess.run(
        [
            "cp",
            f"{static_data_directory}/luts/ecm2/nb_cloud_mask_calipso_prior_new.nc",
            f"{static_data_directory}/luts/ecm2/nb_cloud_mask_calipso_prior.nc",
        ]
    )
    print("Finished downloading static data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""The GeoIPS get_ancildata_static.py wrapper for obtaining the
          static ancillary data required for running the
          University of Wisconsin Cooperative Institude for Meteorological Satellite
          Studies (CIMSS) Clouds for AVHRR Extended (CLAVR-x) pre-processing.

          CLAVR-x expects the static ancillary data to exist specifically in the
          'static' subdirectory of the --ancillary_data_directory, this wrapper
          script ensures the static ancillary data exists in the correct location.

          Note this script will never update an existing static data directory. In
          order to update an existing static data directory, you must manually remove,
          then re-run this script without the validate_only flag.
          """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--ancillary_data_directory",
        type=str,
        required=False,
        default=os.path.join(gpaths["GEOIPS_ANCILDAT"], "clavrx"),
        help="""Full path to the clavrx ancillary datasets.

          Note this --ancillary_data_directory must match:

          * --ancillary_data_directory passed into update_ancildata_dynamic.py
          * --ancillary_data_directory passed into into run_clavrx.py, and
          * first line of the clavrx_options file.
            * CLAVR-x uses the first line of the clavrx_options file
              to determine the full path to the ancillary data directory, and that
              directory must contain both explicitly named 'dynamic' and 'static'
              subdirectories.

          This command line argument should not include the
          'static' subdirectory, but only the base ancillary data directory.

          Note this script will never update an existing static data directory. In
          order to update an existing static data directory, you must manually remove,
          then re-run this script without the validate_only flag.
          """,
    )
    parser.add_argument(
        "--validate_only",
        action="store_true",
        help="""If --validate_only passed in, just check for existence of static
          ancillary data, but do not attempt to download.  This is useful in test
          scripts to confirm the ancillary data exists prior to running tests, but
          do not actually attempt to download the full 410GB dataset.  This will force
          the test to fail, and provide the appropriate command to download the
          ancillary data.

          Note this script will never update an existing static data directory. In
          order to update an existing static data directory, you must manually remove,
          then re-run this script without the validate_only flag.
          """,
    )
    args = parser.parse_args()
    fetch_static(args.ancillary_data_directory, validate_only=args.validate_only)
