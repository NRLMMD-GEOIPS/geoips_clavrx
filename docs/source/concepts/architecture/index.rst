.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Architecture
************

This document describes the architecture of the ``geoips_clavrx`` plugin, which integrates
the CLAVR-x cloud product retrieval algorithm into the GeoIPS imagery production framework.

Overview
========

The ``geoips_clavrx`` plugin bridges CLAVR-x (Clouds for AVHRR Extended)
Level 2 cloud products with GeoIPS readers, colormappers, and products. CLAVR-x processes
satellite radiance data from multiple sensors (ABI, AHI, MODIS, VIIRS) to produce cloud
property retrievals including cloud fraction, cloud type, cloud mask, cloud top height,
cloud base height, cloud optical depth, cloud phase, cloud temperature, effective radius,
and brightness temperatures.

GeoIPS Interface Mappings
=========================

The plugin implements the following GeoIPS interfaces:

Readers
-------

Two readers parse CLAVR-x Level 2 output files into GeoIPS-compatible xarray DataArrays:

* ``clavrx_hdf4`` - Reads HDF4 Level 2 files produced by CLAVR-x. Handles HDF4 SCALED
  dataset conventions with ``scale_factor`` and ``add_offset`` attributes.
* ``clavrx_netcdf4`` - Reads NetCDF4 Level 2 files. Supports both packed and unpacked
  data formats.

Algorithms
----------

* ``absdiff_cth`` - Computes absolute difference cloud top height between consecutive
  time steps, useful for detecting cloud evolution.
* ``single_channel`` - Inherited from the base ``geoips`` plugin, used for single-channel
  brightness temperature imagery.

Colormappers
------------

Nine colormapper modules map cloud product values to visual color tables:

* ``cmap_cldFraction`` - Cloud fraction (0 to 1.0)
* ``cmap_cldType`` - Cloud type (categorical, 0-13)
* ``cmap_cldMask`` - Cloud mask (categorical, 0-3)
* ``cmap_cldHeight`` - Cloud height (0 to 20 km)
* ``cmap_cldOpd`` - Cloud optical depth (negative to positive values)
* ``cmap_cldPhase`` - Cloud phase (categorical, 0-5)
* ``cmap_cldTemp`` - Cloud temperature (160 to 320 K)
* ``cmap_cldReff`` - Cloud effective radius (0 to 160 micrometers)
* ``cmap_IR`` - Infrared brightness temperature (180 to 340 K)

Products
--------

The ``clavrx.yaml`` product file defines 12 products that combine readers, colormappers,
sectors, and output formatters into complete imagery production pipelines.

Product Defaults
----------------

Three product default YAML files provide reusable configuration:

* ``CLAVR-x-Base`` - Base defaults for all CLAVR-x products
* ``Cloud-Height`` - Defaults specific to cloud height products
* ``Temp`` - Defaults for temperature-related products

CLAVR-x Preprocessing
=====================

The plugin includes four wrapper scripts that handle CLAVR-x preprocessing:

* ``install_clavrx.py`` - Installs the CLAVR-x executable into the GeoIPS dependency
  directory. Supports prebuilt binaries via ``--source_prebuilt_clavrx_exec`` (local
  path or HTTPS URL for remote download).
* ``run_clavrx.py`` - Executes CLAVR-x orbital processing. Reads input satellite files,
  applies ancillary data, and produces Level 2 cloud product outputs.
* ``get_ancildata_static.py`` - Downloads static ancillary data (surface type, terrain,
  etc.) required by CLAVR-x.
* ``update_ancildata_dynamic.py`` - Downloads dynamic ancillary data (ephemeris,
  atmospheric profiles) that changes with time.

Data Flow
=========

The data flow from raw satellite data to GeoIPS imagery is:

1. Raw satellite Level 1-B data is downloaded (outside this plugin's scope)
2. ``run_clavrx.py`` processes Level 1-B data with CLAVR-x to produce HDF4/NetCDF4
   Level 2 cloud product files in ``$GEOIPS_OUTDIRS/preprocessed/clavrx/``
3. The ``clavrx_hdf4`` or ``clavrx_netcdf4`` reader parses Level 2 files into xarray
   DataArrays with proper coordinate systems and metadata
4. Colormappers apply color tables to the DataArrays
5. Products combine all steps into complete imagery outputs

CLAVR-x HDF4 to GeoIPS xarray Conversion
----------------------------------------

CLAVR-x HDF4 files use the SCALED dataset convention where raw integer values are
converted to physical values using:

.. code-block:: python

   physical_value = raw_value * scale_factor + add_offset

The readers apply this conversion automatically and set required xarray metadata:

* ``source_name`` - Identifies the data source (e.g., "clavrx")
* ``platform_name`` - Identifies the satellite platform (e.g., "GOES-17", "HIMAWARI-9")
* ``start_datetime`` / ``end_datetime`` - Validity period of the data

Architecture Diagram
====================

.. note::

   Architecture diagram placeholder. A visual diagram showing the data flow from
   satellite input through CLAVR-x processing to GeoIPS imagery output will be added.

   ::

       Satellite Level 1-B
           |
           v
       run_clavrx.py (CLAVR-x)
           |
           v
       HDF4/NetCDF4 Level 2 Files
           |
           v
       clavrx_hdf4 / clavrx_netcdf4 Reader
           |
           v
       xarray DataArray (GeoIPS internal format)
           |
           v
       Colormapper (cmap_*)
           |
           v
       Product (clavrx.yaml)
           |
           v
       Output Imagery
