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
"""CLAVR-x Cloud Phase Product Processing."""

# Python Standard Libraries
import logging

alg_func_type = "xarray_to_numpy"

log = logging.getLogger(__name__)


def cldPhase(xobj, output_data_range=None):
    """CLAVR-x Cloud Phase Product Process.

    It is designed for Cloud Phase product from AHI or ABI cloud property
    data files.

    Get the appropriate variable names for the input data file based on
    sensor name

    output_data_range values are set in cldPhase.yaml

    CldPhase=0(clear),1(water),2(supercooled),3(mixed),4(ice), 5(unknown)
    """
    # Gather variables

    cldPhase_min = output_data_range[0]
    cldPhase_max = output_data_range[1]
    cldPhase = xobj["cloud_phase"].to_masked_array()  # select cloud type variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldPhase,
        min_val=cldPhase_min,
        max_val=cldPhase_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
