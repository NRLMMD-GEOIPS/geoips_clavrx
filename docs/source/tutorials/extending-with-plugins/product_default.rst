.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _clavrx-product-defaults:

CLAVR-x Product Defaults
************************

Lets first discuss what product defaults are. Product Defaults, as their name implies,
are defaults for commonly used GeoIPS products. They allow you to create default product
arguments, for interfaces like interpolators, algorithms, and colormappers, so that you
don't have to fully specify them each time you create a new product. In our use case,
Cloud Top Height, Cloud Base Height, and Cloud Depth all use very similar arguments,
besides the algorithm they employ. Therefore, it'd be smart to have a Cloud-Height
product default, and override such default file wherever it is necessary.

GeoIPS has a number of product_defaults plugins defined to help you not reinvent the wheel, but:
    * You can override any of the product defaults within your product definition
    * You can absolutely define all of the available options within your product plugin

To give you a better idea of what we are talking about, feel free to view some files in these folders.
    * `Pre-defined CLAVR-x product defaults
      <https://github.com/NRLMMD-GEOIPS/geoips_clavrx/tree/main/geoips_clavrx/plugins/yaml/product_defaults>`_ (part of
      the CLAVR-x plugin)
    * `Pre-defined GeoIPS product defaults
      <https://github.com/NRLMMD-GEOIPS/geoips/tree/main/geoips/plugins/yaml/product_defaults>`_

If you have product definition parameters that you want to reuse (i.e. if you're
copy/pasting product definition parameters!), consider creating a product default for
your plugin.

The top level attributes
``interface``, ``family``, and ``docstring``
are required for every GeoIPS plugin.

Please see documentation for
:ref:`additional info on these GeoIPS required attributes<required-attributes-product-defaults>`

.. _required-attributes-product-defaults:

How Product Defaults Work and When to Use Them
----------------------------------------------

Product defaults reduce duplication in product definitions. When multiple products share
the same algorithm, interpolator, and colormapper settings, you can define those settings
once in a product default and reference it by name.

Use product defaults when:

* Multiple products share the same algorithm, interpolator, and colormapper
* You want to standardize settings across a family of products
* You want to make changes to shared settings in one place

When NOT to use product defaults:

* A product has unique settings that don't match any existing default
* You only have one product that would use the default

Different Implementations of Product Defaults
---------------------------------------------

Shown below is the geoips_clavrx Cloud-Height product defaults yaml file. That we will be
using in all of our :ref:`Products<clavrx-products>`. Wherever we add
``product_defaults: Cloud-Height``, we are referring to these properties.

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

In your product you can use the product_defaults verbatim, as is shown below.

.. code-block:: yaml

    spec:
      products:
        - name: My-Cloud-Top-Height
          source_names: ["clavrx"]
          docstring: |
            CLAVR-x Cloud Top Height
          product_defaults: Cloud-Height
          spec:
            variables: ["cld_height_acha", "latitude", "longitude"]

Overriding Defaults in Product Definitions
------------------------------------------

You can also override just some parts of the product defaults. In this example, we
override the algorithm plugin contained in the Cloud-Height product defaults, with our
own specification. You can also omit certain arguments. For example, if we left out
``norm: True`` shown below, then that argument would be supplied by the Cloud-Height
algorithm's norm default value.

.. code-block:: yaml

    interface: products
    family: list
    name: clavrx
    docstring: |
      The Products geoips_clavrx default configuration
    spec:
      products:
        - name: Cloud-Top-Height
          source_names: ["clavrx"]
          docstring: |
            CLAVR-x Cloud Top Height
          product_defaults: Cloud-Height
          spec:
            variables: ["cld_height_acha", "latitude", "longitude"]
            algorithm:
              plugin:
                name: single_channel
                arguments:
                  output_data_range: [0, 20]
                  scale_factor: 0.001
                  min_outbounds: "mask"
                  max_outbounds: "mask"
                  norm: True
                  inverse: False

We also have the option to fully define a product without using product defaults. This
may be your use case if you have a product that isn't related to any other product you've
created.

To do this:
    * Remove the 'product_defaults' property
    * Add the 'family' property
    * This is shown in the code block below.

.. code-block:: yaml

    interface: products
    family: list
    name: clavrx
    docstring: |
      The Products geoips_clavrx default configuration
    spec:
      products:
        - name: Cloud-Top-Height
          source_names: ["clavrx"]
          docstring: |
            CLAVR-x Cloud Top Height
          family: interpolator_algorithm_colormapper  # Note: Absdiff-Cloud-Top-Height uses "algorithm_interpolator_colormapper"
          spec:
            variables: ["cld_height_acha", "latitude", "longitude"]
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
                  min_outbounds: "mask"
                  max_outbounds: "mask"
                  norm: True
                  inverse: False
            colormapper:
              plugin:
                name: cmap_cldHeight
                arguments:
                  data_range: [0, 20]

Creating New Product Defaults
-----------------------------

If you have product definition parameters that you want to reuse across multiple products,
consider creating a new product default.

#. Create a new YAML file in your plugin package's ``plugins/yaml/product_defaults/``
   directory.

#. Define the top-level attributes and the ``spec`` section:

.. code-block:: yaml

    interface: product_defaults
    family: interpolator_algorithm_colormapper
    name: My-Product-Defaults
    docstring: |
      The My-Product-Defaults product_defaults geoips_clavrx configuration.
    spec:
      interpolator:
        plugin:
          name: interp_nearest
          arguments: {}
      algorithm:
        plugin:
          name: single_channel
          arguments:
            output_data_range: [0, 100]
            scale_factor: 1.0
            min_outbounds: "crop"
            max_outbounds: "crop"
            norm: False
            inverse: False
      colormapper:
        plugin:
          name: cmap_my_colormap
          arguments:
            data_range: [0, 100]

#. Reference the new product default in your product definitions:

.. code-block:: yaml

    spec:
      products:
        - name: My-Product
          source_names: ["clavrx"]
          docstring: |
            CLAVR-x My Product
          product_defaults: My-Product-Defaults
          spec:
            variables: ["cld_my_variable", "latitude", "longitude"]
