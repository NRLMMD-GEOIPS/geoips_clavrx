 | # # # Distribution Statement A. Approved for public release. Distribution unlimited.
 | # # #
 | # # # Author:
 | # # # Naval Research Laboratory, Marine Meteorology Division
 | # # #
 | # # # This program is free software: you can redistribute it and/or modify it under
 | # # # the terms of the NRLMMD License included with this program. This program is
 | # # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
 | # # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
 | # # # for more details. If you did not receive the license, for more information see:
 | # # # https://github.com/U-S-NRL-Marine-Meteorology-Division/


Testing Updates
============

Update test outputs for all tests
--------------------------------

* The test files in test_data_clavrx were updated requiring that the comparison outputs also be updated

::
    new: tests/outputs/abi.cldFraction.imagery_clean/20230411.160200.goes-16.abi.cldFraction.goes16.71p70.cira.10p0.png
    new: tests/outputs/ahi.Temp11p0.imagery_clean/20230411.030000.him9.ahi.Temp11p0.himawari8.71p70.cira.10p0.png
    new: tests/outputs/ahi.Temp3p75.imagery_clean/20230411.030000.him9.ahi.Temp3p75.himawari8.71p70.cira.10p0.png
    new: tests/outputs/ahi.cldFraction.imagery_clean/20230411.030000.him9.ahi.cldFraction.himawari8.71p70.cira.10p0.png
    new: tests/outputs/ahi.cldHeight.imagery_clean/20230411.030000.him9.ahi.cldHeight.himawari8.48p00.cira.10p0.png
    new: tests/outputs/ahi.cldMask.imagery_clean/20230411.030000.him9.ahi.cldMask.himawari8.71p70.cira.10p0.png
    new: tests/outputs/ahi.cldOpd.imagery_clean/20230411.030000.him9.ahi.cldOpd.himawari8.69p44.cira.10p0.png
    new: tests/outputs/ahi.cldPhase.imagery_clean/20230411.030000.him9.ahi.cldPhase.himawari8.33p41.cira.10p0.png
    new: tests/outputs/ahi.cldReff.imagery_clean/20230411.030000.him9.ahi.cldReff.himawari8.48p00.cira.10p0.png
    new: tests/outputs/ahi.cldTemp.imagery_clean/20230411.030000.him9.ahi.cldTemp.himawari8.48p00.cira.10p0.png
    new: tests/outputs/ahi.cldType.imagery_clean/20230411.030000.him9.ahi.cldType.himawari8.71p70.cira.10p0.png
    deleted: tests/outputs/abi.cldFraction.imagery_clean/20230113.000000.goes-16.abi.cldFraction.goes16.63p31.cira.10p0.png
    deleted: tests/outputs/ahi.Temp11p0.imagery_clean/20201201.090000.him8.ahi.Temp11p0.himawari8.71p70.cira.10p0.png
    deleted: tests/outputs/ahi.Temp3p75.imagery_clean/20201201.090000.him8.ahi.Temp3p75.himawari8.71p70.cira.10p0.png
    deleted: tests/outputs/ahi.cldFraction.imagery_clean/20201201.090000.him8.ahi.cldFraction.himawari8.63p31.cira.10p0.png
    deleted: tests/outputs/ahi.cldHeight.imagery_clean/20201201.090000.him8.ahi.cldHeight.himawari8.45p74.cira.10p0.png
    deleted: tests/outputs/ahi.cldHeightBase.imagery_clean/20201201.090000.him8.ahi.cldHeightBase.himawari8.45p54.cira.10p0.png
    deleted: tests/outputs/ahi.cldMask.imagery_clean/20201201.090000.him8.ahi.cldMask.himawari8.63p31.cira.10p0.png
    deleted: tests/outputs/ahi.cldOpd.imagery_clean/20201201.090000.him8.ahi.cldOpd.himawari8.63p14.cira.10p0.png
    deleted: tests/outputs/ahi.cldPhase.imagery_clean/20201201.090000.him8.ahi.cldPhase.himawari8.26p72.cira.10p0.png
    deleted: tests/outputs/ahi.cldReff.imagery_clean/20201201.090000.him8.ahi.cldReff.himawari8.45p61.cira.10p0.png
    deleted: tests/outputs/ahi.cldTemp.imagery_clean/20201201.090000.him8.ahi.cldTemp.himawari8.45p74.cira.10p0.png
    deleted: tests/outputs/ahi.cldType.imagery_clean/20201201.090000.him8.ahi.cldType.himawari8.63p31.cira.10p0.png
    modified: tests/scripts/abi_cldFraction.sh
    modified: tests/scripts/ahi_Temp11p0.sh
    modified: tests/scripts/ahi_Temp3p75.sh
    modified: tests/scripts/ahi_cldFraction.sh
    modified: tests/scripts/ahi_cldHeight.sh
    modified: tests/scripts/ahi_cldHeightBase.sh
    modified: tests/scripts/ahi_cldHeightTop.sh
    modified: tests/scripts/ahi_cldMask.sh
    modified: tests/scripts/ahi_cldOpd.sh
    modified: tests/scripts/ahi_cldPhase.sh
    modified: tests/scripts/ahi_cldReff.sh
    modified: tests/scripts/ahi_cldTemp.sh
    modified: tests/scripts/ahi_cldType.sh

Code Formatting and Style Updates
=================================

Fix formatting in YAML files
---------------------------

::
    deleted: geoips_clavrx/yaml_configs/product_inputs/abi.yaml
    deleted: geoips_clavrx/yaml_configs/product_inputs/ahi.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/Temp11p0.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/Temp3p75.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldFraction.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldHeight.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldHeightBase.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldHeightTop.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldMask.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldOpd.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldPhase.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldReff.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldTemp.yaml
    deleted: geoips_clavrx/yaml_configs/product_params/cloud/cldType.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/Temp11p0.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/Temp3p75.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldFraction.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldHeight.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldHeightBase.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldHeightTop.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldMask.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldOpd.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldPhase.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldReff.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldTemp.yaml
    modified: geoips_clavrx/plugins/yaml/product_defaults/cloud/cldType.yaml
    modified: geoips_clavrx/plugins/yaml/products/abi.yaml
    modified: geoips_clavrx/plugins/yaml/products/ahi.yaml

