.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

System Requirements
*******************

The geoips_clavrx plugin has specific system requirements that depend on whether you are running
the base GeoIPS processing or the full CLAVR-x preprocessing pipeline.

Python and GeoIPS Requirements
==============================

- **Python** >= 3.9
- **geoips** >= 1.18.0 (must be installed separately; the ``geoips`` requirement is not
  tracked in ``pyproject.toml``)

Required Environment Variables
==============================

The following environment variables must be set for the plugin to function:

- ``GEOIPS_TESTDATA_DIR`` - Directory for test data
- ``GEOIPS_PACKAGES_DIR`` - Directory where GeoIPS packages are installed
- ``GEOIPS_OUTDIRS`` - Directory for output files
- ``GEOIPS_DEPENDENCIES_DIR`` - Directory for plugin dependencies
- ``GEOIPS_ANCILDAT`` - Directory for ancillary data

Full Pipeline (CLAVR-x Preprocessing) Requirements
==================================================

To run the complete CLAVR-x preprocessing pipeline, you additionally need:

- ``GEOIPS_ANCILDAT`` - Must contain static and dynamic ancillary data for CLAVR-x processing
- ``GEOIPS_DEPENDENCIES_DIR`` - Must contain the CLAVR-x executable

Test Data Repositories
======================

Integration tests require test data repositories to be installed. Use the ``geoips config install``
command to download the necessary test data for the CLAVR-x plugin.

Static Ancillary Data
=====================

The CLAVR-x preprocessing stage requires approximately **410 GB** of static ancillary data.
This data includes surface type information, terrain data, and other reference datasets
needed for cloud product retrieval.

Docker Support
==============

macOS users who cannot run the CLAVR-x prebuilt binary natively should use Docker.
A Dockerfile is provided in the repository to facilitate containerized deployment.
