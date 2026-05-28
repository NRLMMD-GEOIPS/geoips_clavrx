# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Script to install clavrx in the GeoIPS expected location.

This expects a pre-existing pre-built executable that can just be copied into the
appropriate location for the GeoIPS wrappers to run CLAVR-x appropriately.
"""

import os
import requests
import sys

import argparse

# Geoips packages
from geoips.filenames.base_paths import PATHS as gpaths


def install_clavrx(src_exec, dest_exec, validate_only=False):
    """Installs clavrx using pre-built executable."""
    if os.path.exists(dest_exec) and validate_only:
        print("SUCCESS! CLAVR-x executable exists and validate_only True!")
        sys.exit(0)
    elif validate_only:
        print("FAILED File does not exist, and validate_only requested, failing.")
        print("Please run this script again without the validate_only flag.")
        raise FileNotFoundError("CLAVR-x executable does not exist, validate_only True")

    # setup files
    if os.path.exists(dest_exec):
        print("FAILED File exists already and validate_only NOT requested, failing.")
        print("Please remove executable and run the same command again to replace.")
        print(f"# rm -fv {dest_exec}")
        raise IOError("CLAVR-x executable exists, and validate_only False")

    # setup dirs
    clavrx_dir = os.path.dirname(dest_exec)
    if not os.path.isdir(clavrx_dir):
        os.mkdir(clavrx_dir)

    if "https:" in src_exec:
        print("Installing pre-built CLAVR-X from {}".format(src_exec))
        # install
        try:
            r = requests.get(src_exec, timeout=12)
        except requests.exceptions.Timeout:
            print("HTTP timeout.")
            raise
        if r.status_code != 200:
            raise ValueError(
                f"Bad request url for {src_exec}, got HTTPS code {r.status_code}"
            )

        with open(dest_exec, "wb") as output_file:
            output_file.write(r.content)
        os.chmod(dest_exec, 0o700)

    return None


if __name__ == "__main__":
    """Run installer."""
    parser = argparse.ArgumentParser(
        description="""The GeoIPS install_clavrx.py wrapper for installing a
          pre-built executable of the
          University of Wisconsin Cooperative Institude for Meteorological Satellite
          Studies (CIMSS) Clouds for AVHRR Extended (CLAVR-x) processing system.

          This expects CLAVR-x has already been built appropriately, and will ensure
          the pre-built executable is in the correct location expected by the
          GeoIPS run_clavrx.py wrapper script.

          Currently this installation script only supports pulling a pre-built
          executable from the CIMSS gitlab CI that has been tested and shown to work
          with the test scripts contained in this GeoIPS plugin package repository.

          In the future we will support the ability to run a separate "build_clavrx.py"
          wrapper script, which will build CLAVR-x from scratch with specific
          functionality enabled, then this "install_clavrx.py" script will
          copy the resulting local pre-built executable into place

          Note this script will *not* replace an existing executable.  If you need to
          update an existing executable, you will need to manually replace it in
          advance.
          """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--source_prebuilt_clavrx_exec",
        type=str,
        required=False,
        default=(
            "https://gitlab.ssec.wisc.edu/clavrx/clavrx-dev/-"
            "/jobs/117757/artifacts/raw/run/bin/clavrxorb?inline=false"
        ),
        help="""Full path to original pre-built clavrx executable.

            If this path contains https:, it will be pulled remotely using
            requests.get.

            If this path is a local file on disk, it will simply be copied into place.

            Note this script will NOT replace an existing executable - you must
            manually remove prior to running to update an existing executable.

            NOTE local file on disk not currently supported, but should be easy to add.
            The intent is we can add a 'build_clavrx.py' script that will build
            CLAVR-x however we want it, then 'install_clavrx.py' will just copy that
            pre-built executable to the $GEOIPS_DEPENDENCIEs_DIR/clavrx/run location.
            """,
    )
    parser.add_argument(
        "--dest_geoips_clavrx_exec",
        type=str,
        required=False,
        default=os.path.join(
            gpaths["GEOIPS_DEPENDENCIES_DIR"], "clavrx", "run_clavrxorb"
        ),
        help="""Full path to pre-built clavrx executable for use within the GeoIPS
            wrapper scripts. The --source_prebuilt_clavrx_exec will be copied to this
            location.  This --dest_geoips_clavrx_exec must match the --clavrx_exec
            passed into run_clavrx.py.

            Note this script will NOT replace an existing executable - you must
            manually remove prior to running to update an existing executable.
            """,
    )
    parser.add_argument(
        "--validate_only",
        action="store_true",
        help="""If --validate_only passed in, return zero if the executable
          exists, and return non-zero if it does not exist. This can
          be useful for tests, where we don't want to pass the executable already
          exists, but we want to provide appropriate instructions for installing
          the executable if it does NOT exist.

          If --validate_only is NOT passed in, fail with non-zero if the
          executable exists, to avoid inadvertently replacing/updating an installed
          geoips clavrx executable. The user must always manually remove an existing
          executable in order to replace it with a new version. This script will never
          replace an existing executable.
          """,
    )
    args = parser.parse_args()
    install_clavrx(
        args.source_prebuilt_clavrx_exec,
        args.dest_geoips_clavrx_exec,
        args.validate_only,
    )
