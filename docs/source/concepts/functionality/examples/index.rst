.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Examples
********

This document links to test scripts that serve as usage examples for the
``geoips_clavrx`` plugin.

Imagery Examples
================

The following scripts produce imagery from existing CLAVR-x outputs:

abi.imagery_clean.sh
--------------------

Produces clean ABI cloud product imagery from preprocessed CLAVR-x Level 2 outputs.

.. code-block:: bash

    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi.imagery_clean.sh

ahi.imagery_clean.sh
--------------------

Produces clean AHI cloud product imagery from preprocessed CLAVR-x Level 2 outputs.

.. code-block:: bash

    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.imagery_clean.sh

Full Pipeline Example
=====================

clavrx_proc_to_geoips.sh
------------------------

Demonstrates the full pipeline from CLAVR-x preprocessing through GeoIPS imagery
production:

.. code-block:: bash

    $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/clavrx_proc_to_geoips.sh

This script:

1. Runs CLAVR-x preprocessing via ``run_clavrx.py``
2. Reads CLAVR-x Level 2 outputs via ``clavrx_hdf4``
3. Applies colormappers and products from ``clavrx.yaml``
4. Produces final imagery outputs

Test Markers Reference
======================

The ``geoips_clavrx`` test suite uses the following pytest markers:

+----------------------------------+--------------------------------------------------+
| Marker                           | Description                                      |
+==================================+==================================================+
| ``base``                         | Base tests that run quickly and do not require   |
|                                  | external data or network access.                 |
+----------------------------------+--------------------------------------------------+
| ``full``                         | Full test suite including all tests. Runs        |
|                                  | slower than ``base`` tests.                      |
+----------------------------------+--------------------------------------------------+
| ``external_preprocessing``       | Tests that require CLAVR-x preprocessing to be   |
|                                  | run externally. Requires CLAVR-x executable and  |
|                                  | ancillary data to be installed.                  |
+----------------------------------+--------------------------------------------------+
| ``lint``                         | Linting tests that check code style and          |
|                                  | formatting conventions.                          |
+----------------------------------+--------------------------------------------------+
| ``validation``                   | Validation tests that verify data integrity and  |
|                                  | output correctness.                              |
+----------------------------------+--------------------------------------------------+

Running tests with markers:

.. code-block:: bash

    # Run only base tests
    pytest -m base

    # Run full test suite
    pytest -m full

    # Run tests requiring external preprocessing
    pytest -m external_preprocessing

    # Run lint tests
    pytest -m lint

    # Run validation tests
    pytest -m validation

    # Run multiple marker groups
    pytest -m "base or lint"
