.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _linux-installation-clavrx:

Installation on Linux
*********************

This page provides instructions for installing the geoips_clavrx plugin using pip in a
conda virtual environment on Linux.

1. Create and Activate Conda Environment
=========================================

.. code-block:: bash

    conda create -n geoips python=3.9
    conda activate geoips

2. Install Base GeoIPS
======================

First, install the base GeoIPS package. See the `base GeoIPS documentation <https://geoips.github.io>`_
for full installation instructions.

3. Clone the geoips_clavrx Repository
=====================================

Clone the plugin repository into your GeoIPS packages directory:

.. code-block:: bash

    git clone https://github.com/NRLMMD-GEOIPS/geoips_clavrx $GEOIPS_PACKAGES_DIR/geoips_clavrx

4. Install the Plugin
=====================

Install the plugin in editable mode:

.. code-block:: bash

    pip install -e $GEOIPS_PACKAGES_DIR/geoips_clavrx

5. Register Plugins
===================

Register the newly installed plugins with GeoIPS:

.. code-block:: bash

    geoips config create-registries

6. Install CLAVR-x Prebuilt Binary
==================================

Install the CLAVR-x prebuilt binary executable:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py

7. Download Static Ancillary Data
=================================

Download the static ancillary data required for CLAVR-x preprocessing. This download is approximately
**410 GB**:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py

8. Download Dynamic Ancillary Data
==================================

Download the dynamic ancillary data that is updated regularly:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py

9. Install Test Data
====================

Install the test data required for integration tests:

.. code-block:: bash

    geoips config install test_data_clavrx

10. Verify Installation
=======================

Verify that the installation was successful by running the plugin tests:

.. code-block:: bash

    pytest $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/

If all tests pass, the installation is complete and the CLAVR-x plugin is ready to use.
