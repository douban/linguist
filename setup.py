#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'linguist',
    version = '0.0.1',
    keywords = ('linguist',),
    description = 'Language Savant',
    long_description = 'Language Savant',
    license = 'MIT License',

    url = 'https://github.com/liluo/linguist',
    author = 'liluo',
    author_email = 'i@liluo.org',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['PyYAML', 'pygments>=1.6', 'charlockholmes'],
    classifiers = [],
)
