#!/usr/bin/env python
import sys
import versioneer
from setuptools import setup

SETUP_REQUIRES = ["setuptools >= 30.3.0"]
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []

if __name__ == "__main__":
    setup(
        name="rewardgym",
        setup_requires=SETUP_REQUIRES,
        include_package_data=True,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
    )
