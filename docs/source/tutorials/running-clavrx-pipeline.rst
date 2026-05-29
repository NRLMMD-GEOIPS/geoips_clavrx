.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Running the CLAVR-x Pipeline
****************************

This tutorial walks through the complete CLAVR-x pipeline, from environment setup to
producing GeoIPS imagery from CLAVR-x output.

Step 1: Set Up Environment Variables
------------------------------------

Set the following environment variables before proceeding:

.. code-block:: bash

    export GEOIPS_PACKAGES_DIR=$HOME/geoips_packages
    export GEOIPS_ANCILDAT=$HOME/geoips_ancildata
    export GEOIPS_DEPENDENCIES_DIR=$HOME/geoips_dependencies
    export GEOIPS_OUTDIRS=$HOME/geoips_outdirs
    export GEOIPS_TESTDATA_DIR=$GEOIPS_PACKAGES_DIR/test_data

Step 2: Install CLAVR-x Prebuilt Binary
---------------------------------------

Install the CLAVR-x prebuilt binary using the plugin's wrapper script:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py

This copies the prebuilt CLAVR-x executable into ``$GEOIPS_DEPENDENCIES_DIR/clavrx/``.

Step 3: Download Static Ancillary Data
--------------------------------------

CLAVR-x requires static ancillary data that does not change between runs. Download this
data once and store it in a persistent location. This download is approximately **410 GB**:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py

The static data will be stored in ``$GEOIPS_ANCILDAT/clavrx/static/``.

Step 4: Download Dynamic Ancillary Data
---------------------------------------

CLAVR-x also requires dynamic ancillary data that changes with each satellite overpass.
Download this data before each processing run:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py

For a specific date:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py --download_dtg 20240115

The dynamic data will be stored in ``$GEOIPS_ANCILDAT/clavrx/dynamic/``.

Step 5: Run CLAVR-x on ABI/AHI/MODIS/VIIRS Input
------------------------------------------------

Run CLAVR-x on satellite input data. CLAVR-x supports ABI (GOES-R/GOES-16/GOES-17),
AHI (Himawari-8/9), MODIS (Terra/Aqua), and VIIRS (Suomi NPP/NOAA-20) input.

Use the plugin's ``run_clavrx.py`` wrapper script:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py \
        --input_files /path/to/abi/L1B/*.nc \
        --runtime_directory /tmp/clavrx_runtime \
        --template_options_file $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/clavrx_options_template \
        --level2_list $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/level2_list \
        --output_directory $GEOIPS_OUTDIRS/preprocessed/clavrx/ \
        --clavrx_exec $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

Step 6: Verify Output
---------------------

Verify that CLAVR-x produced the expected output files. CLAVR-x outputs HDF4 files
containing cloud product variables such as cloud top height, cloud base height,
cloud fraction, and more:

.. code-block:: bash

    ls -la $GEOIPS_OUTDIRS/preprocessed/clavrx/*.level2.hdf

Step 7: Run GeoIPS on CLAVR-x Output
------------------------------------

Use GeoIPS to process and visualize CLAVR-x output. The geoips_clavrx plugin provides
readers, algorithms, colormappers, and products for working with CLAVR-x data.

.. code-block:: bash

    geoips run single_source \
        $GEOIPS_OUTDIRS/preprocessed/clavrx/clavrx_OR_ABI-L1b-RadF-M6C01_G16_s20240151200194.level2.hdf \
        --reader_name clavrx_hdf4 \
        --product_name Cloud-Top-Height \
        --output_formatter imagery_clean \
        --filename_formatter geoips_fname \
        --minimum_coverage 0 \
        --sector_list conus

The output will be a PNG image of the Cloud-Top-Height product over the CONUS sector.
