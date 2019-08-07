from setuptools import setup

VERSION = "0.0.8"

with open('README.rst', 'r') as f:
    long_description = f.read()
setup(
    name="sinricpro",
    version=VERSION,
    author="Dhanush",
    author_email="dhanushdazz@gmail.com",
    description="A python package for your sinric-pro alexa skill",
    long_description=long_description,
    url="https://github.com/sinricpro/Python-SDK",
    packages=['sinric'],
    install_requires=["websockets","loguru"],
    keywords=['alexa', 'alexa-skill', 'sinric', 'sinric-alexa-skill', 'alexa-home-automation', 'sinric-pro',
              'sinric-pro-alexa-skill'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ]
)
