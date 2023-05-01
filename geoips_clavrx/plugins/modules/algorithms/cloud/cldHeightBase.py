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
"""CLAVR-x Cloud Base Height Processing."""

# Python Standard Libraries
import logging

log = logging.getLogger(__name__)

interface = "algorithms"
family = "xarray_to_numpy"
name = "cldHeightBase"


def normalize(val, minval, maxval):
    """Normalize data."""
    val[val < minval] = minval
    val[val > maxval] = maxval
    val = (val - minval) / (maxval - minval)
    return val


def call(xobj, output_data_range=None):
    """ABI or AHI Cloud Height Base Cloud Property Processing.

    Designed for Cloud Height Base products from AHI or ABI cloud property data
    files. Cloud_Height_Base is defined as the height of a cloud bottom level
    (in unit of meters).

    Get the appropriate variable name map for the input data file based on
    sensor name. output_data_range values are set in cldHeightBase.yaml.
    """
    # Gather variables

    cldHeightBase_min = output_data_range[0]
    cldHeightBase_max = output_data_range[1]
    cldHeightBase = (
        xobj["cld_height_base_acha"].to_masked_array() / 1000.0
    )  # cloud height_base/convert to km)

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldHeightBase,
        min_val=cldHeightBase_min,
        max_val=cldHeightBase_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
