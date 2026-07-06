# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

#######################################################################################
#######################################################################################
# Check for required environment variables for CLAVR-x tests.
#######################################################################################
#######################################################################################

# Allows running command and failing appropriately
geoips_check=". $GEOIPS_PACKAGES_DIR/geoips/setup/check_system_requirements.sh"

date -u

if [[ "$1" == *"help"* || -z $GEOIPS_ANCILDAT || -z $GEOIPS_OUTDIRS || -z $GEOIPS_PACKAGES_DIR || -z $GEOIPS_DEPENDENCIES_DIR || -z $GEOIPS_TESTDATA_DIR ]]; then
    echo ""
    echo "Must set the following environment variables for clavrx tests"
    echo ""
    echo "* GEOIPS_ANCILDAT - location for clavrx static and dynamic ancillary data sets."
    echo "                    Recommended this points to a shared directory, as clavrx ancillary data is quite large"
    echo "                    The geoips wrapper scripts 'get_ancildata_static.py' and 'update_ancildata_dynamic.py"
    echo "                    use GEOIPS_ANCILDAT/clavrx as the clavrx ancillary data location, and this test script expects the same location."
    echo "* GEOIPS_PACKAGES_DIR - for template clavrx configurations in geoips_clavrx repository"
    echo "* GEOIPS_DEPENDENCIES_DIR - for clavrx installation."
    echo "                    The geoips wrapper script 'install_clavrx.py' copies the"
    echo "                    pre-built clavrx executable into $GEOIPS_DEPENDENCIES_DIR/clavrx/run,"
    echo "                    and this test scripts expects the same location."
    echo "* GEOIPS_OUTDIRS - for clavrx and geoips outputs"
    echo "* GEOIPS_TESTDATA_DIR - for clavrx input test datasets"
    echo ""
    echo "********************************************************************************"
    echo "********************************************************************************"
    echo "***CLAVR-x processing through GeoIPS Processing Integration Test Script"
    echo "***Will run the following steps, expecting:"
    echo "    * the above environment variables are set"
    echo "    * CLAVR-x was installed using the geoips_clavrx/clavrx/install_clavrx.py utility"
    echo "********************************************************************************"
    echo "********************************************************************************"
    echo "################################################################################"
    echo "***Run install_clavrx.py to make sure clavrx executable is in the right place for geoips."
    echo "    python geoips_clavrx/clavrx/install_clavrx.py --validate_only --source_clavrx_prebuilt_clavrx_exec [arg] --dest_geoips_clavrx_exec [arg]"
    echo "***Remove expected CLAVR-x output and expected geoips output, if they exist, to ensure a clean run"
    echo "    rm -fv \$GEOIPS_OUTDIRS/preprocessed/clavrx/[clavrx_hdf4_file]"
    echo "    rm -fv \$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/[sector]/[sector]/[product]/clavrx/[geoips_png_file]"
    echo "***Static ancillary data check (will NOT download, will fail if it doesn't exist, and tell you how to get it)."
    echo "    python geoips_clavrx/clavrx/get_ancildata_static.py --[arguments]"
    echo "***Update dynamic ancillary data"
    echo "    python geoips_clavrx/clavrx/update_ancildata_dynamic.py --[arguments]"
    echo "***Run CLARV-x executable"
    echo "    python geoips_clavrx/clavrx/run_clavrx.py --[arguments]"
    echo "***Run GeoIPS"
    echo "    geoips run single_source [arguments]"
    echo "***Check for specific GeoIPS expected output"
    echo "    ls -l \$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/[sector]/[sector]/[product]/clavrx/[geoips_png_file]"
    echo "################################################################################"
    exit 1
fi

#######################################################################################
#######################################################################################
# Set variables based on the current data types, to be used in the common clavrx and
# geoips calls below
#######################################################################################
#######################################################################################

# Common arguments for all data types.  Using standard geoips installation locations
# for testing purposes.
# Currently tested gitlab build artifact
# previous stable binary version (CLAVR-x v2) was from job #117757
remote_clavrx_exec="https://gitlab.ssec.wisc.edu/clavrx/clavrx-dev/-/jobs/135947/artifacts/raw/run/bin/clavrxorb?inline=false"
ancillary_data_directory=$GEOIPS_ANCILDAT/clavrx
runtime_directory=$GEOIPS_OUTDIRS/scratch/clavrx_runtime
template_options_file=$GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/clavrx_options_template.toml
level2_list=$GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/level2_list
clavrx_output_directory=$GEOIPS_OUTDIRS/preprocessed/clavrx
clavrx_exec=$GEOIPS_DEPENDENCIES_DIR/clavrx/run_clavrxorb

# Sensor specific arguments, including expected clavrx and geoips output file paths
# for output validation.
if [[ "$1" == "ahi" ]]; then
    download_dtg=20240606
    # All 160 channel data files
    input_files=$GEOIPS_TESTDATA_DIR/test_data_clavrx/data/clavrx_input/ahi_h09_20240606/HS_H09_20240606_1210_*_FLDK_*_*.DAT
    sector_list=test_himawari_eqc_3km_landocean
    # This exact file should be produced.
    clavrx_output=$clavrx_output_directory/clavrx_H09_20240606_1210_B01_FLDK_DK_R10_S0110.DAT.level2.nc
    geoips_product="Cloud-Fraction"
    pseg_arg="--pseg"
    geoips_output=$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/Tests-x-Himawari/x-x-x/Cloud-Fraction/clavrx/20240606.121000.him9.clavrx.Cloud-Fraction.test_himawari_eqc_3km_landocean.100p00.cira.3p0.png
elif [[ "$1" == "abi" ]]; then
    download_dtg=20240606
    # All 16 channel data files
    input_files=$GEOIPS_TESTDATA_DIR/test_data_clavrx/data/clavrx_input/goes16_20240607/OR_ABI-L1b-RadF-M6C*_G16_s20241581200194_e20241581209*_c20241581209*.nc
    sector_list=test_goeseast_eqc_3km_landocean
    # This exact file should be produced.
    clavrx_output=$clavrx_output_directory/clavrx_OR_ABI-L1b-RadF-M6C01_G16_s20241581200194.level2.nc
    pseg_arg="--pseg"
    geoips_product="Cloud-Fraction"
    geoips_output=$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/Tests-x-Goes_East/x-x-x/Cloud-Fraction/clavrx/20240606.120019.goes-16.clavrx.Cloud-Fraction.test_goeseast_eqc_3km_landocean.100p00.cira.3p0.png
elif [[ "$1" == "modis" ]]; then
    download_dtg=20240607
    # MOD03 and MOD021KM
    input_files=$GEOIPS_TESTDATA_DIR/test_data_clavrx/data/clavrx_input/modis_20240607/MOD0*.A2024159.1300.061.2024159135*.NRT.hdf
    sector_list=australia
    # This exact file should be produced.
    clavrx_output=$clavrx_output_directory/clavrx_MOD021KM.A2024159.1300.061.2024159135957.NRT.level2.nc
    # Do not use pseg with viirs/modis since they do not take as long, so we are testing
    # both options.
    pseg_arg=""
    geoips_product="Cloud-Fraction"
    geoips_output=$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/Australia-x-Continental/x-x-x/Cloud-Fraction/clavrx/20240607.130000.terra.clavrx.Cloud-Fraction.australia.23p91.cira.2p0.png
elif [[ "$1" == "viirs" ]]; then
    download_dtg=20240720
    # 26 geolocation and data files
    input_files=$GEOIPS_TESTDATA_DIR/test_data_clavrx/data/clavrx_input/viirs_20240720/*_npp_d20240720_t1641384_e1647188_b65962_c20240723002*_cspp_dev.h5
    sector_list=w_pacific
    # This exact file should be produced.
    clavrx_output=$clavrx_output_directory/clavrx_npp_d20240720_t1641384_e1647188_b6596_b65962_c20240723002845007097_cspp_dev.h5.level2.nc
    # Do not use pseg with viirs/modis since they do not take as long, so we are testing
    # both options.
    pseg_arg=""
    geoips_product="Cloud-Temp-ACHA"
    # Note the coverage and the contents of this image changed slightly from CLAVR-x 2
    # to CLAVR-x 3.  We are unsure why (possibly due to PFAAST coordinate changes).
    geoips_output=$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/x-x-Western_Pacific/x-x-x/Cloud-Temp-ACHA/clavrx/20240720.164138.snpp.clavrx.Cloud-Temp-ACHA.w_pacific.11p55.cira.3p0.png
elif [[ "$1" == "fci" ]]; then
    download_dtg=20260315
    input_files=$GEOIPS_TESTDATA_DIR/test_data_clavrx/data/clavrx_input/fci_20260315/*nc 
    sector_list=meteosat_africa
    pseg_arg="--pseg"
    # pseg_arg=""
    # This exact file should be produced.
    clavrx_output=$clavrx_output_directory/clavrx_meteosat12_SAT%_CMT_2026_074_1600.level2.nc
    geoips_product="Cloud-Type"
    geoips_output=$GEOIPS_OUTDIRS/preprocessed/annotated_imagery/Africa-x-Meteosat-Africa/x-x-x/Cloud-Type/clavrx/20260315.160006.meteosat-12.clavrx.Cloud-Type.meteosat_africa.100p00.cira.3p0.png
else
    echo "Usage: $0 [instrument]"
    echo "Where instrument one of:"
    echo "  ahi"
    echo "  abi"
    echo "  modis"
    echo "  viirs"
    echo "  fci"
    exit 1
fi


#######################################################################################
#######################################################################################
# Compile and print to terminal all commands required for the complete test in advance.
#######################################################################################
#######################################################################################
# Run validate_only for clavrx executable, because we do not want to force the user
# to automatically overwrite their existing install.  Since we are using the same
# installation script to validate the installation, it will provide the exact command
# for installing properly (just remove --validate_only and run manually).
command_install_clavrx="python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py \
    --validate_only \
    --source_prebuilt_clavrx_exec $remote_clavrx_exec \
    --dest_geoips_clavrx_exec $clavrx_exec"
# Run validate_only for get_ancildata_static, because it is huge, and we do not want
# to force the user unknowingly to download half a terabyte of data. Since we are using
# the same installation script to validate the installation, it will provide the exact
# command for installing properly (just remove --validate_only and run manually, or
# manually link to an appropriate ancillary data location.).
command_validate_ancildata_static="python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py \
    --validate_only \
    --ancillary_data_directory $ancillary_data_directory"
command_update_ancildata_dynamic="python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py \
    --download_dtg $download_dtg \
    --ancillary_data_directory $ancillary_data_directory"
# Note run_clavrx.py automatically generates the files required by clavrx at
# runtime in the specified runtime directory, using the information passed in at the
# command line. run_clavrx.py --help for more information.
command_run_clavrx="python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py \
  --input_files $input_files \
  --runtime_directory $runtime_directory \
  $pseg_arg
  --template_options_file $template_options_file \
  --ancillary_data_directory $ancillary_data_directory \
  --level2_list $level2_list \
  --output_directory $clavrx_output_directory \
  --clavrx_exec $clavrx_exec"
# NOTE add compare_path back in after we either update the image comparisons to be less
# strict, and/or grab a fixed set of dynamic ancillary data so the images actually match
# 100%.  For now, just ensure processing completes successfully and the correct output
# file is produced, but do not compare the actual output imagery
#     --compare_path "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/outputs/ahi.clavrx.<product>.imagery_clean" \
command_run_geoips="geoips run single_source \
    $clavrx_output \
    --reader_name clavrx_netcdf4 \
    --product_name $geoips_product \
    --output_formatter imagery_clean \
    --minimum_coverage 0 \
    --sector_list $sector_list"

echo "********************************************************************************"
echo "********************************************************************************"
echo "***CLAVR-x processing through GeoIPS Processing Integration Test Script"
echo "***Will run the following steps:"
echo "********************************************************************************"
echo "********************************************************************************"
echo "################################################################################"
echo "***Install clavrx executable where GeoIPS can find it!"
echo $command_install_clavrx
echo "################################################################################"
echo "***Remove expected CLAVR-x output and expected geoips output, if they exist, to ensure a clean run"
echo rm -fv $clavrx_output
echo rm -fv $geoips_output
echo "################################################################################"
echo "***Static ancillary data check (will NOT download, will fail if it doesn't exist, and tell you how to get it)."
echo $command_validate_ancildata_static
echo "################################################################################"
echo "***Update dynamic ancillary data"
echo $command_update_ancildata_dynamic
echo "################################################################################"
echo "***Run CLARV-x executable"
echo "$command_run_clavrx"
echo "################################################################################"
echo "***Run GeoIPS"
echo "$command_run_geoips"
echo "################################################################################"
echo "***Check for specific GeoIPS expected output"
echo "ls $geoips_output"
echo "################################################################################"
echo "################################################################################"

#######################################################################################
#######################################################################################
# Common test calls for all data types, using the variables set above.
#######################################################################################
#######################################################################################

echo "********************************************************************************"
echo "********************************************************************************"
echo "***Starting Processing"
echo "********************************************************************************"
echo "********************************************************************************"
echo "################################################################################"
echo "***Install clavrx executable where GeoIPS can find it!"
date -u
$geoips_check run_command "$command_install_clavrx" no_logfile_redirect
echo "################################################################################"
echo "Removing expected clavrx output and expected geoips output, if they exist, to ensure a clean test."
date -u
echo rm -fv $clavrx_output
echo rm -fv $geoips_output
rm -fv $clavrx_output
rm -fv $geoips_output
echo "################################################################################"

echo "################################################################################"
echo "Running static ancillary data check."
date -u
# This will print the command to terminal and exit 1 if the command fails.
$geoips_check run_command "$command_validate_ancildata_static" no_logfile_redirect
echo "################################################################################"

echo "################################################################################"
echo "Running dynamic ancillary data update"
date -u
# This will print the command to terminal and exit 1 if the command fails.
$geoips_check run_command "$command_update_ancildata_dynamic" no_logfile_redirect
echo "################################################################################"

echo "################################################################################"
echo "Running clavrx!"
date -u
# This will print the command to terminal and exit 1 if the command fails.
$geoips_check run_command "$command_run_clavrx" no_logfile_redirect
echo "################################################################################"

echo "################################################################################"
echo "Running geoips on clavrx output!"
date -u
$geoips_check run_command "$command_run_geoips" no_logfile_redirect
echo "################################################################################"

echo "################################################################################"
echo "Checking for geoips outputs!"
date -u
ls -l $runtime_directory/*
ls -l $geoips_output
ls -l $clavrx_output
echo ""
if [[ -e $geoips_output ]]; then
    date -u
    echo "SUCCESS Expected geoips output exists, all clavrx and geoips tests passed!!"
    retval=0
else
    date -u
    echo "FAILED Expected geoips output does not exist!"
    echo "        Expected $geoips_output"
    retval=1
fi
echo "################################################################################"
date -u
exit $retval
