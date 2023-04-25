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

#!/bin/env python
"""Cloud Type CLAVR-x Cloud Properties Product Processing."""

# Python Standard Libraries
import logging

alg_func_type = "xarray_to_numpy"

log = logging.getLogger(__name__)


def cldType(xobj, output_data_range=None):
    """Cloud Type CLAVR-x Cloud Properties Product Processing.

    It is designed for Cloud Type product from AHI or ABI cloud property
    data files.

    Get the appropriate variable name map for the input data file based on
    sensor name

    output_data_range values are set in cldType.yaml

    CldType=0(clear),1(probably clear),2(fog),3(water),
    4(supercooled water),5(mixed),6(opaque_ice),
    7(cirrus),8(overlapping),9(overshooting),10(unknown),
    11(dust),12(smoke),13(fire)
    """
    # Gather variables

    cldType_min = output_data_range[0]
    cldType_max = output_data_range[1]
    cldType = xobj["cloud_type"].to_masked_array()  # select cloud type variable

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
