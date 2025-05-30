#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# This should contain test calls to cover ALL required functionality tests for
# this repo.

# The $GEOIPS_PACKAGES_DIR/geoips tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall
   #   return value,
   # calling the test scripts appropriately, and
   # setting the final return value.

if [[ ! -d $GEOIPS_PACKAGES_DIR/geoips ]]; then
    echo "Must CLONE geoips repository into \$GEOIPS_PACKAGES_DIR location"
    echo "to use test_all.sh testing utility."
    echo ""
    echo "export GEOIPS_PACKAGES_DIR=<path_to_geoips_cloned_packages>"
    echo "git clone https://github.com/NRLMMD-GEOIPS/geoips $GEOIPS_PACKAGES_DIR/geoips"
    echo ""
    exit 1
fi

repopath=`dirname $0`/../
pkgname=geoips_clavrx_build
# Argument to test_all_pre.sh ONLY sets the prefix on the log output / filenames.
# Used for clarity, and to differentiate potentially multiple "test_all.sh" scripts
# in the same repo.
. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh $pkgname

echo ""
# Note you must use the variable "call" in the for the loop
# "call" used in test_all_run.sh
for call in \
\
  "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi.clavrx_proc.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.clavrx_proc.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/modis.clavrx_proc.sh" \
  "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/viirs.clavrx_proc.sh"
do
  . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
