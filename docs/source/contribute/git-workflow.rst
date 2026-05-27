.. note:: Distribution Statement

   # # # This source code is subject to the license referenced at
   # # # https://github.com/NRLMMD-GEOIPS.

Git Workflow
************

This document outlines the git workflow specific to the geoips_clavrx plugin.
For the general GeoIPS git workflow, see the base GeoIPS documentation.

Branch Naming
==============

Branches in the geoips_clavrx repository should follow this naming convention:

``<type>/<short-description>``

Where ``<type>`` is one of:

- ``feature/`` - New features or enhancements
- ``bugfix/`` - Bug fixes
- ``docs/`` - Documentation changes
- ``test/`` - Test additions or modifications
- ``refactor/`` - Code refactoring without functional changes

Examples:

- ``feature/add-clavrx-v2-support``
- ``bugfix/fix-cloud-phase-colorbar``
- ``docs/update-installation-instructions``
- ``test/add-integration-test-for-goes-r``

Note: Actual repository branch names may not strictly follow this convention.
This serves as a recommended guideline for contributors.

All development should target the ``main`` branch.

Running Plugin-Specific Tests Before PR
=======================================

Before submitting a Pull Request, ensure all tests pass:

1. Run specific test categories using pytest markers:

    .. code-block:: bash

        pytest -m base          # Run base tests
        pytest -m full          # Run full test suite
        pytest -m lint          # Run linting checks
        pytest -m validation    # Run validation tests

2. Ensure your branch passes the ``geoips/tests/utils/check_code.sh`` script
    from the base GeoIPS repository before requesting a review.
