# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""CLAVR-x NetCDF4 Reader."""

from datetime import datetime, timedelta

import logging

import xarray as xr

LOG = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "clavrx_netcdf4"


def year_day_hours_to_datetime(year, day, time):
    """Convert year, day, and time to a datetime object.

    Parameters
    ----------
    year : int
        The year.
    day : int
        Day of the year (1-366).
    time : float
        Time in hours.

    Returns
    -------
    datetime: datetime.datetime
    """
    date = datetime(year, 1, 1) + timedelta(days=day, hours=time) - timedelta(days=1)
    if date.microsecond >= 500000:
        date = date + timedelta(seconds=1)
    return date.replace(microsecond=0)


def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    """CLAVR-x NetCDF4 reader."""
    LOG.info("Reading clavrx-netcdf4 data.")
    metadata_dict = {}
    xr_list = []
    for fn in fnames:
        tmp_xr = xr.open_dataset(fn)

        for period in ("start", "end"):
            metadata_dict[period + "_datetime"] = year_day_hours_to_datetime(
                int(tmp_xr.attrs[period.upper() + "_YEAR"]),
                int(tmp_xr.attrs[period.upper() + "_DAY"]),
                float(tmp_xr.attrs[period.upper() + "_TIME"]),
            )
        # translate cooridnates
        metadata_dict["source_name"] = "clavrx"
        metadata_dict["platform_name"] = tmp_xr.attrs["platform"].lower()
        metadata_dict["data_provider"] = "cira"
        metadata_dict["source_file_names"] = tmp_xr.attrs["FILENAME"]
        metadata_dict["sample_distance_km"] = tmp_xr.attrs["RESOLUTION_KM"]  # 2km
        metadata_dict["interpolation_radius_of_influence"] = 3000  # 3km
        if len(fnames) == 1 and metadata_only:
            return {"METADATA": xr.Dataset(attrs=metadata_dict)}

        tmp_xr.attrs |= metadata_dict
        xr_list.append(tmp_xr)

    # merge dataset
    if len(fnames) > 1:
        full_xr = xr.concat(xr_list, dim="scan_lines_along_track_direction")
    else:
        full_xr = xr_list[0]
    full_dict = {"DATA": full_xr, "METADATA": xr.Dataset(attrs=metadata_dict)}
    return full_dict
