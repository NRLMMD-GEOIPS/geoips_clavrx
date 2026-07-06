    # # # This source code is subject to the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

Installing CLAVRx prebuilt
==========================

# Installing CLAVRx prebuilt binary

CLAVRx pre-built binaries can be installed with running:
```bash
    python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py
```

This installs a pre-built binary with RTTOV support from the SSEC WISC
GitLab repository.

Building CLAVR-x from scratch with RTTOV support
will be supported in a future GeoIPS release.  Outdated build instructions included
below for reference.

Running the CLAVR-x pipeline on input data
==========================================

Each of these GeoIPS wrapper scripts for installing and running CLAVR-x are fully
configurable via command line arguments.  Please call any of the below wrapper
script with --help for all supported arguments.

* `install_clavrx.py --help`
* `get_ancildata_static.py --help`
* `update_ancildata_dynamic.py --help`
* `run_clavrx.py --help`

Calling all scripts below without additional arguments will install in the GeoIPS
standard locations, which will allow completing the clarvx proc through geoips
integration test scripts successfully.

# Setup static ancillary data

After installing the pre-built binary, users can easily run the pipeline.
Ancillary data is needed to run the pipeline, and can easily be installed 
with the following command.

```bash
python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/get_ancildata_static.py
```

# Download relevant dynamic ancillary data

For running any processing, users must install dynamic ancillary data
surrounding the datetime of the observation. For observations near
00Z it is recommeneded to install both the day of observation and the
surrounding dates (EX: AHI data of 20251125T0100Z, download both 20251125T
and 20251124T dynamic data).

Calling `update_ancildata_dynamic.py` with no arguments will download the current
dynamic ancillary data.

```bash
python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py
python $GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/update_ancildata_dynamic.py YYYYMMDD
```

# Run processing on data

For running processing, execute the following command on all the input files.
Calling with no additional arguments will use the standard geoips locations for all
ancillary data, clavrx configuration files, etc. Please call `run_clavrx.py --help`
for supported arguments to configure your run as needed.

```bash
$GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py <input_files>
```

Outputs are produced in the following folder by default:

```bash
$GEOIPS_OUTDIRS/preprocessed/clavrx/
```

Running CLAVR-x pipeline with PSEG utility 
==========================================

Optionally, users can install PSEG, a multiprocessing wrapper for running CLAVR-x, this
reduces runtimes significantly for all sensors at the cost of compute strain. To install
PSEG and run it within processing, users can follow the steps below:

```bash
$GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/install_clavrx.py -p
```

Running CLAVR-x with PSEG is as simple as adding the -p flag to the processing call.

```bash
$GEOIPS_PACKAGES_DIR/geoips_clavrx/geoips_clavrx/clavrx/run_clavrx.py <runtime_args> -p
```


Depolying SSEC CLAVRx pipeline (outdated, will be reimplemented at a later date)
================================================================================

# NWP SAF Free Registration


Building, testing, and running CLAVR-x requires

1. Registering for and downloading the RTTOV radiative transfer model
2. Building CLAVR-x
3. Downloading the static and appropriate dynamic ancillary datasets
3. Running CLAVR-x on Level 1-B datasets (ABI, AHI, MODIS, VIIRS)
4. Running GeoIPS on the Level 2 output of CLAVR-x

Running CLAVR-x in near real-time requires

1. Making the 410GB static ancillary dataset available to the CLAVR-x processing
2. Setting up an automated method of running the dynamic ancillary
   dataset ingest
3. Setting up an automated method of kicking off CLAVR-x processing
   on the Level 1-B input datasets.
4. Setting up an automated method of kicking off GeoIPS processing
   on the Level 2 outputs from CLAVR-x.

Instructions for performing the first 4 steps are contained in
this document - the real-time processing implementation is outside
the scope of this plugin repository.

NWP SAF Free Registration
=========================

- For CLAVRx radiative transfer modeling, either PFAAST or RTTOV can be used, if RTTOV is preferred, follow steps below
- Click on this link to be directed to the registartion page: https://nwp-saf.eumetsat.int/site/registration_privacy/
- Click on the link at the bottom of the page labeled: "Accept and register"
- Fill out the necessary information that is asked to register
- An activation link will be sent to the email that you specified; Activate your account by clicking this link
(Note that if you do not recieve a registration confirmation email within a few minutes, double check your junk and/or spam;
If there is still no confirmation within an hour, email: admin@nwp-saf.eumetsat.int and they should resolve the issue)
- Once you have activated your account, go to this link: https://nwp-saf.eumetsat.int/site/
- Select the link at the top of the page labeled: "Software Downloads"
- If it asks for you to log in with your information, then login with the credentials that you just created in the steps before
- Click on the link at the bottom of the page labeled: "Change Software Preferences"
- Select the box located next to the RTTOV v13 package (note that v13 might be labeled as something else based upon the most recent version of the package)
- Scroll all the way to the bottom of the page and select the radio button labeled: "I agree" after reading the Licence Agreement
- Once this "I agree" button has been selected, Click on the "Update Software Preferences" button located at the bottom of the page
- At the bottom of the page a link will appear under the "Latest software package download links:"
- This link will look something like this: "RTTOV v13.2, November 2022" (yours might look different based on the most recent version of RTTOV)
- Click on this link to download the most recent RTTOV tar file
- Download the RTTOV tar file
  * Save it to ```$GEOIPS_DEPENDENCIES_DIR/rttov132.tar.xz```
  * (It can be saved anywhere, but for consistency so you can find it later...)
- Once you have completed these steps, you will then be able to install CLAVRx
- You will need to use the path to the rttov tar file as an arg to the CLAVR-x setup script,
  so don't forget where you put it!

Building CLAVRx from scratch (outdated)
=======================================

Install RTTOV tar file from instructions above
----------------------------------------------

CLAVR-x supports either PFAAST or RTTOV for radiative transfer modeling,
instructions for using RTTOV included above.

Set up conda environment for  CLAVR-x build
-------------------------------------------

Start in a completely clean bash enviroment, before sourcing config_clavrx_build.

```bash
  source $GEOIPS_PACKAGES_DIR/geoips_clavrx/setup/config_clavrx_build # Get current base conda env, and vars
  conda create -y -n clavrx_build -c conda-forge python=3.10 openblas git gcc=9.5 gxx=9.5 imagemagick gfortran curl hdf5 libnetcdf
  conda activate clavrx_build
```

Confirm environment
-------------------

Start in a completely clean bash environment, and source the clavrx build config
(once you've created the env).  Then confirm all the build tools are pointing to
your current conda environment

NOTE (open source-ish): DO NOT ```module load``` any libraries as this can lead to errors.

```bash
  source $GEOIPS_PACKAGES_DIR/geoips_clavrx/setup/config_clavrx_build
  # Verify everything is properly set:
  which python  # should point to python in your clavrx_build env, /base_path/miniconda3/envs/clavrx_build/bin/python
  which gcc  # should point to gcc in your clavrx_build env, /base_path/miniconda3/envs/clavrx_build/bin/gcc
  # If these are not pointing to your enviroment, compilling will fail, check your $PATH and other enviroment variables.
```

Install geoips into the CLAVR-x build environment
-------------------------------------------------

```pip install -e $GEOIPS_PACKAGES_DIR/geoips```

Run CLAVR-x install (takes ~40min)
----------------------------------

```$GEOIPS_PACKAGES_DIR/geoips_clavrx/setup.sh install_clavrx $GEOIPS_DEPENDENCIES_DIR/rttov132.tar.xz```

Now source $GEOIPS_CONFIG_FILE, to use your normal geoips environment
You should have already installed geoips_clavrx into your normal GeoIPS environment from the README

Obtain ancillary datasets required for tests
============================================

Link static ancillary data if appropriate
-----------------------------------------

NOTE: Static data for clavrx is large (410 GB) and is slow to download (+6 hours),
it is recommended you softlink the static data

Install dynamic ancillary data (and static if not linked)
---------------------------------------------------------

SAY NO TO STATIC IF YOU HAVE ACCESS TO A SHARED LOCAL COPY

This setup script installs the dynamic ancillary data required
for the test scripts included with this plugin repository.

```$GEOIPS_PACKAGES_DIR/geoips_clavrx/setup.sh install_ancillary_data```

Test the installation
---------------------

NOTE: This can be run either in your native geoips_conda enviroment or the clavrx install enviroment.
We recommend using your standard GeoIPS environment by sourcing the appropriate GEOIPS_CONFIG_FILE
or other appropriate method of setting up your environment.

```bash
  # Ensure GeoIPS environment is set
  $GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/scripts/viirs.clavrx_proc.sh
```

Running CLAVRx processing (TBD)
===============================

- Run geoips_clavrx/ancillary/update_dynamic.py <YYYYMMDD> with the date values from the respective data
- Create an level2_list that contains the output values needed
- Pass an input file, input directory, and output directory to geoips_clavrx/run_clavrx_proc.py
- Example options files, and level2 files can be found in tests/proc_files/
- Verify output log and data to check for missing data, improper builds, or correct option selection
