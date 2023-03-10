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
"""3.75um Brightness Temperature CLAVR-x Product."""

# Python Standard Libraries
import logging

alg_func_type = "xarray_to_numpy"

log = logging.getLogger(__name__)


def Temp3p75(xobj, output_data_range=None):
    """3.75um Brightness Temperature CLAVR-x Product.

    It is designed for brightness temperature product at 3.75 um from AHI or
    ABI cloud property data files.

    Note: Temp is only available where cloud exists.  cllud clear pixels are
    masked out

    Get the appropriate variable name map for the input data file based on
    sensor name

    output_data_range values are set in cldTemp.yaml
    """
    # Gather variables
    Temp3p75_min = output_data_range[0]
    Temp3p75_max = output_data_range[1]
    Temp3p75 = xobj[
        "temp_3_75um_nom"
    ].to_masked_array()  # select cloud top temp variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        Temp3p75,
        min_val=Temp3p75_min,
        max_val=Temp3p75_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
