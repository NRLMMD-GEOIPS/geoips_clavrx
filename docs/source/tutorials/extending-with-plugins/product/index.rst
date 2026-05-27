.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _clavrx-products:

CLAVR-x Products
****************

This section discusses how to create multiple products for CLAVR-x data, specifically
Cloud-Top-Height and Cloud-Base-Height. Products are the cornerstone
plugin for GeoIPS, as they define how to produce a specific product as a combination of
other plugins. Products use other plugins, such as an algorithm, colormapper,
interpolator, etc. to generate the correct result.

How clavrx.yaml Defines 12 Products
-----------------------------------

The ``clavrx.yaml`` product definition file in the geoips_clavrx plugin defines 12
cloud products. Each product specifies:

* ``name`` - The product name used by GeoIPS
* ``source_names`` - Data source identifier (matching the reader's ``source_name`` attribute)
* ``docstring`` - Description of the product
* ``product_defaults`` - Default algorithm, interpolator, and colormapper settings
* ``spec.variables`` - Input variables required from the reader

The 12 products defined in ``clavrx.yaml`` include:

* Cloud-Fraction
* Cloud-Type
* Cloud-Mask
* Cloud-Top-Height
* Cloud-Base-Height
* Cloud-Optical-Depth
* Cloud-Phase
* Cloud-Temp-ACHA
* Temp-3p75
* Temp-11p0
* Effective-Radius
* Absdiff-Cloud-Top-Height

How product_defaults Simplify Product Definitions
-------------------------------------------------

The ``product_defaults`` mechanism allows you to define common settings once and reuse
them across multiple products. The geoips_clavrx plugin defines several product defaults:

**CLAVR-x-Base**

Base product defaults for standard CLAVR-x products. Provides default interpolator,
algorithm, and colormapper settings.

**Cloud-Height**

Product defaults for cloud height products (Cloud-Top-Height, Cloud-Base-Height).
Uses the ``cmap_cldHeight`` colormapper and ``single_channel`` algorithm with
appropriate data ranges.

**Temp**

Product defaults for temperature-related products (Cloud-Temp-ACHA,
Temp-3p75, Temp-11p0). Uses temperature-appropriate colormappers and data ranges.

For example, the Cloud-Height product defaults look like:

.. code-block:: yaml

    interface: product_defaults
    family: interpolator_algorithm_colormapper
    name: Cloud-Height
    docstring: |
      The Cloud-Height product_defaults geoips_clavrx configuration.
    spec:
      interpolator:
        plugin:
          name: interp_nearest
          arguments: {}
      algorithm:
        plugin:
          name: single_channel
          arguments:
            output_data_range: [0, 20]
            scale_factor: 0.001
            min_outbounds: "crop"
            max_outbounds: "crop"
            norm: False
            inverse: False
      colormapper:
        plugin:
          name: cmap_cldHeight
          arguments:
            data_range: [0, 20]

When a product specifies ``product_defaults: Cloud-Height``, it inherits all of these
settings. The product only needs to specify its unique attributes (name, variables, etc.).

How to Add a New Product to clavrx.yaml
---------------------------------------

To add a new product to ``clavrx.yaml``, follow these steps:

#. Open the ``clavrx.yaml`` file in your plugin package's products directory.

#. Add a new entry to the ``products`` list with the following structure:

.. code-block:: yaml

    interface: products
    family: list
    name: clavrx
    docstring: |
      The Products geoips_clavrx default configuration
    spec:
      products:
        # ... existing products ...
        - name: My-New-Product
          source_names: ["clavrx"]
          docstring: |
            CLAVR-x My New Product
          product_defaults: Cloud-Height  # Or another appropriate default
          spec:
            variables: ["cld_new_variable", "latitude", "longitude"]

#. If the new product requires a different algorithm or colormapper, override the
   product defaults:

.. code-block:: yaml

    - name: My-New-Product
      source_names: [clavrx]
      docstring: |
        CLAVR-x My New Product
      product_defaults: Cloud-Height
      spec:
        variables: ["cld_new_variable", "latitude", "longitude"]
        algorithm:
          plugin:
            name: my_custom_algorithm
            arguments:
              output_data_range: [0, 100]
        colormapper:
          plugin:
            name: my_custom_colormapper
            arguments:
              data_range: [0, 100]

#. Create a test script in your ``tests/scripts`` directory to verify the product works.

#. Run the test script to confirm the product produces correct imagery.
