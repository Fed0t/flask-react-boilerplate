#!/usr/bin/env python

import re
import sys
from os import path
from setuptools import setup, find_packages


version_file = path.join(path.dirname(__file__), "flask_restful", "__version__.py")
with open(version_file, "r") as fp:
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fp.read(), re.M)
    version = m.groups(1)[0]


setup(
    name="ColdWallet",
    version=version,
    license="BSD",
    author="Veelancing",
    author_email="contact@veelancing.io",
    description="Veelancing Cold Wallet",
    packages=find_packages(exclude=["tests"]),
)
