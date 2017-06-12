#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="pgraphmap",
    version='0.1',
    description='Parallel graphmap',
    url='https://github.com/nmiculinic/pgraphmap',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'celery',
        'redis',
        'pysam',
        'biopython',
        'python-dotenv'
    ],
)
