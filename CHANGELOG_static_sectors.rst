Pre Version 1.10.0a12 (2023-05-02)
**********************************

* Removed sectorfiles argument from all test scripts.
* Added missing docstring to init file.

Breaking Changes
================

Removed sectorfiles argument from all test scripts
--------------------------------------------------

No longer require explicit path to YAML sector files - pass
only sector_list, since sectors are now fully fledged plugins.

::

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

