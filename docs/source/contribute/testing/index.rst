.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Testing
*******

The geoips_clavrx plugin includes a comprehensive test suite to ensure
correctness of the CLAVR-x integration with GeoIPS.

Test Structure
==============

Tests are organized in the following directories:

- ``tests/scripts/`` - Shell scripts for integration and end-to-end tests

The ``pytest`` command at the repository root runs all tests.

Pytest Markers
==============

Tests use pytest markers to categorize and selectively run test suites:

``base``
  Core integration tests that verify basic functionality without external dependencies.
  These tests run quickly and do not require test data files.

``full``
  Complete test suite including all test categories. Use this for final validation
  before submitting a Pull Request.

``external_preprocessing``
  Tests that require external preprocessing steps or data sources. These tests
  may take longer to run and require additional setup.

``lint``
  Code style and formatting checks using flake8, black, and other linting tools.

``validation``
  Interface and plugin validation tests.

Run tests with markers:

.. code-block:: bash

    pytest -m base
    pytest -m full
    pytest -m external_preprocessing
    pytest -m lint
    pytest -m validation

--no-fail-on-missing-data Flag

The ``--no-fail-on-missing-data`` flag can be used to skip tests that require
specific data files that may not be available in all environments:

.. code-block:: bash

    pytest --no-fail-on-missing-data

This is useful during development when test data files are not yet available,
or when running tests in environments with limited storage.

Test Data Requirements
======================

Some tests require test data files to be present. The following data is needed
for full test coverage:

- CLAVR-x HDF4 data files for testing readers and algorithms
- Sector definition files for testing imagery generation
- Reference output files for validation tests

Test data files should be installed via ``geoips config install test_data_clavrx``
into the ``$GEOIPS_TESTDATA_DIR/test_data_clavrx/`` directory.
Large data files should be excluded from version control using ``.gitignore``
and made available through the GeoIPS data download utilities.
