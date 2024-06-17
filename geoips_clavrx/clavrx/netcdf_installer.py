# # # Distribution Statement A. Approved for public release. Distribution is unlimited.
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

"""Install netcdf and set netcdf env vars."""

import os
import sys
import shutil
import requests
import logging

from install_utils import run_shell_command
from hdf5_installer import get_hdf5_verify_path


def get_netcdf_install_dir(install_parent_dir, netcdf_ver):
    """Join parent dir with netcdf variables."""
    return os.path.join(install_parent_dir, "netcdf", f"netcdf-c-{netcdf_ver}")


def get_netcdf_verify_path(netcdf_dir):
    """Return a path with the specified version of HDF5 is installed."""
    return os.path.join(netcdf_dir, "bin", "nf-config")


def get_env_variables_netcdf_c(compiler_flags, hdf5_dir, netcdf_install_dir):
    """Update env with new vars."""
    environ = dict(os.environ)
    environ["LDFLAGS"] = f"-L{hdf5_dir}/lib"
    environ["PATH"] = f"{hdf5_dir}/bin:{environ.get('PATH', '')}"
    environ["LD_LIBRARY_PATH"] = f"{hdf5_dir}/lib:{environ.get('LD_LIBRARY_PATH', '')}"
    environ["LIBRARY_PATH"] = f"{hdf5_dir}/lib:{environ.get('LIBRARY_PATH', '')}"
    # Not sure if NCDIR is required, so leaving out for now
    environ["NCDIR"] = netcdf_install_dir
    environ["CPPFLAGS"] = f"-I{hdf5_dir}/include"
    return environ


def get_env_variables_netcdf_f(netcdf_install_dir, hdf4_dir, hdf5_dir):
    """Set env new env vars for netcdf download."""
    environ = dict(os.environ)
    environ["LD_LIBRARY_PATH"] = (
        f"{netcdf_install_dir}/lib:{hdf4_dir}/lib:\
    {hdf5_dir}/lib:{environ.get('LD_LIBRARY_PATH', '')}"
    )
    # Not sure if NCDIR and NFDIR are required, but can't hurt
    environ["NCDIR"] = netcdf_install_dir
    environ["NFDIR"] = netcdf_install_dir
    environ["CPPFLAGS"] = f"-I{netcdf_install_dir}/include -I{hdf5_dir}/include"
    environ["LDFLAGS"] = f"-L{netcdf_install_dir}/lib -L{hdf5_dir}/lib"
    return environ


def get_netcdf_f_version(netcdf_ver):
    """Check netcdf version compatibility."""
    netcdf_f_compatibility = {
        # netcdf_f_ver: min_netcdf_ver
        "4.5.3": "4.7.4",
        "4.5.2": "4.6.0",
        "4.6.0": "4.9.0",
    }
    # Sort in reverse order of netcdf-f
    netcdf_f_versions = sorted(netcdf_f_compatibility.keys(), reverse=True)
    for this_netcdf_f_ver in netcdf_f_versions:
        min_netcdf_ver = netcdf_f_compatibility[this_netcdf_f_ver]
        if netcdf_ver >= min_netcdf_ver:
            return this_netcdf_f_ver
    raise KeyError(
        f"No compatible netcdf-f version found for netcdf version {netcdf_ver}.\
        May need to update netcdf_f_compatibility dictionary"
    )


def install_netcdf_f(
    netcdf_f_ver,
    netcdf_dir,
    hdf4_dir,
    hdf5_dir,
    tarball_dir,
    compiler_flags,
):
    """Download and install netcdf."""
    # download netcdf-f tarball
    netcdf_tar_dir = os.path.join(tarball_dir, "netcdf")
    os.makedirs(netcdf_tar_dir, exist_ok=True)
    netcdf_f_tar_filepath = os.path.join(
        netcdf_tar_dir, f"netcdf-fortran-{netcdf_f_ver}.tar.gz"
    )
    if not os.path.isfile(netcdf_f_tar_filepath):
        url = (
            "https://github.com/Unidata/netcdf-fortran/"
            + f"archive/refs/tags/v{netcdf_f_ver}.tar.gz"
        )
        logging.info(f"Downloading {url}")
        r = requests.get(url, timeout=3)
        open(netcdf_f_tar_filepath, "wb").write(r.content)

    logging.info("Untarring netcdf-f tarball")
    netcdf_f_src_folder = f"netcdf-fortran-{netcdf_f_ver}"
    if os.path.isdir(netcdf_f_src_folder):
        shutil.rmtree(netcdf_f_src_folder)

    run_shell_command(
        f"tar -xf {netcdf_f_tar_filepath} -C {netcdf_dir}/",
        "Untarring netcdf-fortran tarball",
        env=None,
    )

    os.chdir(f"{netcdf_dir}/{netcdf_f_src_folder}")

    netcdf_f_env = get_env_variables_netcdf_f(netcdf_dir, hdf4_dir, hdf5_dir)

    run_shell_command(
        f"./configure --enable-fortran --prefix={netcdf_dir}",
        "Configuring netcdf-f",
        env=netcdf_f_env,
    )

    run_shell_command(
        "make",
        "Compiling netcdf-fortran (this will likely take a while)",
        env=netcdf_f_env,
    )
    run_shell_command("make -i install", "Installing netcdf-fortran", env=netcdf_f_env)

    os.chdir(os.pardir)


def install_netcdf(
    install_parent_dir,
    netcdf_ver,
    hdf4_dir,
    hdf5_dir,
    tarball_dir,
    compiler_flags,
    overwrite=False,
):
    """Install netcdf from a tarball."""
    netcdf_dir = get_netcdf_install_dir(install_parent_dir, netcdf_ver)

    if os.path.isfile(get_netcdf_verify_path(netcdf_dir)) and not overwrite:
        hdf5_verify_path = get_hdf5_verify_path(hdf5_dir)
        if not os.path.isfile(hdf5_verify_path):
            logging.critical(
                f"{hdf5_verify_path} is missing.\
                HDF5 must be installed prior to netCDF.\
                This is unexpected if using the provided install_clavrx.py"
            )
            sys.exit()
        else:
            logging.info(f"Using existing netcdf installation at {netcdf_dir}")
            return netcdf_dir
    logging.info(f"Installing netcdf at {netcdf_dir}")
    if os.path.isdir(netcdf_dir):
        shutil.rmtree(netcdf_dir)
    os.makedirs(netcdf_dir)

    # download netcdf-c tarball
    netcdf_tar_dir = os.path.join(tarball_dir, "netcdf")
    os.makedirs(netcdf_tar_dir, exist_ok=True)
    netcdf_c_tar_filepath = os.path.join(
        netcdf_tar_dir, f"netcdf-c-{netcdf_ver}.tar.gz"
    )
    if not os.path.isfile(netcdf_c_tar_filepath):
        url = (
            "https://github.com/Unidata/netcdf-c/"
            + f"archive/refs/tags/v{netcdf_ver}.tar.gz"
        )
        logging.info(f"Downloading {url}")
        r = requests.get(url, timeout=3)
        open(netcdf_c_tar_filepath, "wb").write(r.content)

    logging.info("Untarring netcdf-c tarball")

    run_shell_command(
        f"tar -xf {netcdf_c_tar_filepath} -C {netcdf_dir}/..",
        "Untarring netcdf tarball",
        env=None,
    )

    os.chdir(f"{netcdf_dir}")

    netcdf_c_env = get_env_variables_netcdf_c(compiler_flags, hdf5_dir, netcdf_dir)

    run_shell_command(
        f"./configure --enable-fortran --prefix={netcdf_dir}",
        "Configuring netcdf-c",
        env=netcdf_c_env,
    )
    run_shell_command(
        "make",
        "Compiling netcdf-c (this will likely take a while)",
        env=netcdf_c_env,
    )
    run_shell_command("make -i install", "Installing netcdf-c", env=netcdf_c_env)

    os.chdir(os.pardir)

    netcdf_f_ver = get_netcdf_f_version(netcdf_ver)
    install_netcdf_f(
        netcdf_f_ver,
        netcdf_dir,
        hdf4_dir,
        hdf5_dir,
        tarball_dir,
        compiler_flags,
    )

    return netcdf_dir
