# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

#!/bin/bash

if [[ "$1" == "install_clavrx" ]]; then
    if [[ "$2" == "" ]]; then
        echo "Must pass path to rttov tar file."
        echo "Please see geoips_clavrx/README.md for information on obtaining rttov."
        exit 1
    elif [[ ! -e $2 ]]; then
        echo "Must pass path to valid rttov tar file."
        echo "$2 does not exist."
        echo "Please see geoips_clavrx/README.md for information on obtaining rttov."
        exit 1
    fi

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py --rttov_tar $2
    

elif [[ "$1" == "install_ancillary_data" ]]; then
    # download ancillary data files and put them in appropriate directories
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/static
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/dynamic
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/dynamic/gfs
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/dynamic/snow/hires
    year=$(date +%Y)
    mkdir -p $GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/dynamic/oisst_nc/$year

    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/ancillary/ancil_data.py

elif [[ "$1" == "test_clavrx_install" ]]; then
    # check if clavrx has been installed, 
    # then check if ancillary data has been installed, then...
    if [[ -f "$GEOIPS_DEPENDENCIES_DIR/clavrx/CLAVRx/run/bin/clavrxorb" && -d "$GEOIPS_DEPENDENCIES_DIR/clavrx/ancillary/" ]]; then
        python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/test/test_clavrx.py

        # $GEOIPS_DEPENDENCIES_DIR/clavrx/CLAVRx/run/run_clavrxorb
    else
        echo "Must install CLAVRx as well as the required ancillary data first."
        echo "run sh setup.sh install_clavrx '/path/to/rttov_tar_file' "
        echo "run sh setup.sh install_ancillary_data"
        exit 1
    fi
    # else: install clavrx first
else
    echo "Pass one of install_clavrx, install_ancillary_data, or test_clavrx_install"
    echo "You passed:"
    echo "    $0 $@"
    exit 1
fi
