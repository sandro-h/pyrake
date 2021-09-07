#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

setup(
    author="sandro-h",
    python_requires='>=3.6',
    description="pyrake",
    install_requires=[
        'soupsieve==2.1', 'lxml==4.6.2', 'beautifulsoup4==4.9.3'
    ],
    include_package_data=True,
    name='pyrake',
    packages=find_packages(include=['pyrake']),
    url='https://github.com/sandro-h/pyrake',
    version='0.2.0',
    zip_safe=False,
)