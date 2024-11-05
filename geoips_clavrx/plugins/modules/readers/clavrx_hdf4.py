# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""
CLAVR-x hdf4 cloud property data reader.

S.Yang:  1/19/2023
"""

import logging
from datetime import datetime, timedelta

import numpy as np
import xarray as xr

from geoips.interfaces import readers
from geoips.utils.context_managers import import_optional_dependencies

LOG = logging.getLogger(__name__)

with import_optional_dependencies(loglevel="info"):
    """Attempt to import a package and print to LOG.info if the import fails."""
    from pyhdf.error import HDF4Error
    from pyhdf.SD import SD, SDC

interface = "readers"
family = "standard"
name = "clavrx_hdf4"


SCALED_ATTRIB = "SCALED"
SCALE_FACTOR_ATTRIB = "scale_factor"
ADD_OFFSET_ATTRIB = "add_offset"
SCALED_FLAG = 1

SCALING_ATTRIBS = [
    SCALED_ATTRIB,
    SCALE_FACTOR_ATTRIB,
    ADD_OFFSET_ATTRIB,
]


def parse_metadata(metadata_in):
    """Parse metadata."""
    metadata = dict(metadata_in)

    # Map GOES-RU-IMAGER to "abi" GeoIPS sensor name
    if metadata["sensor"] == "GOES-RU-IMAGER":
        metadata["sensor"] = "abi"

    return metadata


def year_day_hours_to_datetime(year, day, time):
    return datetime(year, 1, 1) + timedelta(days=day, hours=time)


def read_cloudprops(fname, chans=None, metadata_only=False):
    """Read CLAVR-x Cloud Properties Data.



    Returns:

    A dictionary containing an xArray Dataset of cloud observation data with
    variables under key "DATA":
        - 'latitude': Latitude.
        - 'longitude': Longitude.
        - 'cloud_type': Cloud type.
        - 'cloud_mask': Cloud mask.
        - 'cloud_phase': Cloud phase.
        - 'cloud_fraction': Cloud fraction.
        - 'cld_height_acha': Cloud height.
        - 'cld_height_base_acha': Base cloud height.
        - 'cld_height_top_acha': Top cloud height.
        - 'cld_temp_acha': Cloud temperature.
        - 'cloud_water_path': Cloud water path.
        - 'cld_opd_acha': Cloud optical depth.
        - 'cld_reff_acha': Effective cloud particle radius.
        - 'temp_3_75um_nom': Brightness temperature at 3.75 µm.
        - 'temp_11_0um_nom': Brightness temperature at 11.0 µm.
        - 'solar_zenith_angle': Solar zenith angle.

    Note:
        Values of the attribute 'valid_range' for 'cloud_type', 'cloud_mask',
        and possibly 'cloud_phase' are not valid. They should be specified
        with their definitions; this code does so for 'cloud_type' and 'cloud_mask'.
    """
    data = SD(str(fname), SDC.READ)
    return_dataset = xr.Dataset()

    data_metadata = parse_metadata(data.attributes())

    # carry along all provided metadata to output dataset
    for metadata_attr, metadata_attr_value in data_metadata.items():
        return_dataset.attrs[metadata_attr] = metadata_attr_value

    # Set human readable start/end times
    for period in ["start", "end"]:
        return_dataset.attrs[period + "_datetime"] = year_day_hours_to_datetime(
            data_metadata[period.upper() + "_YEAR"],
            data_metadata[period.upper() + "_DAY"],
            data_metadata[period.upper() + "_TIME"],
        )
    return_dataset.attrs["source_name"] = "clavrx"
    return_dataset.attrs["platform_name"] = data_metadata["platform"].lower()
    return_dataset.attrs["data_provider"] = "CIRA"
    return_dataset.attrs["source_file_names"] = data_metadata["FILENAME"]
    return_dataset.attrs["sample_distance_km"] = data_metadata["RESOLUTION_KM"]  # 2km
    return_dataset.attrs["interpolation_radius_of_influence"] = 3000  # 3km

    # process of all variables
    if metadata_only:
        LOG.debug("metadata_only requested, returning without reading data")
        return return_dataset

    if chans is None:
        var_names = sorted(data.datasets().keys())
    else:
        var_names = chans

    for var in var_names:
        try:
            attrs = data.select(var).attributes()
            data_get = data.select(var).get()
        except HDF4Error as e:
            LOG.critical(f"Dataset '{var}' does not exist in file '{fname}'")
            raise e

        # mask grids with missing or bad values
        limit1 = attrs["valid_range"][0]
        limit2 = attrs["valid_range"][1]
        if var == "cloud_type":
            limit1 = 0
            limit2 = 13
        if var == "cloud_mask":
            limit1 = 0
            limit2 = 3
        data_get_mask = np.ma.masked_outside(data_get, limit1, limit2, copy=True)
        # convert the scaled/ofset values into the actual values
        data_get_actualvalue = (
            data_get_mask * attrs["scale_factor"] + attrs["add_offset"]
        )
        return_dataset[var] = xr.DataArray(data_get_actualvalue, attrs=attrs)

    return return_dataset


def _is_var_scaled(attrs: Dict[str, Any]) -> bool:
    return SCALED_ATTRIB in attrs and attrs[SCALED_ATTRIB] == SCALED_FLAG


def _scaling_attributes_removed(attrs: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in attrs.items() if k not in SCALING_ATTRIBS}


def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    """Read CLAVR-x hdf4 cloud properties for one or more files.

    Parameters
    ----------
    fnames : list
        * List of strings, full paths to files
    metadata_only : bool, default=False
        * NOT YET IMPLEMENTED
        * Return before actually reading data if True
    chans : list of str, default=None
        * NOT YET IMPLEMENTED
        * List of desired channels (skip unneeded variables as needed).
        * Include all channels if None.
    area_def : pyresample.AreaDefinition, default=None
        * NOT YET IMPLEMENTED
        * Specify region to read
        * Read all data if None.
    self_register : str or bool, default=False
        * NOT YET IMPLEMENTED
        * register all data to the specified dataset id (as specified in the
          return dictionary keys).
        * Read multiple resolutions of data if False.

    Returns
    -------
    dict of xarray.Datasets
        * dictionary of xarray.Dataset objects with required Variables and
          Attributes.
        * Dictionary keys can be any descriptive dataset ids.

    See Also
    --------
    :ref:`xarray_standards`
        Additional information regarding required attributes and variables
        for GeoIPS-formatted xarray Datasets.
    """
    return readers.read_data_to_xarray_dict(
        fnames,
        _call_single_time,
        metadata_only,
        chans,
        area_def,
        self_register,
    )


def _call_single_time(
    fnames, metadata_only=False, chans=None, area_def=None, self_register=False
):
    """Read CLAVR-x hdf4 cloud properties for one file.

    Parameters
    ----------
    fnames : list
        * List of strings, full paths to files
    metadata_only : bool, default=False
        * NOT YET IMPLEMENTED
        * Return before actually reading data if True
    chans : list of str, default=None
        * NOT YET IMPLEMENTED
        * List of desired channels (skip unneeded variables as needed).
        * Include all channels if None.
    area_def : pyresample.AreaDefinition, default=None
        * NOT YET IMPLEMENTED
        * Specify region to read
        * Read all data if None.
    self_register : str or bool, default=False
        * NOT YET IMPLEMENTED
        * register all data to the specified dataset id (as specified in the
          return dictionary keys).
        * Read multiple resolutions of data if False.

    Returns
    -------
    dict of xarray.Datasets
        * dictionary of xarray.Dataset objects with required Variables and
          Attributes.
        * Dictionary keys can be any descriptive dataset ids.

    See Also
    --------
    :ref:`xarray_standards`
        Additional information regarding required attributes and variables
        for GeoIPS-formatted xarray Datasets.
    """
    print("Running call_single_time")
    if not area_def == False:
        logging.warning(
            f"area_def is set to a non-default value: {area_def},"
            "\n"
            "but area_def's value doesn't affect the behaviour of"
            "clavrx"
        )  # TODO add note ab what area_def _could_ do
    if not self_register == False:
        logging.warning(
            f"self_register is set to a non-default value: {self_register},"
            "\n"
            "but self_register's value doesn't affect the behaviour of"
            "clavrx"
        )
    fname = fnames[0]
    xarrays = read_cloudprops(fname, chans=chans, metadata_only=metadata_only)
    return {"DATA": xarrays, "METADATA": xarrays[[]]}


def get_test_files(test_data_dir):
    """Return test xarray and files for unit testing."""
    import os

    test_file = os.path.join(
        test_data_dir,
        "test_data_clavrx",
        "data",
        "himawari9_2023101_0300",
        "clavrx_H09_20230411_0300_B01_FLDK_DK_R10_S0110.DAT.level2.hdf",
    )
    return call([test_file])


def get_test_parameters():
    """Get test data key and a variable to test."""
    return [{"data_key": "DATA", "data_var": "cld_height_acha"}]
