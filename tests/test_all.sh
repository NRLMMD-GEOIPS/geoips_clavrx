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
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/abi.Cloud-Fraction.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Fraction.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Top-Height.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Base-Height.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Maske.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Optical-Depth.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Phase.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Effective-Radius.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Temp-ACHA.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Cloud-Type.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Temp-11p0.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/ahi.Temp-3p75.imagery_clean.sh"
do
    . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
