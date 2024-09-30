# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Test the clavrx package and installation."""

# python packages
import os
import logging
from argparse import ArgumentParser
from datetime import datetime

# geoips packages
from geoips_clavrx.clavrx.install_utils import run_shell_command


LOG = logging.getLogger(__name__)

geoips_dependencies_dir = os.getenv("GEOIPS_DEPENDENCIES_DIR")


def get_env(clavrx_dir, netcdf_dir, hdf4_dir, hdf5_dir):
    """Set environment variables for testing."""
    environ = dict(os.environ)
    environ["LD_LIBRARY_PATH"] = (
        f"{netcdf_dir}/lib:{hdf4_dir}/lib:\
    {hdf5_dir}/lib:{environ.get('LD_LIBRARY_PATH', '')}"
    )
    # Not sure if NCDIR and NFDIR are required, but can't hurt
    environ["NCDIR"] = netcdf_dir
    environ["NFDIR"] = netcdf_dir
    environ["CPPFLAGS"] = f"-I{netcdf_dir}/include -I{hdf5_dir}/include"
    environ["LDFLAGS"] = f"-L{netcdf_dir}/lib -L{netcdf_dir}/lib"
    environ["PATH"] = f"{clavrx_dir}/CLAVRx/run/bin:{environ.get('PATH', '')}"

    return environ


def run_clavrxorb(clavrx_dir, hdf4_dir, hdf5_dir, netcdf_dir):
    """Run shell commands to setup options and testing directories."""
    # Changing to the run directory within CLAVRx
    os.chdir(f"{clavrx_dir}/CLAVRx/run/")

    run_shell_command(
        "cp example_runscripts/run_clavrxorb .",
        "copying run_clavrxorb executable to run directory",
        env=None,
    )

    run_shell_command(
        "cp examples-clavrx_options/clavrx_options .",
        "copying clavrx_options test example to run directory",
        env=None,
    )

    run_shell_command(
        "cp examples-file_list/file_list .",
        "copying file_list test example to run directory",
        env=None,
    )

    run_shell_command(
        "cp examples-level2_list/level2_list .",
        "copying level2_list test example to run directory",
        env=None,
    )

    # edit paths within files
    # Change first line in clavrx_options to "$GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary"

    with open(f"{geoips_dependencies_dir}/clavrx/CLAVRx/run/clavrx_options") as f:
        lines = f.readlines()
        lines[0] = f"{geoips_dependencies_dir}/clavrx/ancillary/\n"
        lines[39] = (
            "2 1 1 !E6 native res sample(0)/average(1),\
        average+stats(2), X_stride(>=1), Y_Stride (>=1))\n"
        )
    with open(f"{geoips_dependencies_dir}/clavrx/CLAVRx/run/clavrx_options", "w") as f:
        f.writelines(lines)

    env = get_env(clavrx_dir, hdf4_dir, hdf5_dir, netcdf_dir)
    LOG.info("Running clavrx")
    run_shell_command(
        "./run_clavrxorb",
        "running clavrxorb executable to test CLAVRx installation",
        env=env,
    )


if __name__ == "__main__":
    """Set arguments and runs test suite."""
    parser = ArgumentParser()

    parser.add_argument(
        "--clavrx_dir",
        type=str,
        default=f"{geoips_dependencies_dir}/clavrx/",
        help="directory containing clavrx build",
    )
    parser.add_argument(
        "--hdf4_dir",
        type=str,
        default=f"{geoips_dependencies_dir}/clavrx/lib/hdf4/hdf-4.2.15/",
        help="directory containing hdf4",
    )
    parser.add_argument(
        "--hdf5_dir",
        type=str,
        default=f"{geoips_dependencies_dir}/clavrx/lib/hdf5/hdf5-1.10.9/",
        help="directory containing hdf5",
    )
    parser.add_argument(
        "--netcdf_dir",
        type=str,
        default=f"{geoips_dependencies_dir}/clavrx/lib/netcdf/netcdf-4.9.0/",
        help="directory containing netcdf",
    )

    parser.add_argument("-l", "--log", type=str, default="INFO", help="Log level")
    args = parser.parse_args()

    clavrx_dir = args.clavrx_dir
    hdf4_dir = args.hdf4_dir
    hdf5_dir = args.hdf5_dir
    netcdf_dir = args.netcdf_dir
    logging.basicConfig(
        filename="clavrx_test_{}.log".format(
            datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        ),
        encoding="utf-8",
        level=logging.INFO,
    )

    LOG.info("Starting Clavrx run")
    run_clavrxorb(clavrx_dir, hdf4_dir, hdf5_dir, netcdf_dir)
