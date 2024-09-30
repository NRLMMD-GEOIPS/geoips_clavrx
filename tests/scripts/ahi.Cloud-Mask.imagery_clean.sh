# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

script_dir=`dirname $0`
output_dir=$script_dir/../outputs

run_procflow $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/himawari9_2023101_0300/clavrx_H09_20230411_0300_B01_FLDK_DK_R10_S0110.DAT.level2.hdf \
    --procflow single_source \
    --reader_name clavrx_hdf4 \
    --product_name Cloud-Mask \
    --output_formatter imagery_clean \
    --compare_path "$output_dir/ahi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list himawari
retval=$?

exit $retval
