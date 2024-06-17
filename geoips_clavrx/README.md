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

# NWP SAF Free Registration

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
  * Save it to $GEOIPS_DEPENDENCIES_DIR/rttov132.tar.xz
  * (It can be saved anywhere, but for consistency so you can find it later...)
- Once you have completed these steps, you will then be able to install CLAVRx
- You will need to use the path to the rttov tar file as an arg
  - $GEOIPS_PACKAGES_DIR/geoips_clavrx/setup.sh install $GEOIPS_DEPENDENCIES_DIR/rttov132.tar.xz
