# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/
"""CLAVR-x Cloud Optical Depth Processing."""

# Python Standard Libraries
import logging

interface = "algorithms"
family = "xarray_to_numpy"
name = "cldOpd"

log = logging.getLogger(__name__)


def call(xobj, output_data_range=None):
    """CLAVR-x Cloud Optical Depth Processing.

    It is designed for Cloud OPD(cloud optical depth at 0.65 um)
    product from AHI or ABI cloud property data files.

    Get the appropriate variable name map for the input data file based on
    sensor name.

    output_data_range values are set in cldOpd.yaml (-0.2 - 8)
    opd unit=?
    """
    # Gather variables

    cldOpd_min = output_data_range[0]
    cldOpd_max = output_data_range[1]
    cldOpd = xobj["cld_opd_acha"].to_masked_array()  # select cloud type variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldOpd,
        min_val=cldOpd_min,
        max_val=cldOpd_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
