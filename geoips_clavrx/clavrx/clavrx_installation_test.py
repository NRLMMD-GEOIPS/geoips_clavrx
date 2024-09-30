# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Wrapper to install clavrx."""

from install_clavrx import install_clavrx
from datetime import datetime

install_parent_dir = "/users/duff/install_clavrx_test/lib"
clavrx_install_dir = "/users/duff/install_clavrx_test/"

tarball_dir = "/users/duff/install_clavrx_test/tar"

hdf4_ver = "4.2.15"
hdf5_ver = "1.10.9"
netcdf_ver = "4.9.0"
rttov_ver = "132"

start = datetime.now()

install_clavrx(
    install_parent_dir,
    clavrx_install_dir,
    tarball_dir,
    hdf4_ver,
    hdf5_ver,
    netcdf_ver,
    rttov_ver,
)


end = datetime.now()

print(f"Total time to build and install CLAVRx: {end-start}")
