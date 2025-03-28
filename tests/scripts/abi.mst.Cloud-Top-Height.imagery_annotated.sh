# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

geoips run single_source $GEOIPS_TESTDATA_DIR/reader_tests/data/clavrx/goes16/2024283.1500.1510/*.hdf \
    --reader_name clavrx_hdf4 \
    --product_name Absdiff-Cloud-Top-Height \
    --output_formatter imagery_annotated \
    --minimum_coverage 0 \
    --sector_list goes_east
retval=$?

exit $retval
