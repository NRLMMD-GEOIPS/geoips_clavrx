.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _clavrx-colormappers:

CLAVR-x Colormappers
********************

A GeoIPS colormapper defines a method of applying a colormap to imagery. There are
multiple methods to implement this colormap, and we will present those throughout this
section. This section is also largely informational. We will actually implement
colormappers in the :ref:`Create New Colormappers Section<create-colormappers>`

The top level attributes
``interface``, ``family``, and ``docstring``
are required in every GeoIPS plugin.

Please see documentation for
:ref:`additional info on these GeoIPS required attributes<required-attributes-colormappers>`

.. _required-attributes-colormappers:

How Existing Colormappers Work
------------------------------

The `matplotlib_linear_norm plugin
<https://github.com/NRLMMD-GEOIPS/geoips/blob/main/geoips/plugins/modules/colormappers/matplotlib_linear_norm.py>`_
can also leverage ASCII colormap files installed within GeoIPS, installed within a
plugin package, or stored in an arbitrary location on disk.

For example, the ``cmap_cldFraction`` colormapper is a Python-based ``ListedColormap``
that defines cloud fraction colors programmatically. The colormapper returns a dictionary
of matplotlib color information that GeoIPS uses to render the imagery.

Python-based Colormappers
-------------------------

GeoIPS supports two types of colormappers:

**ASCII-based colormappers**

* Defined as plain text files with RGB triplets (0-256 range)
* Simpler to create and modify
* Used with the ``matplotlib_linear_norm`` plugin
* Stored in ``plugins/txt/ascii_palettes/`` within a plugin package
* Best for simple gradient colormaps

**Python-based colormappers**

* Defined as Python modules with a ``call`` function
* More flexible and powerful
* Can use any matplotlib colormap or custom segmented colormaps
* Stored in ``plugins/modules/colormappers/`` within a plugin package
* Best for complex colormaps with specific transition points and colors

.. _create-colormappers:

How to Create a New Colormapper
-------------------------------

We will now go hands on in creating a custom python-based colormapper. This will be
similar to the module shown above, but to your own specifications.

First off, lets create a new colormappers directory and activate it.

.. code-block:: bash

    mkdir -pv $MY_PKG_DIR/$MY_PKG_NAME/plugins/modules/colormappers
    touch $MY_PKG_DIR/$MY_PKG_NAME/plugins/modules/colormappers/__init__.py
    cd $MY_PKG_DIR/$MY_PKG_NAME/plugins/modules/colormappers

Now that we have that directory activated, let's create a file called
``colorful_cloud_height.py``. Once you have that created, copy and paste the code below
into your colormapper python file. Feel free to adjust any of the colors/parameters to
what you need for your own colormap.

.. code-block:: python

    """Module containing colormap for colorful cloud height products."""
    import logging

    LOG = logging.getLogger(__name__)

    interface = "colormappers"
    family = "matplotlib"
    name = "colorful_cloud_height"

    def call(data_range=[0, 20]):
        """Colorful cloud height colormap."""

        transition_vals = [
            (data_range[0], 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 6),
            (6, 8),
            (8, 10),
            (10, 15),
            (15, data_range[1]),
        ]
        transition_colors = [
            ("pink", "red"),
            ("paleturquoise", "teal"),
            ("plum", "rebeccapurple"),
            ("yellow", "chartreuse"),
            ("limegreen", "darkgreen"),
            ("wheat", "darkorange"),
            ("darkgray", "black"),
            ("lightgray", "silver"),
            ("lightskyblue", "deepskyblue"),
        ]

        ticks = [int(xx[0]) for xx in transition_vals]
        tick_labels = ticks + [int(data_range[1])]

        LOG.info("Setting cmap")
        from geoips.image_utils.colormap_utils import create_linear_segmented_colormap
        mpl_cmap = create_linear_segmented_colormap(
            "89pct_cmap", data_range[0], data_range[1], transition_vals, transition_colors
        )

        LOG.info("Setting norm")
        from matplotlib.colors import Normalize
        mpl_norm = Normalize(vmin=data_range[0], vmax=data_range[1])

        cbar_spacing = "proportional"
        mpl_tick_labels = None
        mpl_boundaries = None

        mpl_colors_info = {
            "cmap": mpl_cmap,
            "norm": mpl_norm,
            "cbar_ticks": ticks,
            "cbar_tick_labels": tick_labels,
            "cbar_label": "Cloud Height (km)",
            "boundaries": mpl_boundaries,
            "cbar_spacing": cbar_spacing,
            "colorbar": True,
            "cbar_full_width": True,
        }
        return mpl_colors_info

Now that you've properly created your module-based colormapper, we need to add it to
``pyproject.toml``. Modify your this file (found in the top level of your package
directory) to include the code listed below. Note: if you named your package something
other than ``cool_plugins``, replace that with your package name.

.. code-block:: toml

    [project.entry-points."geoips.colormappers"]
    colorful_cloud_height = "cool_plugins.plugins.modules.colormappers.colorful_cloud_height"

Once you've done that, you'll have to reinstall your package since you modified
``pyproject.toml``. If you don't reinstall, GeoIPS won't find your new colormapper in
its namespace.

.. code-block:: bash

    pip install -e $MY_PKG_DIR

Using Your Custom Python-based Colormapper in a Product
-------------------------------------------------------

Note, this section assumes you've already created the ``my_clavrx_products.yaml`` file.
If you haven't yet, please visit the :ref:`Products Section<clavrx-products>` to create
that file first.

Let's begin by adding a new product to your ``my_clavrx_products.yaml`` file, called
``Cloud-Base-Python-Colors``. This file can be found in your products directory.

Copy and paste the code below into your products file, under the ``products`` section.

.. code-block:: yaml

    - name: Cloud-Base-Python-Colors
      source_names: ["clavrx"]
      docstring: |
        CLAVR-x Colorful Cloud Base Height,
        using a python-based custom colormapper.
      product_defaults: Cloud-Height
      spec:
        variables: ["cld_height_base", "latitude", "longitude"]
        colormapper:
          plugin:
            name: colorful_cloud_height
            arguments: {}

Create a Script to Visualize Your New Colormapper
-------------------------------------------------

Now that we have a product that implements our new colormapper, we should create a
script that visualizes it. Change directories into your /tests/scripts directory, and
create a file called ``clavrx.conus_annotated.cloud-base-python-colors.sh``. Once you've
done that, copy and paste the code below into that file.

.. code-block:: bash

    geoips run single_source \
        $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/goes16_2023101_1600/clavrx_OR_ABI-L1b-RadF-M6C01_G16_s20231011600207.level2.hdf \
        --reader_name clavrx_hdf4 \
        --product_name "Cloud-Base-Python-Colors" \
        --output_formatter imagery_clean \
        --filename_formatter geoips_fname \
        --minimum_coverage 0 \
        --sector_list conus
    ss_retval=$?

Once you've added that code to that file, you can run the script with the command listed
below.

.. code-block:: bash

    $MY_PKG_DIR/tests/scripts/clavrx.conus_annotated.cloud-base-python-colors.sh

This will write some log output. If your script succeeded it will end with INTERACTIVE:
Return Value 0. To view your output, look for a line that says SINGLESOURCESUCCESS. Open
the PNG file to view your custom colormapped imagery.
