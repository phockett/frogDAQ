from setuptools import setup, find_packages

# Minimal setup.py for froglib, adapted from
# https://github.com/maet3608/minimal-setup-py/blob/master/setup.py

setup(
    name='froglib',
    version='1.0.0',
    url='https://github.com/xmhk/froglib/tree/master',
    author='Christoph Mahnke (xmhk), 2018',
    author_email='chmhnk_at_googlemail_dot_com',
    description='A library to reconstruct the complex optical field of short optical pulses from FROG (Frequency Resolved Optical Gating[1]) traces.',
    packages=find_packages(),
    install_requires=[],
)
