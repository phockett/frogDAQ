Femtolab FROG code
==================

Basic code for running frog measurements & reconstruction.

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
    - Finish restructuring.
    - Add interface layer for handling other hardware types.

This code:
    Paul Hockett
    paul@femtolab.ca
    femtolab.ca
    github.com/phockett  [not yet posted]

Released under GNU GPL v3.
