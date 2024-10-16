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

# v1.6.2: 2023-01-31, Initial release

# v1.6.1: 2022-12-29, Initial commit of CLAVR-x readers and output products
## GEOIPS#3: 2023-01-12, create geoips_clavrx repo
### Formatting Updates
* Applied black, flake8, and bandit defaults to existing code base.
### Major New Functionality
#### Top Level Administrivia
* **README.md**: standard README with repo cloning, optional geoips installation,
  and testing
* **CHANGELOG.md**: Initial CHANGELOG contents.
* **VERSION**: Required VERSION file
* **setup.py**: pip setup.py with package dependencies and entry points.
#### Testing
* **tests/test_all.sh**: Complete test script for full package integration tests
* **tests/scripts/**: Test script for each product (using full hdf4 data)
  * Single ABI test script
  * AHI test scripts for ALL products
* **tests/outputs/**: Test clean imagery output for each product
  * Single ABI test script
  * AHI test scripts for ALL products
#### Package modules
* **geoips_clavrx/interface_modules/readers/**: CLAVR-x hdf4 reader, for ABI and AHI
* **geoips_clavrx/interface_modules/algorithms/**: CLAVR-x products (apply ranges)
* **geoips_clavrx/interface_modules/user_colormaps/**: CLAVR-x colormaps
* **geoips_clavrx/yaml_configs/product_params/**: CLAVR-x product specs
* **geoips_clavrx/yaml_configs/product_inputs/ahi.yaml**: AHI CLAVR-x specs
```
new file: geoips_clavrx/interface_modules/readers/clavrx_hdf4.py
new file: geoips_clavrx/yaml_configs/product_inputs/abi.yaml
new file: tests/outputs/abi.cldFraction.imagery_clean/20230113.000000.goes-16.abi.cldFraction.goes16.63p31.cira.10p0.png
new file: tests/scripts/abi_cldFraction.sh
```

