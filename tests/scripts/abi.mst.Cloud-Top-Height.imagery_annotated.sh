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

#!/bin/bash

geoips run single_source $GEOIPS_PACKAGES_DIR/test_data_clavrx/data/goes16_2024283_1501_1506/*.hdf \
    --reader_name clavrx_hdf4 \
    --product_name Absdiff-Cloud-Top-Height \
    --output_formatter imagery_annotated \
    --minimum_coverage 0 \
    --sector_list conus
retval=$?

exit $retval
