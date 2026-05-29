.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Coding Standards
****************

This document outlines the coding standards specific to the geoips_clavrx plugin.
For general GeoIPS coding standards, see the base GeoIPS documentation.

CLAVR-x Variable Naming Conventions
===================================

CLAVR-x output variables should follow the naming conventions used by the
CLAVR-x algorithm itself. When mapping CLAVR-x variables to GeoIPS xarray
data variables, use descriptive names that reflect the physical quantity
being represented.

Common CLAVR-x variables include:

- ``cloud_fraction`` - Cloud fraction (0 to 1.0)
- ``cloud_type`` - Cloud type classification (0 to 13)
- ``cloud_mask`` - Cloud mask (0 to 3)
- ``cld_height_base`` - Cloud base height (0 to 20 km)
- ``cld_height_acha`` - Cloud top height (ACHA method, 0 to 20 km)
- ``cld_opd_acha`` - Cloud optical depth (ACHA method, -0.2 to 8)
- ``cloud_phase`` - Cloud phase (0 to 5)
- ``cld_temp_acha`` - Cloud temperature (ACHA method, 160 to 320 K)
- ``temp_3_75um_nom`` - Brightness temperature at 3.75 um
- ``temp_11_0um_nom`` - Brightness temperature at 11.0 um
- ``cld_reff_acha`` - Cloud effective radius (ACHA method, 0 to 160 um)

When creating new variables, follow these rules:

- Use lowercase with underscores separating words
- Use units in the variable name only when necessary for disambiguation
- Keep variable names consistent with CLAVR-x documentation where possible

Colormapper Naming Convention
=============================

All colormappers in the geoips_clavrx plugin must use the ``cmap_`` prefix
in their Python module file names. This convention makes it easy to
identify colormapper modules among other Python modules.

Examples:

- ``cmap_cldTemp.py``
- ``cmap_cldOpd.py``
- ``cmap_cldPhase.py``

The colormapper Python modules should define:

- ``interface`` - Set to "colormappers"
- ``family`` - Set to "matplotlib"
- ``name`` - The colormapper name
- ``call`` function - Returns a dictionary of matplotlib color information

YAML Product Structure Conventions
===================================

Product YAML files in geoips_clavrx follow the standard GeoIPS product
configuration structure with plugin-specific conventions:

- ``name`` - Must match the YAML filename without the ``.yaml`` extension
- ``source_names`` - List of reader names that provide the data (e.g., ``clavrx``)
- ``algorithm`` - Set to ``single_channel`` or ``absdiff_cth`` for CLAVR-x based products
- ``colormapper`` - Nested plugin specification: ``colormapper.plugin.name`` references the colormapper module, ``colormapper.plugin.arguments`` passes runtime arguments
- ``docstring`` - Human-readable description of the product
- ``spec`` - Defines product variables, colormapper, and other specifications for imagery generation

Product YAML files should be organized in the ``geoips_clavrx/plugins/yaml/products/``
directory with subdirectories organized by satellite platform or product
category as appropriate.
