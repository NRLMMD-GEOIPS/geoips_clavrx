 | # # # Distribution Statement A. Approved for public release. Distribution unlimited.
 | # # #
 | # # # Author:
 | # # # Naval Research Laboratory, Marine Meteorology Division
 | # # #
 | # # # This program is free software: you can redistribute it and/or modify it under
 | # # # the terms of the NRLMMD License included with this program. This program is
 | # # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
 | # # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
 | # # # for more details. If you did not receive the license, for more information see:
 | # # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

Please see geoips/CHANGELOG_TEMPLATE.rst for instructions on updating
CHANGELOG appropriately with each PR

Release notes for previous/upcoming versions can be found in docs/source/releases,
for reference.

Breaking Changes
================

Update interface naming and move to plugins directory
-------------------------------------------------

*From issue GEOIPS/geoips_clavrx#4: 2023-04-25*

* Moved interface_modules to plugins/modules

  * Updated entry points
* Renamed output_format to output_formatter
* Renamed user_colormaps to colormaps

::

    moved: geoips_clavrx/interface_modules -> geoips_clavrx/plugins/modules
    modified: tests/scripts/*
    renamed: geoips_clavrx/plugins/modules/user_colormaps -> geoips_clavrx/plugins/modules/colormaps