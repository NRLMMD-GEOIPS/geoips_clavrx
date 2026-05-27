.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _clavrx_best_practices:

CLAVR-x Plugin Best Practices
*****************************

There are many ways to incorporate the geoips_clavrx plugin into your research or operational flow.
While the developers do not want to be prescriptivist, we recommend a series of best practices
to ensure that your CLAVR-x plugin deployment experience is as smooth as possible.

Recommended Directory Layout
============================

A recommended directory layout for CLAVR-x deployments:

.. code-block:: bash

    $HOME/
    ├── geoips/                          # GEOIPS_PACKAGES_DIR
    │   ├── geoips/                      # Base GeoIPS package
    │   └── geoips_clavrx/               # CLAVR-x plugin package
    ├── ancillary_data/                  # GEOIPS_ANCILDAT
    │   ├── static/                      # Static ancillary data (~410 GB)
    │   └── dynamic/                     # Dynamic ancillary data (updated regularly)
    ├── dependencies/                    # GEOIPS_DEPENDENCIES_DIR
    │   └── clavrx/                      # CLAVR-x executable and dependencies
    └── test_data/                       # GEOIPS_TESTDATA_DIR
        └── test_data_clavrx/            # CLAVR-x test data

Setting Up Environment Variables Persistently
=============================================

Add the following to your ``~/.bashrc`` or ``~/.zshrc`` to set environment variables persistently:

.. code-block:: bash

    export GEOIPS_PACKAGES_DIR=$HOME/geoips
    export GEOIPS_TESTDATA_DIR=$GEOIPS_PACKAGES_DIR/test_data
    export GEOIPS_OUTDIRS=$GEOIPS_PACKAGES_DIR/outdirs
    export GEOIPS_DEPENDENCIES_DIR=$GEOIPS_PACKAGES_DIR/dependencies
    export GEOIPS_ANCILDAT=$GEOIPS_PACKAGES_DIR/ancillary_data

    # Reactivate your conda environment after setting variables
    conda deactivate && conda activate geoips

Using Shared Ancillary Data for Multiple Users
==============================================

If multiple users on a system need access to the CLAVR-x ancillary data, consider:

1. Storing the static ancillary data on a shared network filesystem.
2. Setting ``GEOIPS_ANCILDAT`` to point to the shared location for all users.
3. Ensuring proper read permissions are set on the shared directory.

This approach avoids duplicating the ~410 GB of static ancillary data across multiple systems.

When to Use Docker vs. Native Install
=====================================

Use **Docker** when:

- You are on macOS and cannot run the CLAVR-x prebuilt binary natively.
- You want an isolated, reproducible environment.
- You need to deploy CLAVR-x in a containerized infrastructure.

Use a **Native Install** when:

- You are on a supported Linux distribution.
- You need direct access to the file system for large data transfers.
- You are developing or modifying the CLAVR-x plugin code.

Running Tests Post-Installation
===============================

After installation, always verify your setup by running the plugin tests:

.. code-block:: bash

    pytest $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/

If you encounter test failures, check the troubleshooting guide for common issues.
