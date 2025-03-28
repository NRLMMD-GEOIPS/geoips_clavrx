# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

# download ancillary data
python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/ancillary/update_dynamic.py 20240606

# run test
python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/test/test_clavrx.py -i AHI

# run geoips tests
# NOTE add compare_path back in after we either update the image comparisons to be less
# strict, and/or grab a fixed set of dynamic ancillary data so the images actually match
# 100%.  For now, just ensure processing completes successfully, but do not compare the
# actual output imagery
#     --compare_path "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/outputs/ahi.clavrx.<product>.imagery_clean" \
run_procflow \
    $GEOIPS_OUTDIRS/clavrx_products/testing/ahi/*.hdf \
    --procflow single_source \
    --reader_name clavrx_hdf4 \
    --product_name Cloud-Fraction \
    --output_formatter imagery_clean \
    --minimum_coverage 0 \
    --sector_list himawari


retval=$?

exit $retval
