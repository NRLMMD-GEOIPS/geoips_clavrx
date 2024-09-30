# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Downloads ancillary data."""

from datetime import datetime
import calendar
import requests
import logging
import os

LOG = logging.getLogger(__name__)

today = datetime.now()
date_format = "%m/%d/%Y"


year = today.year
month = today.month
day = today.day

day_one = datetime.strptime(f"01/01/{year}", date_format)
day_now = datetime.strptime(f"{month-1}/{day}/{year}", date_format)
delta = day_now - day_one

if calendar.isleap(year):
    day_total = delta.days + 2
else:
    day_total = delta.days + 1

year_digits = year - 2000
hour = ["00", "06", "12", "18"]
forecast_time = ["03", "06", "09", "12", "15", "18", "21"]
gfs_files = []

if month - 1 < 10:
    z = 0
else:
    z = ""
if day < 10:
    x = 0
else:
    x = ""


key = "GEOIPS_DEPENDENCIES_DIR"
geoips_dependencies_dir = os.getenv(key)

ancil_home = f"{geoips_dependencies_dir}/clavrx/ancillary/"
dynamic_dir = f"{geoips_dependencies_dir}/clavrx/ancillary/dynamic"
static_dir = f"{geoips_dependencies_dir}/clavrx/ancillary/static"
t = 0

"""
Below is the download of dynamic ancillary data required for CLAVRx to function
"""

# Required NWP data
for h in hour:
    for f in forecast_time:
        gfs_files.append(f"gfs.{year_digits}{z}{month-1}{x}{day}{h}_F0{f}.hdf")

print("list of files: \n")
for i in range(len(gfs_files)):
    t += 1
    print(str(i) + ") " + gfs_files[i] + ": \n")
    url = (
        "http://geodb.ssec.wisc.edu/ancillary/"
        + f"{year}_{z}{month-1}_{x}{day}_{day_total}/{gfs_files[i]}"
    )
    print(url + "\n\n")
    logging.info(f"Downloading {url}")
    r = requests.get(url, timeout=1)
    open(f"{dynamic_dir}/gfs/{gfs_files[i]}", "wb").write(r.content)

# Optional IMS data
snow = f"snow_map_4km_{year_digits}{z}{month-1}{x}{day}.nc"
url = (
    "http://geodb.ssec.wisc.edu/ancillary/"
    + f"{year}_{z}{month-1}_{x}{day}_{day_total}/{snow}"
)
logging.info(f"Downloading {url}")
r = requests.get(url, timeout=3)
print(f"{i+1}) {snow}: \n")
print(url + "\n\n")
open(f"{dynamic_dir}/snow/hires/{snow}", "wb").write(r.content)


# Optional OISST data
oisst = f"avhrr-only-v2.{year}{z}{month-1}{x}{day}.nc"
url = (
    "http://geodb.ssec.wisc.edu/"
    + f"ancillary/{year}_{z}{month-1}_{x}{day}_{day_total}/{oisst}"
)
logging.info(f"Downloading {url}")
r = requests.get(url, timeout=3)
print(f"{i+2}) {oisst}:\n")
print(url + "\n\n")
open(f"{dynamic_dir}/oisst_nc/{year}/{oisst}", "wb").write(r.content)

"""
Download static data for CLAVRx
"""
# download from CSPP (much more reliable)
"""
static_url = "https://bin.ssec.wisc.edu/pub/CSPP/hidden/CLAVRx/v3.0/"
             "CSPP_CLAVRX_V3.0_STATIC.tar.xz"

print("Downloading Static data from CSPP_CLAVRX v3.0")

wget_run = subprocess.run(
    ["wget", "-v", static_url], capture_output=True, cwd=ancil_home
)

# print(wget_run.stdout)
tar_path = os.path.join(ancil_home, "CSPP_CLAVRX_V3.0_STATIC.tar.xz")
if not os.path.exists(tar_path):
    print("Tar file issue, see error: ", wget_run.stderr)
    raise
print("Tar file downloaded successfully, untarring")
untar = subprocess.run(["tar", "-xaf", tar_path], capture_output=True, cwd=static_dir)
static_folders = os.path.join(static_dir, "CLAVRx_3_0", "static", "*")

subprocess.run(f"mv {static_folders} {static_dir}", shell=True)
subprocess.run(["rm", "-rf", os.path.join(static_dir, "CLAVRx_3_0")])
"""
print("Finished downloading static and ancillary data")
