.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Creating Imagery from CLAVR-x
*****************************

This tutorial shows how to produce cloud product imagery from CLAVR-x output using
GeoIPS.

Basic Command Structure
-----------------------

Use the ``geoips run single_source`` command to generate imagery from CLAVR-x data:

.. code-block:: bash

    geoips run single_source \
        <input_file> \
        --reader_name clavrx_hdf4 \
        --product_name <product_name> \
        --output_formatter <formatter_name> \
        --filename_formatter <filename_formatter> \
        --minimum_coverage <min_coverage> \
        --sector_list <sector>

Where:

* ``<input_file>`` - Path to a CLAVR-x HDF4 output file
* ``<product_name>`` - Name of the cloud product to visualize (e.g., Cloud-Top-Height, Cloud-Fraction)
* ``<formatter_name>`` - Output formatter plugin (e.g., imagery_annotated, imagery_clean)
* ``<filename_formatter>`` - Filename formatter plugin (e.g., geoips_fname)
* ``<min_coverage>`` - Minimum coverage percentage (0 = no minimum)
* ``<sector>`` - Geographic sector to display (e.g., conus, us, global)

Specifying Different Products
-----------------------------

The geoips_clavrx plugin defines 12 cloud products. Common products include:

* Cloud-Top-Height - Cloud top height in kilometers
* Cloud-Base-Height - Cloud base height in kilometers
* Cloud-Fraction - Cloud fraction (0 to 1)
* Cloud-Optical-Depth - Cloud optical depth
* Cloud-Phase - Cloud phase (water, ice, mixed)
* Cloud-Temp-ACHA - Cloud temperature in Kelvin
* Effective-Radius - Cloud particle effective radius

.. code-block:: bash

    # Cloud Fraction imagery
    geoips run single_source \
        $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/goes16_20230113_0000/clavrx_goes16_20230113000020.level2.hdf \
        --reader_name clavrx_hdf4 \
        --product_name Cloud-Fraction \
        --output_formatter imagery_clean \
        --filename_formatter geoips_fname \
        --minimum_coverage 0 \
        --sector_list test_goeseast_eqc_3km_landocean

    # Cloud Top Height imagery
    geoips run single_source \
        $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/goes16_20230113_0000/clavrx_goes16_20230113000020.level2.hdf \
        --reader_name clavrx_hdf4 \
        --product_name Cloud-Top-Height \
        --output_formatter imagery_clean \
        --filename_formatter geoips_fname \
        --minimum_coverage 0 \
        --sector_list test_goeseast_eqc_3km_landocean

Specifying Different Sectors
----------------------------

Replace ``--sector_list conus`` with any valid GeoIPS sector name:

.. code-block:: bash

    --sector_list us        # United States
    --sector_list polar_n   # Northern polar
    --sector_list polar_s   # Southern polar
    --sector_list global    # Global

Specifying Different Output Formatters
--------------------------------------

Replace ``--output_formatter imagery_clean`` with any valid GeoIPS output formatter:

.. code-block:: bash

    --output_formatter imagery_clean   # Clean imagery without annotations
    --output_formatter imagery_annotated    # Annotated imagery

Modifying Test Scripts for Custom Outputs
-----------------------------------------

Test scripts are stored in your plugin package's ``tests/scripts`` directory. To create
a custom output, copy an existing test script and modify it:

.. code-block:: bash

    # Copy an existing test script
    cp $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi.imagery_clean.sh \
       $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/my-custom-product.sh

    # Edit the copied script to change the product name, sector, or formatter
    $EDITOR $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/my-custom-product.sh

    # Run the custom script
    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/my-custom-product.sh

The script will produce a PNG image in the current working directory. Look for the
``SINGLESOURCESUCCESS`` message in the log output to confirm the script completed
successfully.
