# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

script_dir=`dirname $0`
output_dir=$script_dir/../outputs

run_procflow \
    $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/goes16_2023101_1600/clavrx_OR_ABI-L1b-RadF-M6C01_G16_s20231011600207.level2.hdf \
    --procflow single_source \
    --reader_name clavrx_hdf4 \
    --product_name Cloud-Fraction \
    --output_formatter imagery_clean \
    --compare_path "$output_dir/abi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list goes_east
retval=$?

exit $retval
