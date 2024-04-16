#!/usr/bin/env bash

# Minimal installer for frogDAQ prerequisites
#
# NOTE: this uses pip to install libs, if using virtual envs please first activate desired env!
#
# v1 16/04/24   For Docker builds.
#

# Set working dir, defaults to cwd
WORKINGDIR=${1:-$(pwd)}
REPODIR=${2:-$(cd ../ && pwd)}

echo "Working dir: ${WORKINGDIR}"
echo "Repo/parent dir: ${REPODIR}"

#*** FROGLIB, https://github.com/xmhk/froglib
# Clone repo
echo "Cloning Froglib"
cd $REPODIR
git clone https://github.com/xmhk/froglib.git
# Add setup file patch to allow for pip install.
cp ${WORKINGDIR}/patches/setup_froglib.py ${REPODIR}/froglib/setup.py

#*** Install local repos
echo "Running 'pip install -e .' for local repos..."
cd $WORKINGDIR
pip install -e .

cd ${REPODIR}/froglib
pip install -e .

#*** Install other repos
echo "Installing pyserial and NewportESP libs..."

# Install from https://pypi.org/project/NewportESP, may need patching
# pip install NewportESP

# Install local patched version
cd $WORKINGDIR/patches/newportESP-1.1
pip install .

pip install pyserial

# pip install NewportESP
# conda install pyserial

# NOTE - currently need to replace NewportESP with frogDAQ/patches/NewportESPbyte.py - not sure how to automate this (with conda this is in something like <conda user dir>/<env>/site-packages)
# In test Docker builds, /opt/conda/lib/python3.9/site-packages/newportESP.py
# UPDATE: now use frogDAQ/patches/newportESP-1.1 instead. Should push to Github?



#*** pySEABREEZE, from https://python-seabreeze.readthedocs.io/en/latest/install.html
echo "Installing seabreeze lib..."
# conda install -c conda-forge seabreeze
pip install seabreeze

# Run Seabreeze USB config script, see https://github.com/ap--/python-seabreeze/tree/main/os_support
# For Linux this sets UDEV rules
# For Win, downloads drivers.
# In Docker this only works if /etc/udev available...?

# seabreeze_os_setup
echo "To configure spectrometers, run 'seabreeze_os_setup'."
