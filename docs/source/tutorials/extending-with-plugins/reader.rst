.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

.. _describe-clavrx-readers:

CLAVR-x Readers
***************

GeoIPS readers are module-based plugins that create a method of reading in many types of
satellite derived data. The CLAVR-x plugin provides readers for CLAVR-x output files.

GeoIPS readers return a dictionary of xarrays minimally containing the following
variables.

.. _clavrx-minimum-contents:

+------------------------------------------+--------------------------------------------------------+-----------------+
| Common Names(s)                          | Required Name in Xarray                                | Data Format     |
+==========================================+========================================================+=================+
| Latitude, Longitude                      | latitude, longitude                                    | float/int       |
+------------------------------------------+--------------------------------------------------------+-----------------+
| Variables of Interest                    | <customizable> but should match names used by products |  float/int      |
+------------------------------------------+--------------------------------------------------------+-----------------+
| Time of Observation                      | time                                                   | datetime object |
+------------------------------------------+--------------------------------------------------------+-----------------+
| Metadata attr: Data Source               | source_name                                            | string          |
+------------------------------------------+--------------------------------------------------------+-----------------+
| Metadata attr: Time of First Observation | start_datetime                                         | datetime object |
+------------------------------------------+--------------------------------------------------------+-----------------+
| Metadata attr: Time of Final Observation | end_datetime                                           | datetime object |
+------------------------------------------+--------------------------------------------------------+-----------------+

The ``source_name`` set in your reader correlates to the ``source_names`` property in
your products plugin. As an example, ``my_clavrx_products.yaml`` data is read in by the
`clavrx_hdf4 reader
<https://github.com/NRLMMD-GEOIPS/geoips_clavrx/blob/main/geoips_clavrx/plugins/modules/readers/clavrx_hdf4.py>`_,
which sets its source name as ``clavrx``. See the module-level ``source_name`` attribute of that file for proof! In every
product of ``my_clavrx_products.yaml``, we set the source name as ``clavrx`` since that
is the reader we want to use to load in our data. See ``My-Cloud-Top-Height`` below for
an example of that.

.. code-block:: yaml

    spec:
      products:
        - name: My-Cloud-Top-Height
          source_names: [clavrx]
          docstring: |
            CLAVR-x Cloud Top Height
          product_defaults: Cloud-Height
          spec:
            variables: ["cld_height_acha", "latitude", "longitude"]

The variables defined in the product above directly correlate to the variables contained
in the Xarray after being processed by the reader. If you changed those variables name
in your product, it wouldn't work!

As with any GeoIPS plugin, a reader is required to define the top level attributes
``interface``, ``family``, and ``docstring``.

Please see documentation for
:ref:`additional info on GeoIPS required attributes<required-attributes-readers>`,

.. _required-attributes-readers:

Reader Structure Overview
-------------------------

A GeoIPS reader is module-based, and therefore must have a ``call`` function, as do all
other module-based plugins. Readers generally also have one or several ``read functions``,
that exist outside of the call function. Optionally, a reader can also include ``utility
functions`` that perform some kind of operation on inputs. We will discuss each of each
of these in further detail now.

* The ``call`` function.
    * The call function is the main driver of a GeoIPS reader. It accepts the keyword
      arguments (kwargs) that contain the list of files to be read, and a handful of
      instructions that adjust how the reader functions.

* Reader functions
    * Populate Xarrays with data from the files themselves. They technically are
      optional if you include all of this in the call function, but it is best practice
      to create them.

* Utility functions
    * Perform operations on the inputs, typically to convert them to a format
      understandable by GeoIPS. This could be using ``np.meshgrid(lats, lons)`` to
      create a 2D array of latitude and longitude, or whatever else you envision.

* Unit tests
    * Unit testing to help test conformity and validity of the reader and test data.
      For more details see the reference unit tests documentation.

See below for an example of all three functions signatures in action.

.. code-block:: python

    def year_day_hours_to_datetime(time_array, use_shape=None):  # Utility Function

    def read_cloudprops(fname, chans=None, metadata_only=False):  # Read Function

    def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):  # Call Function, with
    important kwargs

There are a few key points of the call function that should be talked about. First off,
is the metadata required by GeoIPS that is associated with your data. Mainly, there are
three key-pieces to the metadata that *must be defined*: ``start_datetime``, ``end_datetime``,
and ``source_name``. As we discussed earlier, this is how your product can find the correct
reader at runtime to load in your data.

Another important piece of the reader is the ``metadata_only`` section. While it's not
required, it gives users the option to only load in the metadata if that's all they need.
This allows GeoIPS to not load in very large files multiple times.

See below for an example of both of those key points.

.. code-block:: python

    xarrays[data_type].attrs["start_datetime"] = start_date
    xarrays[data_type].attrs["end_datetime"] = end_date
    xarrays[data_type].attrs["source_name"] = "clavrx"

    if metadata_only is True:
        LOG.info(
            "metadata_only is True, reading only first file for metadata information and returning"
        )
        return {"METADATA": xarrays[data_type]}

The last key point of a GeoIPS reader is the *read* function. Again, while not required,
it is best practice to separate your read function from the call function, for clarity
and ease of use in the future. See below for an example of invoking a read function.

.. code-block:: python

    xarray_objs = {}
    for fname in fnames:
        xarray_objs[basename(fname)] = read_cloudprops(fname, chans=chans, metadata_only=metadata_only)  # The read function is invoked here

    xarray_objs["METADATA"] = list(xarray_objs.values())[0][[]]
    """Different approach to the above code section that reads data and then sets the metadata afterward"""

    return xarray_objs

A Typical Read Function
-----------------------

When creating a read function in a GeoIPS Reader, it is largely the dealer's choice (ie.
yourself). The read function needs to open the file and read the contents (:ref:`Remember the
Minimum Contents Table<clavrx-minimum-contents>`) into a dictionary of xarrays to be passed
along to GeoIPS. However, as with any piece of code, there are some challenges that you
should be aware of.

The first challenge are 1-Dimensional (1D) Variables. It's ok if your variables are 1D,
so long as *all of them* are 1D. You may need to do some array manipulation to get
everything even! This is a common issue particularly with time arrays.

Another issue is time formatting. For example ``TAI93``, ``UTC``, ``binary string``,
``seconds since epoch``... there are a lot of ways time is reported in data formats.
Consult the users guide for your data to figure out how to convert time variables to the
required datetime object format.

The last challenge that should be noted is reading in the necessary ``channels`` for your
product. GeoIPS cannot intelligently read required channels unless you code your reader
to do just that. Remember that your ``call`` script is invoked with the ``chans``
parameter. Use that information to save you and your customer's time!

How to Add a New CLAVR-x Product Variable to the Reader
-------------------------------------------------------

To add a new CLAVR-x product variable to the reader, follow these steps:

#. Open the ``clavrx_hdf4.py`` reader file in your plugin package.

#. Add the new variable to the read function, extracting it from the CLAVR-x HDF4 file.

#. Add the new variable to the returned xarray dataset.

#. Update the product definition to include the new variable in the ``variables`` list.

Example: Adding a New Variable to the CLAVR-x HDF4 Reader
---------------------------------------------------------

Below is an example of adding a new variable called ``cloud_type`` to the ``clavrx_hdf4``
reader.

.. code-block:: python

    def read_cloudprops(fname, chans=None, metadata_only=False):
        """Read a single CLAVR-x file fname."""
        from pyhdf.SD import SD, SDC
        import xarray as xr
        import numpy as np

        fileobj = SD(str(fname), SDC.READ)

        # Extract existing variables
        cth = fileobj.select("cld_height_acha").get()
        cbh = fileobj.select("cld_height_base_acha").get()
        lat = fileobj.select("latitude").get()
        lon = fileobj.select("longitude").get()

        # Extract new variable
        cloud_type = fileobj.select("cloud_type").get()

        # Setup xarray variables
        final_xarray = xr.Dataset()
        final_xarray["latitude"] = xr.DataArray(lat)
        final_xarray["longitude"] = xr.DataArray(lon)
        final_xarray["cld_height_acha"] = xr.DataArray(cth)
        final_xarray["cld_height_base_acha"] = xr.DataArray(cbh)
        final_xarray["cloud_type"] = xr.DataArray(cloud_type)  # New variable
        return final_xarray

After adding the variable to the reader, update your product definition:

.. code-block:: yaml

    spec:
      products:
        - name: My-Cloud-Type
          source_names: [clavrx]
          docstring: |
            CLAVR-x Cloud Type
          product_defaults: Cloud-Height
          spec:
            variables: ["cloud_type", "latitude", "longitude"]
