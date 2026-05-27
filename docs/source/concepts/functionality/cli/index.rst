.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Plugin CLI Reference
********************

This document describes the command-line interfaces for the four wrapper scripts
provided by the ``geoips_clavrx`` plugin.

install_clavrx.py
=================

Installs the CLAVR-x executable into the GeoIPS dependency directory.

Arguments
---------

``--source_prebuilt_clavrx_exec``
    Path to a prebuilt CLAVR-x executable binary to install.

``--dest_geoips_clavrx_exec``
    Destination path where the CLAVR-x executable will be installed.
    Typically ``$GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb``.

``--validate_only``
    If set, validate that both the source executable and the destination
    path exist, and skip the installation.

Example
-------

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py \
        --source_prebuilt_clavrx_exec /opt/clavrx/bin/run_clavrxorb \
        --dest_geoips_clavrx_exec $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

run_clavrx.py
=============

Executes CLAVR-x orbital processing to produce Level 2 cloud product files.

Arguments
---------

``--input_files``
    Space-separated list of Level 1-B input satellite files to process.

``--runtime_directory``
    Directory for CLAVR-x runtime working files.

``--template_options_file``
    Path to the CLAVR-x options template file containing runtime configuration.

``--level2_list``
    Path to the file listing which Level 2 products to generate.

``--output_directory``
    Directory where CLAVR-x Level 2 output files will be written.
    Typically ``$GEOIPS_OUTDIRS/preprocessed/clavrx/``.

``--ancillary_data_directory``
    Base directory for CLAVR-x ancillary data. Static and dynamic data
    will be read from subdirectories under this path.
    Typically ``$GEOIPS_ANCILDAT/clavrx/``.

``--clavrx_exec``
    Path to the CLAVR-x executable.
    Typically ``$GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb``.

Example
-------

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py \
        --input_files /data/abi/L1b/*.nc \
        --runtime_directory /tmp/clavrx_runtime \
        --template_options_file /path/to/clavrx_options_template \
        --level2_list /path/to/level2_list \
        --output_directory $GEOIPS_OUTDIRS/preprocessed/clavrx/ \
        --ancillary_data_directory $GEOIPS_ANCILDAT/clavrx \
        --clavrx_exec $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

get_ancildata_static.py
=======================

Downloads static ancillary data required by CLAVR-x (surface type, terrain, etc.).

Arguments
---------

``--ancillary_data_directory``
    Base directory for ancillary data. Static data will be stored in
    ``ancillary_data_directory/static/``.

``--validate_only``
    If set, only validate that the required static data exists.
    Do not perform the download.

Example
-------

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py \
        --ancillary_data_directory $GEOIPS_ANCILDAT/clavrx

update_ancildata_dynamic.py
===========================

Downloads dynamic ancillary data that changes with time (ephemeris, atmospheric profiles).

Arguments
---------

``--download_dtg``
    Date-time group (DTG) for which to download dynamic ancillary data.
    Format: ``YYYYMMDD`` (default: current date).

``--ancillary_data_directory``
    Base directory for ancillary data. Dynamic data will be stored in
    ``ancillary_data_directory/dynamic/``.

``--clean_dynamic_empty_files``
    If set, remove empty download artifacts after downloading dynamic data.

Example
-------

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py \
        --download_dtg 20240115 \
        --ancillary_data_directory $GEOIPS_ANCILDAT/clavrx
