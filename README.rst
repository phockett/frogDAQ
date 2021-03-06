Femtolab FROG code
==================

Basic code for running FROG (Frequency Resolved Optical Gating) measurements & reconstruction.

Assumes:
    - Ocean Optics spectrometer
    - Newport ESP series delay stage, serial connection (USB>serial adaptor also OK)

Prerequisites:
    - pySeabreeze for spectrometer comms, https://github.com/ap--/python-seabreeze
    - newportESP for serial comms with ESP300/301 controller, https://pypi.org/project/NewportESP/
    - frog analysis routines from froglib, https://github.com/xmhk/froglib

Structure:
    - /frog defines a frog class, this provides an object to handle data & DAQ tasks.
    - /spec provides interfaces to spectrometers: currently supports Ocean Optics only.
    - /stage provides interfaces to stages: currently supports Newport ESP series.
    - frogDemo.py provides use examples, including required local settings for comms.

To do:
    - Finish restructuring & testing current version.
    - Add interface layer for handling other hardware types.
    - Finish python packaging (inc. dependencies).

Known issues/bugs:
    - newportESP module encoding may give errors (likely a python version and/or pyserial version change - tested with newportESP v1.0, python v3.6.6, pyserial v3.4)

      Note: adding .encode() or .decode() to the function call will convert to bytestring, as required.

      Lines to change in newportESP:
          122 - main serial write statement: add ".encode()" to serial write.
          
          286 - status read, changed comparison value to bytes: add ".decode()" to serial read.

    - Pickle save function currently limited to raw data (t, spectrum) only.
    - Reconstruction with froglib implements SHG or blind (default) reconstruction, see  https://github.com/xmhk/froglib for further details.



This code:
    Paul Hockett

    http://femtolab.ca

    https://github.com/phockett/frogDAQ

Released under GNU GPL v3.


*Sample FROG scan for broadband UV pulse*

.. image:: https://github.com/phockett/frogDAQ/blob/master/frogDAQ/demo/2018-10-31_15-29-54_frog_UV_50_20_15.5_comp.png

See demo directory for more.
