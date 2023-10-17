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

"""Test clarvx readers."""

import os
from glob import glob
import pytest
from geoips.commandline.log_setup import setup_logging
from geoips_clavrx.plugins.modules.readers import clavrx_hdf4
from geoips_clavrx.plugins.modules.readers import clavrx_netcdf4


LOG = setup_logging()


class TestClavrxReader:
    """Tests all clavrx readers for GEOIPS xarray conformity."""

    data_dir = os.environ["GEOIPS_TESTDATA_DIR"]
    available_readers = [
        (
            clavrx_hdf4,
            "/test_data_clavrx/data/himawari9_2023101_0300/\
clavrx_H09_20230411_0300_B01_FLDK_DK_R10_S0110.DAT.level2.hdf",
        ),
        (clavrx_netcdf4, ""),
    ]

    def check_xr(self, inxr):
        """Check for GEOIPS xarray conformity."""
        assert inxr
        assert inxr["DATA"].latitude.max()
        assert inxr["DATA"].latitude.min()
        assert inxr["DATA"].longitude.max()
        assert inxr["DATA"].longitude.min()
        assert inxr["METADATA"].attrs["source_name"]
        assert inxr["METADATA"].attrs["platform_name"]
        assert inxr["METADATA"].attrs["data_provider"]
        assert inxr["METADATA"].attrs["start_datetime"]
        assert inxr["METADATA"].attrs["end_datetime"]
        assert inxr["METADATA"].attrs["interpolation_radius_of_influence"]

    @pytest.mark.parametrize("key,files", available_readers)
    def test_standards(self, key, files):
        """Test all reader plugins, xfails for readers that don't have files.

        Parameters
        ----------
        key : string
           Reader plugin key
        files : string
           Wildcard path to data for reader

        Returns
        -------
        None
        """
        file_path = self.data_dir + files
        filelist = glob(file_path)
        if files == "" or len(filelist) == 0:
            pytest.xfail("No files given")

        inxr = key.call(filelist)
        self.check_xr(inxr)
