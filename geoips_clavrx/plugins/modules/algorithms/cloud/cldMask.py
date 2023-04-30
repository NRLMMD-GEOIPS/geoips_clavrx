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
"""CLAVR-x Cloud Mask Processing."""

# Python Standard Libraries
import logging

alg_func_type = "xarray_to_numpy"

log = logging.getLogger(__name__)


def cldMask(xobj, output_data_range=None):
    """CLAVR-x Cloud Mask Processing.

    It is designed for Cloud Mask product from AHI or ABI cloud property
    data files.

    Get the appropriate variable names for the input data file based on
    sensor name

    output_data_range values are set in cldMask.yaml

    CldMask=0(clear),1(probably clear),2(probably cloudy ),3(cloudy)
    """
    # Gather variables

    cldType_min = output_data_range[0]
    cldType_max = output_data_range[1]
    cldType = xobj["cloud_mask"].to_masked_array()  # select cloud type variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldType,
        min_val=cldType_min,
        max_val=cldType_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
