# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Pytest file for calling integration bash scripts."""

import os
import pytest

from tests.integration_tests.test_integration import full_setup  # noqa: F401

from tests.integration_tests.test_integration import (
    run_script_with_bash,
    setup_environment as setup_geoips_environment,
)

# 'full' repo integration tests
full_integ_test_calls = [
    "$geoips_repopath/tests/utils/check_code.sh all $repopath",
    "$geoips_repopath/docs/build_docs.sh $repopath $pkgname html_only",
    "$repopath/tests/scripts/abi.Cloud-Fraction.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Fraction.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Top-Height.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Base-Height.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Mask.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Optical-Depth.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Phase.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Effective-Radius.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Temp-ACHA.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Cloud-Type.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Temp-11p0.imagery_clean.sh",
    "$repopath/tests/scripts/ahi.Temp-3p75.imagery_clean.sh",
]
# Preprocessing test of running CLAVR-x and GeoIPS on output of clavrx.
preprocess_integ_test_calls = [
    "$repopath/tests/scripts/abi.clavrx_proc.sh",
    "$repopath/tests/scripts/ahi.clavrx_proc.sh",
    "$repopath/tests/scripts/modis.clavrx_proc.sh",
    "$repopath/tests/scripts/viirs.clavrx_proc.sh",
]


def setup_environment():
    """
    Set up necessary environment variables for integration tests.

    Configures paths and package names for the GeoIPS core and its plugins by
    setting environment variables required for the integration tests. Assumes
    that 'GEOIPS_PACKAGES_DIR' is already set in the environment.

    Notes
    -----
    The following environment variables are set:
    - geoips_repopath
    - geoips_pkgname
    - repopath
    - pkgname
    """
    # Setup base geoips environment
    setup_geoips_environment()
    # Setup current repo's environment
    os.environ["repopath"] = os.path.join(os.path.dirname(__file__), "..", "..")
    os.environ["pkgname"] = "geoips_clavrx"


@pytest.mark.full
@pytest.mark.integration
@pytest.mark.parametrize("script", full_integ_test_calls)
def test_integ_full_test_script(full_setup: None, script: str):  # noqa: F811
    """
    Run integration test scripts by executing specified shell commands.

    Parameters
    ----------
    script : str
        Shell command to execute as part of the integration test. The command may
        contain environment variables which will be expanded before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the shell command returns a non-zero exit status.
    """
    setup_environment()
    run_script_with_bash(script)


@pytest.mark.external_preprocessing
@pytest.mark.parametrize("script", preprocess_integ_test_calls)
def test_integ_preprocess_test_script(full_setup: None, script: str):  # noqa: F811
    """
    Run integration test scripts by executing specified shell commands.

    Parameters
    ----------
    script : str
        Shell command to execute as part of the integration test. The command may
        contain environment variables which will be expanded before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the shell command returns a non-zero exit status.
    """
    setup_environment()
    run_script_with_bash(script)
