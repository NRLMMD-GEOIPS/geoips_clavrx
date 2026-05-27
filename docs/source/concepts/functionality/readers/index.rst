.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Readers
*******

This document describes the two readers provided by the ``geoips_clavrx`` plugin
for reading CLAVR-x Level 2 cloud product files.

clavrx_hdf4
===========

The ``clavrx_hdf4`` reader reads CLAVR-x HDF4 Level 2 files and converts them into
GeoIPS-compatible xarray DataArrays.

File Format
-----------

Reads HDF4 files produced by CLAVR-x with the naming convention:

.. code-block:: text

    CLAVR_x_<platform>_d<date>_t<time>_e<end_time>_c<creation_time>.hdf

For example:

.. code-block:: text

    CLAVR_x_G17_d20240115_t1234567_e1245678_c2345678.hdf

Note: CLAVR-x output files may also use other naming conventions, such as
``clavrx_<sensor>_<datetime>.level2.hdf``. The reader handles both formats
by reading metadata from within the file.

Variables Extracted
-------------------

The reader extracts the following variables from CLAVR-x Level 2 HDF4 files:

* ``cloud_fraction`` - Cloud fraction (0 to 1.0)
* ``cloud_type`` - Cloud type classification (0 to 13)
* ``cloud_mask`` - Cloud mask (0 to 3)
* ``cld_height_acha`` - Cloud top height (ACHA method, 0 to 20 km)
* ``cld_height_base_acha`` - Cloud base height (ACHA method, 0 to 20 km)
* ``cld_height_top_acha`` - Cloud top height (ACHA method, alternative retrieval)
* ``cld_opd_acha`` - Cloud optical depth (ACHA method, -0.2 to 8)
* ``cloud_phase`` - Cloud phase (0 to 5)
* ``cld_temp_acha`` - Cloud temperature (ACHA method, 160 to 320 K)
* ``cloud_water_path`` - Cloud water path
* ``solar_zenith_angle`` - Solar zenith angle
* ``temp_3_75um_nom`` - Brightness temperature at 3.75 um
* ``temp_11_0um_nom`` - Brightness temperature at 11.0 um
* ``cld_reff_acha`` - Cloud effective radius (ACHA method, 0 to 160 um)

HDF4 Scaling Conventions
------------------------

CLAVR-x HDF4 files use the SCALED dataset convention. Raw integer values must be
converted to physical values using the ``scale_factor`` and ``add_offset`` attributes
stored on each dataset:

.. code-block:: python

   physical_value = raw_value * scale_factor + add_offset

The ``clavrx_hdf4`` reader applies this conversion automatically. Datasets without
scaling attributes are used as-is.

Required xarray Metadata
------------------------

The reader sets the following required metadata on each DataArray:

* ``source_name`` - Set to ``"clavrx"``
* ``platform_name`` - Extracted from the file metadata (e.g., ``"goes-17"``, ``"himawari-9"``)
* ``start_datetime`` - Start time parsed from HDF4 file metadata
* ``end_datetime`` - End time parsed from HDF4 file metadata

clavrx_netcdf4
==============

The ``clavrx_netcdf4`` reader reads CLAVR-x NetCDF4 Level 2 files and converts them
into GeoIPS-compatible xarray DataArrays.

File Format
-----------

Reads NetCDF4 Level 2 files produced by CLAVR-x.

Variables Extracted
-------------------

The reader extracts the same variables as ``clavrx_hdf4``:

* ``cloud_fraction`` - Cloud fraction (0 to 1.0)
* ``cloud_type`` - Cloud type classification (0 to 13)
* ``cloud_mask`` - Cloud mask (0 to 3)
* ``cld_height_acha`` - Cloud top height (ACHA method, 0 to 20 km)
* ``cld_height_base_acha`` - Cloud base height (ACHA method, 0 to 20 km)
* ``cld_height_top_acha`` - Cloud top height (ACHA method, alternative retrieval)
* ``cld_opd_acha`` - Cloud optical depth (ACHA method, -0.2 to 8)
* ``cloud_phase`` - Cloud phase (0 to 5)
* ``cld_temp_acha`` - Cloud temperature (ACHA method, 160 to 320 K)
* ``cloud_water_path`` - Cloud water path
* ``solar_zenith_angle`` - Solar zenith angle
* ``temp_3_75um_nom`` - Brightness temperature at 3.75 um
* ``temp_11_0um_nom`` - Brightness temperature at 11.0 um
* ``cld_reff_acha`` - Cloud effective radius (ACHA method, 0 to 160 um)

NetCDF4 Data Formats
--------------------

CLAVR-x NetCDF4 files may contain both packed (integer) and unpacked (floating-point)
data. The reader handles both formats:

* **Packed data** - Uses ``scale_factor`` and ``add_offset`` attributes from the
  NetCDF variable metadata to convert raw values to physical values.
* **Unpacked data** - Uses floating-point values directly without conversion.

Required xarray Metadata
------------------------

The reader sets the same required metadata as ``clavrx_hdf4``:

* ``source_name`` - Set to ``"clavrx"``
* ``platform_name`` - Extracted from the file metadata
* ``start_datetime`` - Start time parsed from NetCDF4 file metadata
* ``end_datetime`` - End time parsed from NetCDF4 file metadata
