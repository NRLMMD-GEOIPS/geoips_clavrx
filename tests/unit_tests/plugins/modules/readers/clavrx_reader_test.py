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

import pytest
from geoips.commandline.log_setup import setup_logging
from geoips_clavrx.plugins.modules.readers import clavrx_hdf4
from geoips_clavrx.plugins.modules.readers import clavrx_netcdf4


LOG = setup_logging()


class TestClavrxReader:
    """Tests all clavrx readers for GEOIPS xarray conformity."""

    available_readers = [
        (clavrx_hdf4),
        (clavrx_netcdf4),
    ]

    def verify_plugin(self, plugin):
        """Yeild test xarray and parameters."""
        test_xr = plugin.yeild_test_files()
        self.verify_xarray(test_xr)

    def verify_xarray(self, inxr):
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

    @pytest.mark.parametrize("reader", available_readers)
    def test_standards(self, reader):
        """Unit test clavrx reader plugins, yeild xfail for no unit modules."""
        if not hasattr(reader, "yeild_test_files"):
            pytest.xfail(str(reader) + " has no test modules")
        self.verify_plugin(reader)
