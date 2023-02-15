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

run_procflow $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/himawari8_20201201_0900/clavrx_H08_202012010900.level2.hdf \
    --procflow single_source \
    --reader_name clavrx_hdf4 \
    --product_name cldMask \
    --output_format imagery_clean \
    --compare_path "$output_dir/ahi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list himawari8 \
    --sectorfiles $GEOIPS_PACKAGES_DIR/geoips/tests/sectors/static/himawari8.yaml
retval=$?

exit $retval
