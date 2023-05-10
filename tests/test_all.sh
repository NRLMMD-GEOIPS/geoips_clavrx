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

# Please identify and update all instances of "@" found in this script appropriately.
# You will need to generate one or more test scripts that test your complete functionality,
# (these scripts provide example geoips calls and sample output, as well as providing a full integration test),
# and call each script within the test_all.sh script.  Do not rename this script or test directory - automated
# integrations tests look for the tests/test_all.sh script for complete testing.

#!/bin/bash

# This should contain test calls to cover ALL required functionality tests for the @package@ repo.

# The $GEOIPS tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall return value,
   # calling the test scripts appropriately, and 
   # setting the final return value.

# Note you must use the variable "call" in the for the loop

# Argument to test_all_pre.sh ONLY sets the prefix on the log output / filenames.
# Used for clarity, and to differentiate potentially multiple "test_all.sh" scripts in the same repo.
. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh geoips_clavrx

echo ""
# "call" used in test_all_run.sh
for call in \
\
    "$GEOIPS_PACKAGES_DIR/geoips/tests/utils/check_code.sh all `dirname $0`/../" \
    "test_interfaces" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi_cldFraction.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldFraction.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldHeightBase.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldHeight.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldHeightTop.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldMask.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldOpd.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldPhase.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldReff.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldTemp.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_cldType.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_Temp11p0.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi_Temp3p75.sh"
do
    . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
