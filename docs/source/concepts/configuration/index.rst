.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Configuration
*************

This document describes the environment variables and configuration options required
to run the ``geoips_clavrx`` plugin.

Required Environment Variables
===============================

GEOIPS_ANCILDAT
---------------

Location for CLAVR-x ancillary data. This environment variable is the base path; the
actual ancillary data root for CLAVR-x is ``$GEOIPS_ANCILDAT/clavrx/``, which must
contain both ``static/`` and ``dynamic/`` subdirectories as described in the Ancillary
Data section below.

**Example:**

.. code-block:: bash

    export GEOIPS_ANCILDAT=$HOME/geoips_ancildata

GEOIPS_DEPENDENCIES_DIR
-----------------------

Location for the CLAVR-x executable. The CLAVR-x binary ``run_clavrxorb`` must be
placed at ``$GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb``.

**Example:**

.. code-block:: bash

    export GEOIPS_DEPENDENCIES_DIR=$HOME/geoips_dependencies

GEOIPS_PACKAGES_DIR
-------------------

Location of the GeoIPS plugin packages. This is the parent directory containing the
``geoips_clavrx`` plugin package along with the core ``geoips`` package and any
other plugins.

**Example:**

.. code-block:: bash

    export GEOIPS_PACKAGES_DIR=$HOME/geoips_packages

GEOIPS_OUTDIRS
--------------

Base directory for GeoIPS outputs. CLAVR-x Level 2 output files are written to
``$GEOIPS_OUTDIRS/preprocessed/clavrx/``.

**Example:**

.. code-block:: bash

    export GEOIPS_OUTDIRS=$HOME/geoips_outdirs

GEOIPS_TESTDATA_DIR
-------------------

Location of test data used by the plugin's test suite.

**Example:**

.. code-block:: bash

    export GEOIPS_TESTDATA_DIR=$HOME/geoips_testdata

CLAVR-x Runtime Configuration
=============================

clavrx_options_template
-----------------------

The ``clavrx_options_template`` file specifies runtime options for CLAVR-x processing.
This template is passed to ``run_clavrx.py`` via the ``--template_options_file`` argument.
The template controls which cloud products are retrieved, input file patterns, and
output settings.

level2_list
-----------

The ``level2_list`` file specifies which CLAVR-x Level 2 products to generate. The
file contains a header line (``level2_list_viirs``) followed by a list of output
variable names to include in the CLAVR-x Level 2 output file.

CLAVR-x Output Directory Structure
===================================

CLAVR-x Level 2 output files are written to:

.. code-block:: text

    $GEOIPS_OUTDIRS/preprocessed/clavrx/

Output files are written flat into this directory without date-based subdirectories.
Files are organized by sensor prefix in the filename (e.g., ``clavrx_OR_ABI-...`` for
ABI, ``clavrx_OR_AHI-...`` for AHI, etc.).

Ancillary Data Directory Structure
==================================

Static ancillary data is stored at:

.. code-block:: text

    $GEOIPS_ANCILDAT/clavrx/static/

Dynamic ancillary data is stored at:

.. code-block:: text

    $GEOIPS_ANCILDAT/clavrx/dynamic/

The static directory contains surface classification data, terrain data, and other
fixed reference data. The dynamic directory contains time-varying data such as
ephemeris files and atmospheric profiles.

CLAVR-x Executable Location
===========================

The CLAVR-x executable is located at:

.. code-block:: text

    $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

Install the executable using:

.. code-block:: bash

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py \
        --source_prebuilt_clavrx_exec /path/to/prebuilt/run_clavrxorb \
        --dest_geoips_clavrx_exec $GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

Command Line Configuration
==========================

Most configuration is handled through environment variables. Additional options are
passed via command line arguments to the wrapper scripts. See the
:doc:`../functionality/cli/index` documentation for details on each script's arguments.

Setting Environment Variables
=============================

Below are examples of how to set the required environment variables for different shells.

**Bash:**

.. code-block:: bash

    # Edit your ~/.bashrc
    vim ~/.bashrc
    # Add the following lines to your .bashrc
    export GEOIPS_ANCILDAT=$HOME/geoips_ancildata
    export GEOIPS_DEPENDENCIES_DIR=$HOME/geoips_dependencies
    export GEOIPS_PACKAGES_DIR=$HOME/geoips_packages
    export GEOIPS_OUTDIRS=$HOME/geoips_outdirs
    export GEOIPS_TESTDATA_DIR=$HOME/geoips_testdata
    # Reload your configuration
    source ~/.bashrc

**Zsh:**

.. code-block:: zsh

    # Edit your ~/.zshrc
    vim ~/.zshrc
    # Add the following lines to your .zshrc
    export GEOIPS_ANCILDAT=$HOME/geoips_ancildata
    export GEOIPS_DEPENDENCIES_DIR=$HOME/geoips_dependencies
    export GEOIPS_PACKAGES_DIR=$HOME/geoips_packages
    export GEOIPS_OUTDIRS=$HOME/geoips_outdirs
    export GEOIPS_TESTDATA_DIR=$HOME/geoips_testdata
    # Reload your configuration
    source ~/.zshrc

**Fish:**

.. code-block:: fish

    # Edit your ~/.config/fish/config.fish
    vim ~/.config/fish/config.fish
    # Add the following lines to your config.fish
    set -x GEOIPS_ANCILDAT $HOME/geoips_ancildata
    set -x GEOIPS_DEPENDENCIES_DIR $HOME/geoips_dependencies
    set -x GEOIPS_PACKAGES_DIR $HOME/geoips_packages
    set -x GEOIPS_OUTDIRS $HOME/geoips_outdirs
    set -x GEOIPS_TESTDATA_DIR $HOME/geoips_testdata
    # Reload your configuration
    source ~/.config/fish/config.fish

**Nix:**

.. code-block:: nix

    # In your home.nix, configuration.nix or in a flake:
    home.sessionVariables = {
      GEOIPS_ANCILDAT = "${config.home.homeDirectory}/geoips_ancildata";
      GEOIPS_DEPENDENCIES_DIR = "${config.home.homeDirectory}/geoips_dependencies";
      GEOIPS_PACKAGES_DIR = "${config.home.homeDirectory}/geoips_packages";
      GEOIPS_OUTDIRS = "${config.home.homeDirectory}/geoips_outdirs";
      GEOIPS_TESTDATA_DIR = "${config.home.homeDirectory}/geoips_testdata";
    };

**Conda:**

.. code-block:: bash

    # Set PACKAGES_DIR first
    conda env config vars set GEOIPS_PACKAGES_DIR=$HOME/geoips_packages

    # Reactivate environment for variables to take effect
    conda deactivate && conda activate geoips
    conda env config vars set GEOIPS_ANCILDAT=$GEOIPS_PACKAGES_DIR/ancildata
    conda env config vars set GEOIPS_DEPENDENCIES_DIR=$GEOIPS_PACKAGES_DIR/dependencies
    conda env config vars set GEOIPS_OUTDIRS=$GEOIPS_PACKAGES_DIR/outdirs
    conda env config vars set GEOIPS_TESTDATA_DIR=$GEOIPS_PACKAGES_DIR/test_data
    conda deactivate && conda activate geoips
