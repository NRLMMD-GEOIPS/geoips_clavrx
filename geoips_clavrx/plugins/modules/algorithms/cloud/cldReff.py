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
"""CLAVR-x Cloud Particles Product Processing."""

# Python Standard Libraries
import logging

alg_func_type = "xarray_to_numpy"

log = logging.getLogger(__name__)


def cldReff(xobj, output_data_range=None):
    """CLAVR-x Cloud Particles Product Processing.

    It is designed for effective radius of Cloud particles product from AHI or
    ABI cloud property data files.

    Note: Temp is only available where cloud exists.  cllud clear pixels are
    masked out

    Get the appropriate variable name map for the input data file based on
    sensor name

    output_data_range values are set in cldReff.yaml
    """
    # Gather variables
    cldReff_min = output_data_range[0]
    cldReff_max = output_data_range[1]
    cldReff = xobj["cld_reff_acha"].to_masked_array()  # select cloud top temp variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldReff,
        min_val=cldReff_min,
        max_val=cldReff_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
