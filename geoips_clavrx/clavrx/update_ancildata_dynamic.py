#!/usr/bin/env python

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Downloads dynamic CLAVR-x ancillary data."""

import argparse
from datetime import datetime
import requests
import logging
import os
from pathlib import Path
from itertools import chain
from glob import glob
from geoips.filenames.base_paths import PATHS as gpaths

LOG = logging.getLogger(__name__)


def fetch_dynamic(dynamic_dir, input_date=None):
    """Fetch dynamic data for Clavrx.

    Parameters
    ----------
    dynamic_dir: str
        Full path to where data will be downloaded.
    input_date: datetime
        Download dynamic data for given date.
    """
    date_format = "%m/%d/%Y"
    year = input_date.year
    month = input_date.month
    day = input_date.day

    day_one = datetime.strptime(f"01/01/{year}", date_format)
    day_now = datetime.strptime(f"{month}/{day}/{year}", date_format)
    delta = day_now - day_one

    day_total = str(delta.days + 1).zfill(3)
    year_digits = year - 2000
    hour = ["00", "06", "12", "18"]
    forecast_time = ["03", "06", "09", "12", "15", "18", "21"]
    gfs_files = []

    if month < 10:
        z = 0
    else:
        z = ""
    if day < 10:
        x = 0
    else:
        x = ""

    t = 0
    # NWP data
    for h in hour:
        for f in forecast_time:
            gfs_files.append(f"gfs.{year_digits}{z}{month}{x}{day}{h}_F0{f}.hdf")
    for check_create_dir in [
        dynamic_dir,
        f"{dynamic_dir}/gfs",
        f"{dynamic_dir}/oisst_nc/{year}",
        f"{dynamic_dir}/snow/hires",
    ]:
        if Path(check_create_dir).exists() is False:
            Path(check_create_dir).mkdir(parents=True, exist_ok=True)
    LOG.info("Downloading dynamic ancillary data to: %s", dynamic_dir)

    print("Downloading GFS files: \n")
    for i in range(len(gfs_files)):

        t += 1
        print(str(i) + ") " + gfs_files[i] + ":")
        if os.path.exists(f"{dynamic_dir}/gfs/{gfs_files[i]}"):
            print("GFS file already downloaded")
            continue

        url = (
            "http://geodb.ssec.wisc.edu/ancillary/"
            + f"{year}_{z}{month}_{x}{day}_{day_total}/{gfs_files[i]}"
        )
        print(url + "\n\n")
        logging.info(f"Downloading {url}")
        r = requests.get(url, timeout=3)

        if r.status_code == 404:
            logging.debug("HTTP 404: File not found, trying tyr.ssec")
            url = (
                "http://tyr.ssec.wisc.edu/gfs/"
                + f"{year}/{z}{month}_{x}{day}_{day_total}/{gfs_files[i]}"
            )
            print("Reattempting download: ", url + "\n\n")
            logging.info(f"Downloading {url}")
            r = requests.get(url, timeout=3)
            if r.status_code == 404:
                logging.debug("HTTP 404: both failed :(")
                continue

        open(f"{dynamic_dir}/gfs/{gfs_files[i]}", "wb").write(r.content)

    # IMS data
    snow = f"snow_map_4km_{year_digits}{z}{month}{x}{day}.nc"
    url = (
        "http://geodb.ssec.wisc.edu/ancillary/"
        + f"{year}_{z}{month}_{x}{day}_{day_total}/{snow}"
    )
    logging.info(f"Downloading {url}")
    r = requests.get(url, timeout=3)
    # Need 404 check
    if r.status_code == 404:
        print("No file found, attempting different url download")
        url = "http://tyr.ssec.wisc.edu/snow/" + f"{year}/{snow}"
        r = requests.get(url, timeout=3)

    elif os.path.exists(f"{dynamic_dir}/snow/hires/{snow}"):
        print("Snow map file already downloaded.")
    else:
        print(f"{i+1}) {snow}: \n")
        print(url + "\n\n")
        open(f"{dynamic_dir}/snow/hires/{snow}", "wb").write(r.content)

    # OISST data
    oisst = f"avhrr-only-v2.{year}{z}{month}{x}{day}.nc"
    url = (
        "http://geodb.ssec.wisc.edu/"
        + f"ancillary/{year}_{z}{month}_{x}{day}_{day_total}/{oisst}"
    )
    logging.info(f"Downloading {url}")
    r = requests.get(url, timeout=3)

    if r.status_code == 404:
        # oisst might be preliminary
        oisst = f"avhrr-only-v2.{year}{z}{month}{x}{day}_preliminary.nc"
        url = (
            "http://geodb.ssec.wisc.edu/"
            + f"ancillary/{year}_{z}{month}_{x}{day}_{day_total}/{oisst}"
        )
        r = requests.get(url, timeout=3)

        # ultimate fallback: tyr (hdf files?)
        if r.status_code == 404:
            url = "http://tyr.ssec.wisc.edu/oisst_nc/" + f"{year}/{oisst}"
            r = requests.get(url, timeout=3)

    if os.path.exists(f"{dynamic_dir}/oisst_nc/{year}/{oisst}"):
        print("AVHRR SST file already downloaded.")
    else:
        print(f"{i+2}) {oisst}:\n")
        print(url + "\n\n")
        if not os.path.isdir(f"{dynamic_dir}/oisst_nc/{year}/"):
            os.mkdir(f"{dynamic_dir}/oisst_nc/{year}/")
        open(f"{dynamic_dir}/oisst_nc/{year}/{oisst}", "wb").write(r.content)

    return


def clean_dynamic(dynamic_dir):
    """Clean dynamic directory."""
    filelist = [
        chain.from_iterable(glob(os.path.join(x[0], "*")) for x in os.walk(dynamic_dir))
    ][0]

    for f in filelist:
        if os.path.isdir(f):
            continue
        elif os.path.getsize(f) == 196:
            # exact size of empty files
            print(f"Empty file, removing: {f}")
            os.remove(f)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""The GeoIPS update_ancildata_dynamic.py wrapper for obtaining the
          static ancillary data required for running the
          University of Wisconsin Cooperative Institude for Meteorological Satellite
          Studies (CIMSS) Clouds for AVHRR Extended (CLAVR-x) pre-processing.

          CLAVR-x expects the dynamic ancillary data to exist specifically in the
          'dynamic' subdirectory of the --ancillary_data_directory, this wrapper
          script ensures the dynamic ancillary data exists in the correct location.
          """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--ancillary_data_directory",
        type=str,
        required=False,
        default=os.path.join(gpaths["GEOIPS_ANCILDAT"], "clavrx"),
        help="""Full path to the clavrx ancillary datasets.

          Note this --ancillary_data_directory must match:

          * --ancillary_data_directory passed into get_ancildata_static.py,
          * --ancillary_data_directory passed into into run_clavrx.py, and
          * first line of the clavrx_options file.
            * CLAVR-x uses the first line of the clavrx_options file
              to determine the full path to the ancillary data directory, and that
              directory must contain both explicitly named 'dynamic' and 'static'
              subdirectories.

          This command line argument should not include the
          'dynamic' subdirectory, but only the base ancillary data directory.""",
    )
    parser.add_argument(
        "--download_dtg",
        type=str,
        required=False,
        help="""Date time group to download, if not current date.

        This allows processing old test datasets, ensuring we have the dynamic
        ancillary data required for test scripts and case studies.""",
        default=datetime.now().strftime("%Y%m%d"),
    )
    parser.add_argument(
        "--clean_dynamic_empty_files",
        help="""Clean empty files found in the dynamic ancillary data directory.

          To ensure processing does not fail due to incomplete dynamic ancillary
          datasets, run --clean_dynamic_empty_files to remove files of size 196.
          """,
        action="store_true",
    )
    # This is a clavrx requirement - explicit "dynamic" and "static" subdirectories
    # must both be contained in the ancillary_data_directory.
    args = parser.parse_args()
    dynamic_data_directory = os.path.join(args.ancillary_data_directory, "dynamic")
    if args.clean_dynamic_empty_files:
        clean_dynamic(dynamic_data_directory)
    download_date = datetime.strptime(args.download_dtg, "%Y%m%d")
    fetch_dynamic(dynamic_data_directory, download_date)
