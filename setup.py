"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

from setuptools import setup
import sys

if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')

VERSION = "2.4.1"

with open('README.rst', 'r') as f:
    long_description = f.read()
setup(
    name="sinricpro",
    version=VERSION,
    author="Dhanush",
    author_email="dhanushdazz@gmail.com",
    description="A python package for your sinric-pro alexa skill",
    long_description=long_description,
    url="https://github.com/sinricpro/python-sdk",
    packages=['sinric'],
    install_requires=["websockets","loguru"],
    keywords=['alexa', 'alexa-skill', 'sinric', 'sinric-alexa-skill', 'alexa-home-automation', 'sinric-pro',
              'sinric-pro-alexa-skill'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
