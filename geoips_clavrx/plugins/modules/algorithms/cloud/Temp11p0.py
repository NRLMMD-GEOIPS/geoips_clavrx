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
"""11um Brightness Temperature CLAVR-x Product."""

# Python Standard Libraries
import logging

interface = "algorithms"
family = "xarray_to_numpy"
name = "Temp11p0"

log = logging.getLogger(__name__)


def call(xobj, output_data_range=None):
    """11um Brightness Temperature CLAVR-x Product.

    It is designed for brightness temperature product at 3.75 um from AHI or
    ABI cloud property data files.

    Note: Temp is only available where cloud exists.  cllud clear pixels
    are masked out

    Get the appropriate variable name map for the input data file based on
    sensor name

    output_data_range values are set in cldTemp.yaml
    """
    # Gather variables
    Temp11p0_min = output_data_range[0]
    Temp11p0_max = output_data_range[1]
    Temp11p0 = xobj[
        "temp_11_0um_nom"
    ].to_masked_array()  # select cloud top temp variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        Temp11p0,
        min_val=Temp11p0_min,
        max_val=Temp11p0_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
