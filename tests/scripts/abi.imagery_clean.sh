# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

script_dir=`dirname $0`
output_dir=$script_dir/../outputs

if [[ "$1" == "" ]]; then
    echo "Usage: $0 [product_name]"
    exit 1
fi

product_name=$1

geoips run single_source \
    $GEOIPS_TESTDATA_DIR/test_data_clavrx/data/goes16_20230113_0000/clavrx_goes16_20230113000020.level2.hdf \
    --reader_name clavrx_hdf4 \
    --product_name $product_name \
    --output_formatter imagery_clean \
    --compare_path "$output_dir/abi.<product>.imagery_clean" \
    --minimum_coverage 0 \
    --sector_list test_goeseast_eqc_3km_landocean
retval=$?

exit $retval
