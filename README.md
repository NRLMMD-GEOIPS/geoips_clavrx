    # # # Distribution Statement A. Approved for public release. Distribution unlimited.
    # # #
    # # # Author:
    # # # Naval Research Laboratory, Marine Meteorology Division
    # # #
    # # # This program is free software: you can redistribute it and/or modify it under
    # # # the terms of the NRLMMD License included with this program. This program is
    # # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
    # # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
    # # # for more details. If you did not receive the license, for more information see:
    # # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

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
data files produced from the Clouds for AVHRR Extended package.

This package does not currently include installation of clavrx itself, but
expects you are able to produce CLAVR-x outputs for ingest into geoips_clavrx.

System Requirements
-------------------

* geoips >= 1.10.2
* Test data repos contained in $GEOIPS_TESTDATA_DIR for tests to pass.

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
```

Test geoips_clavrx installation
-------------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # Install the clavrx test data repo
    git clone https://github.com/NRLMMD-GEOIPS/test_data_clavrx $GEOIPS_TESTDATA_DIR/test_data_clavrx

    # Run all tests
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/test_all.sh
```

