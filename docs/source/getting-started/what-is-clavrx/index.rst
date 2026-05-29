.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

What is CLAVR-x
***************

CLAVR-x (Clouds for AVHRR Extended) is a satellite cloud product retrieval algorithm that generates
a suite of cloud-related products from multiple satellite sensors. It is an extension of the original
CLAVR algorithm, designed to work across a wide range of geostationary and polar-orbiting platforms.

This plugin provides a GeoIPS-compatible interface for reading and plotting CLAVR-x Level 2 outputs,
integrating seamlessly into the broader GeoIPS ecosystem for consistent product generation across sensors.

Products Provided
=================

This plugin provides 12 cloud products:

1. Cloud-Fraction
2. Cloud-Type
3. Cloud-Mask
4. Cloud-Top-Height
5. Cloud-Base-Height
6. Cloud-Optical-Depth
7. Cloud-Phase
8. Cloud-Temp-ACHA
9. Temp-3p75
10. Temp-11p0
11. Effective-Radius
12. Absdiff-Cloud-Top-Height

Supported Sensors
=================

The CLAVR-x plugin supports the following satellite sensors:

- **ABI** (Advanced Baseline Imager) on GOES-16 and GOES-17
- **AHI** (Advanced Himawari Imager) on Himawari-8 and Himawari-9
- **MODIS** (Moderate Resolution Imaging Spectroradiometer) on Terra and Aqua
- **VIIRS** (Visible Infrared Imaging Radiometer Suite) on SNPP and JPSS

Data Flow
=========

The CLAVR-x plugin operates in two main stages:



**CLAVR-x Preprocessing Stage:**

ABI, AHI, MODIS, and VIIRS inputs are fed into ``run_clavrx.py``, which produces ``level2.hdf`` output files.

**GeoIPS Processing Stage:**

The ``level2.hdf`` files are read by the ``clavrx_hdf4`` reader, converted to xarray, processed through
the algorithm and colormapper modules, and formatted via the output formatter to produce PNG, GeoTIFF,
and netCDF outputs.

Quick Start Commands
===================

After installation, the four CLI wrapper scripts handle the full workflow:

.. code-block:: bash

    # Install the prebuilt CLAVR-x binary
    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py

    # Download static ancillary data (~410 GB)
    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py

    # Download dynamic ancillary data for a date
    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py --download_dtg YYYYMMDD

    # Run CLAVR-x on satellite input
    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py --input_files <files>

Outputs are written to ``$GEOIPS_OUTDIRS/preprocessed/clavrx/``.

Getting Started
===============

To begin using the CLAVR-x plugin, follow the installation guide:

- :doc:`Installation on Linux with conda <../installing/linux_with_conda>`
- :doc:`Installation on macOS with conda <../installing/mac_with_conda>`
- :doc:`Troubleshooting common issues <../installing/troubleshooting>`
