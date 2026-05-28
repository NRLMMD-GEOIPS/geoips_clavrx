    # # # This source code is subject to the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

CLAVR-x GeoIPS Plugin Package
=============================

The geoips_clavrx package is a GeoIPS-compatible plugin, intended to be used
within the GeoIPS ecosystem.
Please see the
[GeoIPS Documentation](https://github.com/NRLMMD-GEOIPS/geoips#readme)
for more information on the GeoIPS plugin architecture and base infrastructure.

Package Overview
----------------

The geoips_clavrx package provides the capability for reading and plotting
data files produced from the Clouds for AVHRR Extended (CLAVR-x) package.

This package also contains wrappers for installing and running the main CLAVR-x
package, prior to processing the CLAVR-x outputs through GeoIPS.

This package does not currently include complete build of the external
CLAVR-x package from source, but
uses a pre-built binary from the University of Wisconsin gitlab page. Future
releases intend to include the option for building CLAVR-x directly from source
if and when needed.

System Requirements
-------------------

* geoips >= 1.18.0
* Test data repos contained in $GEOIPS_TESTDATA_DIR for geoips tests to pass.

For full clavrx installation, and clavrx through GeoIPS test scripts

* GEOIPS_ANCILDAT environment variable set for clavrx ancillary data population
  (ancillary data will be populated by test scripts if it does not exist already within
  GEOIPS_ANCILDAT/clavrx directory).
* GEOIPS_DEPENDENCIES_DIR environment variable for clavrx installation and test.
* GEOIPS_PACKAGES_DIR environment variable containing geoips_clavrx repo clone, for
  clavrx template configuration files for tests.
* GEOIPS_OUTDIRS environment variable for both clavrx and geoips test outputs.

IF REQUIRED: Install base geoips package
----------------------------------------
SKIP IF YOU HAVE ALREADY INSTALLED BASE GEOIPS ENVIRONMENT

If GeoIPS Base is not yet installed, follow the
[installation instructions](https://github.com/NRLMMD-GEOIPS/geoips#installation)
within the geoips source repo documentation.

Install geoips_clavrx package
-----------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    git clone https://github.com/NRLMMD-GEOIPS/geoips_clavrx $GEOIPS_PACKAGES_DIR/geoips_clavrx
    pip install -e $GEOIPS_PACKAGES_DIR/geoips_clavrx
    geoips config create-registries
```

Install CLAVR-x and required dependencies
-----------------------------------------

Follow installation of full pipeline on the 
[CLAVRx pipeline](./geoips_clavrx/clavrx/README.md) docs

Note the `clavrx_proc_to_geoips.sh` test script expects complete clavrx
installation in the standard geoips locations, and will complete successfully
if you follow the instructions in the clavrx/README.md.

Test geoips_clavrx installation
-------------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # Install the clavrx test data repo
    geoips config install test_data_clavrx

    # Run geoips only tests, on pre-existing CLAVR-x outputs
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi.imagery_clean.sh Cloud-Fraction
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.imagery_clean.sh Cloud-Base-Height

    # Run clavrx through geoips tests, if you did the full clavrx+geoips installation
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/clavrx_proc_to_geoips.sh ahi
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/clavrx_proc_to_geoips.sh abi

    # Run all tests, both geoips only and CLAVR-x preprocessing + GeoIPS
    cd $GEOIPS_PACKAGES_DIR/geoips_clavrx
    pytest
```
