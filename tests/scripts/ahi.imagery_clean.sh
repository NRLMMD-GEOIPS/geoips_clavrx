# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

script_dir=`dirname $0`
output_dir=$script_dir/../outputs

product_name=$1

if [[ "$1" == "" ]]; then
    echo "Usage: $0 [product_name]"
    exit 1
fi

geoips run single_source \
    $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/himawari9_2023101_0300/clavrx_H09_20230411_0300_B01_FLDK_DK_R10_S0110.DAT.level2.hdf \
    --reader_name clavrx_hdf4 \
    --product_name $product_name \
    --output_formatter imagery_clean \
    --compare_path "$output_dir/ahi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list test_himawari_eqc_3km_landocean
retval=$?

exit $retval
