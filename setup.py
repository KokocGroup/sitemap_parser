# !/usr/bin/env python
# coding=utf-8
from __future__ import with_statement, unicode_literals

from setuptools import find_packages, setup

VERSION = "0.0.8"

setup(
    name='sitemap_parser',
    description="",
    version=VERSION,
    url='https://github.com/KokocGroup/sitemap_parser',
    author='Evgeniy Titov',
    author_email='falgore88@gmail.com',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.6.3',
        'lxml==4.2.5'
    ]
)
