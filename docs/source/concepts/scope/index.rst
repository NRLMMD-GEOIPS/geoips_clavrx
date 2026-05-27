.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Scope
*****

This document defines what the ``geoips_clavrx`` plugin does and does not cover.

What This Plugin Does
=====================

The ``geoips_clavrx`` plugin:

* Reads CLAVR-x HDF4 and NetCDF4 Level 2 cloud product files via the ``clavrx_hdf4``
  and ``clavrx_netcdf4`` readers
* Converts CLAVR-x Level 2 data into GeoIPS-compatible xarray DataArrays with proper
  metadata and coordinate systems
* Applies colormappers to cloud products for visual imagery production
* Defines 12 cloud product imagery pipelines in ``clavrx.yaml``
* Provides 3 product default YAML files for reusable configuration
* Wraps CLAVR-x preprocessing (executable installation, ancillary data download,
  orbital processing) via Python scripts
* Produces cloud fraction, cloud type, cloud mask, cloud top/base height, cloud
  optical depth, cloud phase, cloud temperature, effective radius, and brightness
  temperature imagery for ABI, AHI, MODIS, and VIIRS sensors

What This Plugin Does NOT Do
=========================

The ``geoips_clavrx`` plugin does **not**:

* Run CLAVR-x in near real-time. Near real-time processing of CLAVR-x is outside the
  scope of this plugin. Users must run CLAVR-x preprocessing separately and then use
  GeoIPS to read and visualize the output.
* Download Level 1-B input data. The raw satellite radiance data that CLAVR-x requires
  as input must be obtained through other means (e.g., NOAA CLASS, NASA LAADS).
* Distribute output products. This plugin produces imagery files but does not include
  mechanisms for distributing or publishing those products to external systems.
* Build CLAVR-x from source. The plugin supports installing prebuilt CLAVR-x binaries
  only. Building CLAVR-x from source code is not supported.

Future Plans / Roadmap
======================

Planned future work for the ``geoips_clavrx`` plugin:

* **Build-from-source support** - Support for building CLAVR-x from source code in
  addition to prebuilt binaries.
* **Additional sensors** - Support for more satellite sensors beyond ABI, AHI, MODIS,
  and VIIRS.
* **Additional algorithms** - New cloud product algorithms beyond the current
  ``absdiff_cth`` and inherited ``single_channel``.
