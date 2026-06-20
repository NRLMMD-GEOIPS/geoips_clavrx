# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#######################################################################################
#######################################################################################
# Start basic pytest imports
# These can be copied as is between repositories and provide the basic pytest-based
# integration test functionality required by all repositories.
#######################################################################################

"""Pytest file for calling integration bash scripts."""

import os
import pytest

# Only use base_setup, because full_setup requires ALL test data repositories.
from tests.integration_tests.test_integration import base_setup  # noqa: F401

# Import the validation and lint test calls, these are identical for all repos
from tests.integration_tests.test_integration import (
    validation_integ_test_calls,
    lint_integ_test_calls,
)

from tests.integration_tests.test_integration import (
    run_script_with_bash,
    setup_environment as setup_geoips_environment,
)

#######################################################################################
# End basic pytest imports
# Copied as is between repos
#######################################################################################
#######################################################################################

#######################################################################################
#######################################################################################
# Start repo specific pytest functionality
# These cannot be copied as is between repositories
#######################################################################################

# Single base test to ensure basic plugin repo functionality.
base_integ_test_calls = [
    "$repopath/tests/scripts/abi.imagery_clean.sh Cloud-Fraction",
]

# Exhaustive test of all remaining functionality in this repo (excluding base+lint).
full_integ_test_calls = [
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Fraction",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Top-Height",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Base-Height",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Mask",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Optical-Depth",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Phase",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Effective-Radius",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Temp-ACHA",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Cloud-Type",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Temp-11p0",
    "$repopath/tests/scripts/ahi.imagery_clean.sh Temp-3p75",
]

# Preprocessing test of running CLAVR-x and GeoIPS on output of clavrx.
preprocess_integ_test_calls = [
    "$repopath/tests/scripts/clavrx_proc_to_geoips.sh ahi",
    "$repopath/tests/scripts/clavrx_proc_to_geoips.sh abi",
    "$repopath/tests/scripts/clavrx_proc_to_geoips.sh modis",
    "$repopath/tests/scripts/clavrx_proc_to_geoips.sh viirs",
    "$repopath/tests/scripts/clavrx_proc_to_geoips.sh fci",
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
    os.environ["repopath"] = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    os.environ["pkgname"] = "geoips_clavrx"


@pytest.mark.external_preprocessing
@pytest.mark.parametrize("script", preprocess_integ_test_calls)
def test_integ_preprocess_test_script(base_setup: None, script: str):  # noqa: F811
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


#######################################################################################
# End repo specific pytest functionality
# Not copied as is between repos
#######################################################################################
#######################################################################################

#######################################################################################
#######################################################################################
# Start basic pytest functions
# These can be copied as is between repositories and provide the basic pytest-based
# integration test functionality required by all repositories.
#######################################################################################


@pytest.mark.base
@pytest.mark.integration
@pytest.mark.parametrize("script", base_integ_test_calls)
def test_integ_base_test_script(
    base_setup: None, script: str, fail_on_missing_data: bool  # noqa: F811
):
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
    run_script_with_bash(script, fail_on_missing_data)


@pytest.mark.full
@pytest.mark.integration
@pytest.mark.parametrize("script", full_integ_test_calls)
def test_integ_full_test_script(
    base_setup: None, script: str, fail_on_missing_data: bool  # noqa: F811
):
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
    run_script_with_bash(script, fail_on_missing_data)


@pytest.mark.lint
@pytest.mark.integration
@pytest.mark.parametrize("script", lint_integ_test_calls)
def test_integ_lint_test_script(base_setup: None, script: str):  # noqa: F811
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


@pytest.mark.validation
@pytest.mark.integration
@pytest.mark.parametrize("script", validation_integ_test_calls)
def test_integ_validation_script(base_setup: None, script: str):  # noqa: F811
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


#######################################################################################
# End basic pytest functions
# Copied as is between repos
#######################################################################################
#######################################################################################
