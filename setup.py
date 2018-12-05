# -*- coding: utf-8 -*-

# Setup file for the femtolab frogDAQ

# Setup template from: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='frogDAQ',
    version='0.4.2',
    description='Femtolab FROG code, current version for Ocean Optics Spectrometers + Newport ESP stages',
    long_description=readme,
    # long_description_content_type="text/rst",
    author='Paul Hockett',
    author_email='paul@femtolab.ca',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
