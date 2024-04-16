# frogDAQ install with Jupyterlab Open stacks base (UB22)
# 16/04/24
#
#
# For test builds
#     docker build -t frogdaq:vXXXX .
#
# Run (with sudo)
#     docker run -it -p 9119:8888 --user root -e GRANT_SUDO=yes frogdaq
#
# To autoremove on stop, add --rm to run command
#
# For USB device access, see https://stackoverflow.com/a/66427245
#
# TEST BUILDS... (note need SUDO for seabreeze config testing)
#   docker run -it --rm -v ~/github/frogDAQ:/home/jovyan/frogDAQ -p 9119:8888 --user root -e GRANT_SUDO=yes -e NB_USER="jovyan" frogdaq:v160424 bash

# Use full scipy notebook, see https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
# 23/01/23 - force to python 3.8 build, can't install Spinnaker whl otherwise!
#           https://hub.docker.com/layers/jupyter/scipy-notebook/x86_64-python-3.8.13/images/sha256-e3b039665109ca38ecf173b548b13ecaca7e2f92755f5175e0c48253fbc482d6?context=explore
# FROM jupyter/scipy-notebook:x86_64-python-3.8.13

# Latest build
FROM jupyter/scipy-notebook

# Set user to root for installers below.
# TODO 21/02/24: change to Jovyan for Conda env creation and/or fix perms and/or run with SUDO - currently have some weird perm issues otherwise, e.g. `conda run -n spinnaker python --version` fails for Jovyan user.
# USER root

# Copy source - use local version?
# COPY ../frogDAQ .    # Failing with relative parent here?
# COPY /home/paul/github/frogDAQ ./frogDAQ
# COPY ./install_prereqs.sh

# Or just pull...
# Note optional @branch here
# RUN pip install --no-deps git+https://github.com/phockett/frogDAQ@updatesApril2024
