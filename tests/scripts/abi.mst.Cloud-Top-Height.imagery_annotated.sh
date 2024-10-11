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

geoips run single_source $GEOIPS_TESTDATA_DIR/reader_tests/data/clavrx/goes16/2024283.1500.1510/*.hdf \
    --reader_name clavrx_hdf4 \
    --product_name Absdiff-Cloud-Top-Height \
    --output_formatter imagery_annotated \
    --minimum_coverage 0 \
    --sector_list goes_east
retval=$?

exit $retval
