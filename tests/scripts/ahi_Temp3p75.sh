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

script_dir=`dirname $0`
output_dir=$script_dir/../outputs

run_procflow $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/himawari9_2023101_0300/clavrx_H09_20230411_0300_B01_FLDK_DK_R10_S0110.DAT.level2.hdf \
    --procflow single_source \
    --reader_name clavrx_hdf4 \
    --product_name Temp3p75 \
    --output_formatter imagery_clean \
    --compare_path "$output_dir/ahi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list himawari8
retval=$?

exit $retval
