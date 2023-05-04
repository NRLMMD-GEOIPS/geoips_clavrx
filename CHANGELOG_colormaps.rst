Pre Version 1.10.0a2 (2023-05-04)
*********************************

* Change colormap families to "matplotlib"

Breaking Changes
================

Change all colormap families to "matplotlib"
--------------------------------------------

Redefining plugin familes as a collection of required_parameters,
required_kwargs, and allowable_kwargs.  This allows us to have a
collections of keyword arguments that *can* be specified for
matplotlib-based colormaps, but do not *have* to be specified.
So rather than having a different family for every combination of
tuning parameters for color specifications, have a general "matplotlib" family
that all return the "mpl_colors_info" dictionary, but can have a variable set
of arguments (depending on requirements for a specific colormap).

All matplotlib families now have NO required params or kwargs, and a list of
available_kwargs.

::

  modified: geoips_clavrx/plugins/modules/colormaps/cmap_IR.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldFraction.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldHeight.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldHeightBase.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldHeightTop.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldMask.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldOpd.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldPhase.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldReff.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldTemp.py
  modified: geoips_clavrx/plugins/modules/colormaps/cmap_cldType.py
