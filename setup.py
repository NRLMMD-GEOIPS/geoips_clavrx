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

# Please identify all instances of "@" within this file, and update appropriately.

"""Installation instructions for geoips_clavrx package."""

from os.path import realpath, join, dirname

import setuptools

# NOTE: VERSION file must contain ONLY the version number, no comments, etc.
# You may set the initial version to any value you desire, just update VERSION
# appropriately.
with open(
    join(dirname(realpath(__file__)), "VERSION"), encoding="utf-8"
) as version_file:
    version = version_file.read().strip()

# Info on Python package_data:
# https://setuptools.pypa.io/en/latest/userguide/datafiles.html
# Info on Python entry points:
# https://setuptools.pypa.io/en/latest/userguide/entry_point.html
setuptools.setup(
    name="geoips_clavrx",
    version=version,
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "geoips_clavrx": [
            "yaml_configs/*",
            "yaml_configs/*/*",
            "yaml_configs/*/*/*",
        ],
    },
    entry_points={
        "geoips.algorithms": [
            "cloud.cldFraction=geoips_clavrx.interface_modules.algorithms.cloud"
            ".cldFraction:cldFraction",
            "cloud.cldType=geoips_clavrx.interface_modules.algorithms.cloud.cldType"
            ":cldType",
            "cloud.cldMask=geoips_clavrx.interface_modules.algorithms.cloud.cldMask"
            ":cldMask",
            "cloud.cldHeightBase=geoips_clavrx.interface_modules.algorithms.cloud"
            ".cldHeightBase:cldHeightBase",
            "cloud.cldHeightTop=geoips_clavrx.interface_modules.algorithms.cloud"
            ".cldHeightTop:cldHeightTop",
            "cloud.cldHeight=geoips_clavrx.interface_modules.algorithms.cloud.cldHeight"
            ":cldHeight",
            "cloud.cldOpd=geoips_clavrx.interface_modules.algorithms.cloud.cldOpd"
            ":cldOpd",
            "cloud.cldPhase=geoips_clavrx.interface_modules.algorithms.cloud.cldPhase"
            ":cldPhase",
            "cloud.cldTemp=geoips_clavrx.interface_modules.algorithms.cloud.cldTemp"
            ":cldTemp",
            "cloud.Temp3p75=geoips_clavrx.interface_modules.algorithms.cloud.Temp3p75"
            ":Temp3p75",
            "cloud.Temp11p0=geoips_clavrx.interface_modules.algorithms.cloud.Temp11p0"
            ":Temp11p0",
            "cloud.cldReff=geoips_clavrx.interface_modules.algorithms.cloud.cldReff"
            ":cldReff",
        ],
        "geoips.readers": [
            "clavrx_hdf4=geoips_clavrx.interface_modules.readers"
            ".clavrx_hdf4:clavrx_hdf4",
        ],
        "geoips.user_colormaps": [
            "cmap_cldFraction=geoips_clavrx.interface_modules.user_colormaps"
            ".cmap_cldFraction:cmap_cldFraction",
            "cmap_cldType=geoips_clavrx.interface_modules.user_colormaps.cmap_cldType"
            ":cmap_cldType",
            "cmap_cldMask=geoips_clavrx.interface_modules.user_colormaps.cmap_cldMask"
            ":cmap_cldMask",
            "cmap_cldHeightBase=geoips_clavrx.interface_modules.user_colormaps"
            ".cmap_cldHeightBase:cmap_cldHeightBase",
            "cmap_cldHeightTop=geoips_clavrx.interface_modules.user_colormaps"
            ".cmap_cldHeightTop:cmap_cldHeightTop",
            "cmap_cldHeight=geoips_clavrx.interface_modules.user_colormaps"
            ".cmap_cldHeight:cmap_cldHeight",
            "cmap_cldOpd=geoips_clavrx.interface_modules.user_colormaps.cmap_cldOpd"
            ":cmap_cldOpd",
            "cmap_cldPhase=geoips_clavrx.interface_modules.user_colormaps.cmap_cldPhase"
            ":cmap_cldPhase",
            "cmap_cldTemp=geoips_clavrx.interface_modules.user_colormaps.cmap_cldTemp"
            ":cmap_cldTemp",
            "cmap_IR=geoips_clavrx.interface_modules.user_colormaps.cmap_IR:cmap_IR",
            "cmap_cldReff=geoips_clavrx.interface_modules.user_colormaps.cmap_cldReff"
            ":cmap_cldReff",
        ],
    },
)
