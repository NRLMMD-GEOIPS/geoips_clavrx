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
"""CLAVR-x Cloud Fraction Product."""

# Python Standard Libraries
import logging

log = logging.getLogger(__name__)

alg_func_type = "xarray_to_numpy"


def normalize(val, minval, maxval):
    """Normalize data."""
    val[val < minval] = minval
    val[val > maxval] = maxval
    val = (val - minval) / (maxval - minval)
    return val


def cldFraction(xobj, output_data_range=None):
    """Cloud Fraction Processing.

    It is designed for Cloud Fraction products from AHI or ABI cloud property
    data files.

    # Get the appropriate variable name map for the input data file based on
    sensor name output_data_range:  its values are set in cldFraction.yaml
    """
    # Gather variables

    cldFract_min = output_data_range[0]
    cldFract_max = output_data_range[1]
    cldFract = xobj[
        "cloud_fraction"
    ].to_masked_array()  # select cloud fraction variable

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        cldFract,
        min_val=cldFract_min,
        max_val=cldFract_max,
        min_outbounds="crop",
        max_outbounds="crop",
        norm=False,
        inverse=False,
    )

    return data
