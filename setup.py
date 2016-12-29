#!/usr/bin/env python

import versioneer
from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from the relevant file
# TODO Make this parse nicely into PyPy
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mkerefuse',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Milwaukee (WI, USA) Garbage & Recyling Date Finder',
    long_description=long_description,

    url='https://github.com/tomislacker/python-mke-trash-pickup',

    author='Ben Tomasik',
    author_email='ben@tomasik.io',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='milwaukee wisconsin garbage recycle recycling',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'docopt',
        'pyyaml',
        'requests',
    ],

    extras_require={
        'dev': ['nose', 'pep8'],
        'test': ['coverage'],
    },

    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'mkerefusecheck=mkerefuse.__main__',
        ],
    },
)
