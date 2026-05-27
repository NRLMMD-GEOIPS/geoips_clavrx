.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _clavrx-algorithms:

CLAVR-x Algorithms
******************

To extend GeoIPS with a new ``algorithm`` plugin, first follow the :ref:`instructions for
setting up a plugin package<plugin-development-setup>`.

.. _plugin-development-setup:

Plugin Development Setup
------------------------

Module plugins are required to have several top-level variables:
    * name
    * interface
    * family
    * docstring

Please see documentation for
:ref:`additional info on GeoIPS required attributes<required-attributes-algorithms>`

.. _required-attributes-algorithms:

How the absdiff_cth Algorithm Works as a Model
----------------------------------------------

The ``absdiff_cth`` algorithm computes the absolute difference between cloud top height
values from two consecutive CLAVR-x files one timestep apart. It serves as a model for
creating new algorithms that transform input variables into new cloud products.

The algorithm:

#. Takes a dictionary of xarray Datasets containing input variables (e.g., cloud top height)
#. Extracts the required variables from the dataset
#. Applies a mathematical transformation (absolute difference in this case)
#. Applies data range corrections (clipping, normalization)
#. Returns the modified xarray with the new product variable

The ``absdiff_cth`` algorithm uses the ``xarray_dict_to_xarray`` algorithm family, which
transforms a dictionary of xarray Datasets into a single xarray Dataset.

How to Create a New Algorithm
-----------------------------

The following steps will teach you how to create a custom algorithm plugin. First off,
change directories to your algorithms directory.

.. code-block:: bash

    cd $MY_PKG_DIR/$MY_PKG_NAME/plugins/modules/algorithms

Create a file called ``my_cloud_depth.py`` (see below). To convert this algorithm to
my_cloud_depth you'll need to update the ``docstring`` (multiline string at the top
of the file) and update the ``name`` to ``my_cloud_depth``.

Copy and paste the code block below into ``my_cloud_depth.py``

.. code-block:: python

    """Cloud depth product.

    Difference of cloud top height and cloud base height.
    """
    import logging
    import numpy as np
    from xarray import DataArray

    LOG = logging.getLogger(__name__)

    interface = "algorithms"
    family = "xarray_dict_to_xarray"
    name = "my_cloud_depth"
    # Conventionally matches the name of the plugin definition file, but can be anything
    # that does not contain hyphens.

Each module-based plugin is required to have a ``call`` function. This is how geoips
will interact with the module-based plugins. See below for the call signature of the
my_cloud_depth.py plugin. To see a list of required arguments for each algorithm family,
see this `link <https://github.com/NRLMMD-GEOIPS/geoips/blob/main/geoips/interfaces/module_based/algorithms.py>`_.

As for keyword arguments (kwargs), you can create as many as you want provided you include
them in your product and are needed for your algorithm.

Copy and paste this code into your algorithm file (feel free to remove the comments).

.. code-block:: python

    def call(
        xarray_dict,
        output_data_range=None,
        input_units=None,
        output_units=None,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
        sun_zen_correction=False,
        mask_night=False,
        max_day_zen=None,
        mask_day=False,
        min_night_zen=None,
        gamma_list=None,
        scale_factor=None,
    ):
        """My cloud depth product algorithm manipulation steps."""

The ``xarray_dict`` parameter is a dictionary of xarray Datasets keyed by sector
name (e.g., ``"DATA"``). Access the data through this dictionary.

Add the code block below to your ``call`` function. This is how cloud-depth will be
calculated.

.. code-block:: python

    cth = np.asarray(xarray_dict["DATA"]["cld_height_acha"][0])
    cbh = np.asarray(xarray_dict["DATA"]["cld_height_base_acha"][0])
    lon = np.asarray(xarray_dict["DATA"]["longitude"][0])
    lat = np.asarray(xarray_dict["DATA"]["latitude"][0])

    out = (cth - cbh) * (scale_factor or 0.001)

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        out,
        min_val=output_data_range[0] if output_data_range else 0,
        max_val=output_data_range[1] if output_data_range else 20,
        min_outbounds=min_outbounds,
        max_outbounds=max_outbounds,
        norm=norm,
        inverse=inverse,
    )

    import xarray as xr
    out_xarray = xr.Dataset(
        data_vars={
            "cld_depth": xr.DataArray(data, dims=["y", "x"]),
            "latitude": xr.DataArray(lat, dims=["y", "x"]),
            "longitude": xr.DataArray(lon, dims=["y", "x"]),
        },
        coords={
            "y": np.arange(data.shape[0]),
            "x": np.arange(data.shape[1]),
        },
    )
    return out_xarray

If you have already created a Product defined in the :ref:`Products<clavrx-products>`
section, we should revisit our :doc:`../product/index` product definition
to use the algorithm we just created. Note: If you haven't yet created this product, see the
:ref:`Products<clavrx-products>` section.

If you are using this page as more of a guideline for how to create an algorithm plugin,
it should be noted that *algorithms are useless on their own*. This goes for other plugins
too, like colormappers, interpolators, etc. These are just sub-components of a larger
plugin, that being a Product, which fully defines the process of how to create a Product
via GeoIPS.

In other words, you should implement your product in a fashion similar to what is done
in the :doc:`../product/index` product definition.

Creating a Cloud Water Path Algorithm
-------------------------------------

To create a new algorithm for a different product, such as cloud water path, follow the
same pattern as ``absdiff_cth`` but modify the data manipulation logic:

.. code-block:: python

    """Cloud water path product.

    Computes cloud water path from cloud water content variables.
    """
    import logging
    import numpy as np
    import xarray as xr
    from xarray import DataArray

    LOG = logging.getLogger(__name__)

    interface = "algorithms"
    family = "xarray_dict_to_xarray"
    name = "my_cloud_water_path"

    def call(
        xarray_dict,
        output_data_range=None,
        input_units=None,
        output_units=None,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
        sun_zen_correction=False,
        mask_night=False,
        max_day_zen=None,
        mask_day=False,
        min_night_zen=None,
        gamma_list=None,
        scale_factor=None,
    ):
        """My cloud water path product algorithm manipulation steps."""

        cwp = np.asarray(xarray_dict["DATA"]["cloud_water_path"][0])

        out = cwp * 1000.0  # Convert to g/m^2

        from geoips.data_manipulations.corrections import apply_data_range

        data = apply_data_range(
            out,
            min_val=output_data_range[0] if output_data_range else 0,
            max_val=output_data_range[1] if output_data_range else 100,
            min_outbounds=min_outbounds,
            max_outbounds=max_outbounds,
            norm=norm,
            inverse=inverse,
        )

        out_xarray = xr.Dataset(
            data_vars={
                "cloud_water_path": xr.DataArray(data, dims=["y", "x"]),
            },
            coords={
                "y": np.arange(data.shape[0]),
                "x": np.arange(data.shape[1]),
            },
        )
        return out_xarray

Required Top-Level Attributes and Call Signature
------------------------------------------------

Every algorithm plugin must have:

* ``interface = "algorithms"`` - Identifies this as an algorithm plugin
* ``family = "xarray_dict_to_xarray"`` - Specifies the algorithm family
* ``name`` - Must match the filename (without .py extension)
* ``docstring`` - Multiline string describing the algorithm

The ``call`` function signature for the ``xarray_dict_to_xarray`` family must include:

* ``xarray_dict`` - Dictionary of xarray Datasets, keyed by sector name (e.g., ``"DATA"``)
* ``output_data_range`` - Min/max range for output data (optional)
* ``input_units``, ``output_units`` - Unit conversion parameters (optional)
* ``min_outbounds``, ``max_outbounds`` - How to handle out-of-bounds values
* ``norm``, ``inverse`` - Normalization and inverse transform flags
* ``sun_zen_correction``, ``mask_night``, ``mask_day`` - Solar geometry corrections
* ``gamma_list`` - Gamma correction values
* ``scale_factor`` - Scaling factor for unit conversion
