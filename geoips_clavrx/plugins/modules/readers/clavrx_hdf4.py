# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""
CLAVR-x hdf4 cloud property data reader.

S.Yang:  1/19/2023
"""

import logging
from datetime import datetime

import numpy as np
import xarray as xr
from geoips.utils.context_managers import import_optional_dependencies

LOG = logging.getLogger(__name__)

with import_optional_dependencies(loglevel="info"):
    """Attempt to import a package and print to LOG.info if the import fails."""
    from pyhdf.error import HDF4Error
    from pyhdf.SD import SD, SDC

interface = "readers"
family = "standard"
name = "clavrx_hdf4"


def parse_metadata(metadatadict):
    """Parse metadata."""
    metadata = {}
    for ii in metadatadict.keys():
        metadata[ii] = metadatadict[ii]

    # Map GOES-RU-IMAGER to "abi" GeoIPS sensor name
    if metadata["sensor"] == "GOES-RU-IMAGER":
        metadata["sensor"] = "abi"

    return metadata


#########################################################################
# READ CLAVR-x CLOUD PROPERTIES
#########################################################################


def read_cloudprops(fname, chans=None, metadata_only=False):
    """Read CLAVR-x Cloud Properties Data."""
    try:
        data = SD(fname, SDC.READ)  # read in all data fields
    except HDF4Error:
        LOG.info("wrong input hdf file %s", fname)
        raise

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
        vars_sel = sorted(data.datasets().keys())
    elif chans:
        vars_sel = chans
    else:
        metadata_only = True

    # process of all variables
    xarrays = {}

    data_metadata = parse_metadata(data.attributes())

    # setup attributes
    # If start/end datetime happen to vary, adjust here.
    # start time
    syr = str(data_metadata["START_YEAR"])
    sjd = str(data_metadata["START_DAY"])
    shr = str(int(data_metadata["START_TIME"]))
    smin = str(int((data_metadata["START_TIME"] - int(shr)) * 60))
    ssec = str(int(((data_metadata["START_TIME"] - int(shr)) * 60 - int(smin)) * 60))
    # end time
    eyr = str(data_metadata["END_YEAR"])
    ejd = str(data_metadata["END_DAY"])
    ehr = str(int(data_metadata["END_TIME"]))
    emin = str(int((data_metadata["END_TIME"] - int(ehr)) * 60))
    esec = str(int(((data_metadata["END_TIME"] - int(ehr)) * 60 - int(emin)) * 60))

    sdt = datetime.strptime(syr + sjd + shr + smin + ssec, "%Y%j%H%M%S")
    edt = datetime.strptime(eyr + ejd + ehr + emin + esec, "%Y%j%H%M%S")

    xarrays = xr.Dataset()
    xarrays.attrs["start_datetime"] = sdt
    xarrays.attrs["end_datetime"] = edt
    xarrays.attrs["source_name"] = "clavrx"
    xarrays.attrs["platform_name"] = data_metadata["platform"].lower()
    xarrays.attrs["data_provider"] = "cira"
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
        xarrays[var] = xr.DataArray(data_get_actualvalue)

    return xarrays


def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    """Read CLAVR-x hdf4 cloud properties."""
    if not self_register == False:
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
    if len(fnames) > 1:
        logging.warning(
            "More than one filename passed to CLAV-RX reader, "
            "but reader only supports one file at a time. "
            "Operating on first file passed."
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
