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


def parse_metadata(metadata_in):
    """Parse metadata."""
    metadata = dict(metadata_in)

    # Map GOES-RU-IMAGER to "abi" GeoIPS sensor name
    if metadata["sensor"] == "GOES-RU-IMAGER":
        metadata["sensor"] = "abi"

    return metadata


def start_year_day_time_to_datetime(year, day, time):
    return datetime(year, 1, 1) + timedelta(days=day, hours=time)


#########################################################################
# READ CLAVR-x CLOUD PROPERTIES
#########################################################################


def read_cloudprops(fname, chans=None, metadata_only=False):
    """Read CLAVR-x Cloud Properties Data."""
    data = SD(str(fname), SDC.READ)  # read in all data fields

    # selected cloud variables
    # definiation of variables
    # cira_out = {'latitude':latitude, 'longitude':longitude,
    #     'cloud_type':cld_type,
    #     'cloud_mask':cld_mask,
    #     'cloud_phase':cld_phase,
    #     'cloud_fraction',cld_fract,
    #     'cld_height_acha':cld_hgt,
    #     'cld_height_base_acha':cld_hgt_base,
    #     'cld_height_top_acha':cld_hgt_top,
    #     'cld_temp_acha':cld_temp,
    #     'cloud_water_path':cwp,
    #     'cld_opd_acha':cld_opd,
    #     'cld_reff_acha':cld_reff,
    #     'temp_3_75um_nom',tb_3p75,
    #     'temp_11_0um_nom':tb_11p0,
    #     'solar_zenith_angle':sza}

    # Note:  Values of the attribute 'valid_range' for cloud_type, cloud_mask,
    #        cloud_phase(?) are not valid.
    #        They should be specified with their definitions.

    if chans is None:
        var_names = sorted(data.datasets().keys())
    else:
        var_names = chans

    # process of all variables
    xarrays = {}

    data_metadata = parse_metadata(data.attributes())

    xarrays = xr.Dataset()

    for period in ["start", "end"]:
        xarrays.attrs[period + "_datetime"] = start_year_day_time_to_datetime(
            data_metadata[period.upper() + "_YEAR"],
            data_metadata[period.upper() + "_DAY"],
            data_metadata[period.upper() + "_TIME"],
        )
    xarrays.attrs["source_name"] = "clavrx"
    xarrays.attrs["platform_name"] = data_metadata["platform"].lower()
    xarrays.attrs["data_provider"] = "CIRA"
    xarrays.attrs["source_file_names"] = data_metadata["FILENAME"]
    xarrays.attrs["sample_distance_km"] = data_metadata["RESOLUTION_KM"]  # 2km
    xarrays.attrs["interpolation_radius_of_influence"] = 3000  # 3km

    if metadata_only:
        LOG.info("metadata_only requested, returning without reading data")
        return xarrays

    for var in vars_sel:
        data_select = data.select(var)  # select this var
        attrs = data_select.attributes()  # get attributes for this var
        data_get = data_select.get()  # get all data of this var
        print(var, attrs)
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
        xarrays[var] = xr.DataArray(data_get_actualvalue, attrs=attrs)

    return xarrays


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
