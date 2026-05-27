.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _troubleshooting-clavrx:

Troubleshooting Your Installation
*********************************

We will compile any potential issues people encounter during the installation
process here. Please reach out to the GeoIPS team if you have an issue
not already found on this page.

RTTOV Registration Errors
=========================

If you encounter RTTOV registration errors during CLAVR-x preprocessing (e.g., if using
a source-built CLAVR-x with RTTOV support), you need to complete the RTTOV registration
flow with NWP SAF. Follow the registration instructions at the `NWP SAF RTTOV website
<https://www.nwpsaf.es>`_ to obtain the required registration files. Note that the prebuilt
CLAVR-x binary does not include RTTOV, so this error does not apply when using the
prebuilt binary.

"Static Ancillary Data Not Found"
==================================

This error indicates that the static ancillary data has not been downloaded or is not
located in the expected directory. The static ancillary data download is approximately
**410 GB**.

To resolve this:

1. Run the static ancillary data download script:

   .. code-block:: bash

       python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py --ancillary_data_directory $GEOIPS_ANCILDAT/clavrx

2. If the download is too large, check if your site has an existing shared copy of the
   static ancillary data and update ``GEOIPS_ANCILDAT`` to point to it.

"CLAVR-x Executable Not Found"
===============================

This error may appear as a "validate-only" error when the CLAVR-x executable is not
present in the expected location. To resolve:

1. Verify the executable exists:

   .. code-block:: bash

       ls $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

2. If it is missing, force reinstall the CLAVR-x binary:

   .. code-block:: bash

       python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py

3. If you are on macOS, use Docker instead since the prebuilt binary is Linux-only.

Conda Environment Conflicts
===========================

If you are building CLAVR-x from source and encounter compilation errors related to
gcc/gfortran version mismatches, ensure your conda environment has compatible versions:

.. code-block:: bash

    conda install -c conda-forge gcc gfortran

Make sure the compiler versions are compatible with the CLAVR-x source code requirements.
This section only applies when building from source; prebuilt binary users do not need
compilers.

"Dynamic Ancillary Data Missing for Given Date"
================================================

This error occurs when the dynamic ancillary data has not been updated for the date
you are processing. To resolve:

1. Update the dynamic ancillary data:

   .. code-block:: bash

        python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py --download_dtg YYYYMMDD --ancillary_data_directory $GEOIPS_ANCILDAT/clavrx

2. Ensure ``GEOIPS_ANCILDAT`` points to the correct directory containing the dynamic data.

"Test Data Not Found"
=====================

This error indicates that the ``GEOIPS_TESTDATA_DIR`` environment variable is not set
or the test data has not been downloaded.

To resolve:

1. Ensure the environment variable is set:

   .. code-block:: bash

       echo $GEOIPS_TESTDATA_DIR

2. Install the test data:

   .. code-block:: bash

       geoips config install test_data_clavrx

3. If the directory does not exist, create it:

   .. code-block:: bash

       mkdir -p $GEOIPS_TESTDATA_DIR
