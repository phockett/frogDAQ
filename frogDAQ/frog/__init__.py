# -*- coding: utf-8 -*-

# Module Imports
# 06/05/21 Duplicated some fo these imports in class method files as they seem to be broken/out of scope currently (testing in Python 3.9)
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import interpolate

#*** Optional Imports
# Import seabreeze for Ocean Optics spectrometer interfacing
try:
    from frogDAQ.spec import OOfunc as OO
except ImportError as e:
    if e.msg != "No module named 'seabreeze.spectrometers'":
        raise
    print('* Seabreeze not found, Ocean Optics Spectrometers not available. ')

# Import froglib for frog reconstruction routines
try:
    # sys.path.append(os.path.join(os.curdir,'froglib-master'))      # Set explicit path if desired
    import froglib as frlib
except ImportError as e:
    if e.msg != "No module named 'froglib'":
        raise
    print('* Froglib not found, FROG reconstruction routines not available. ')

#*** Init frog class based on local definitions
class frog():
    """Class for FROG data and methods.

    Call with frog() for no hardware options, and sensible defaults for other parameters.
    Full call with frog(devices=None, stage=None, devID=0, scanRange=[-100, 100], t0=0, intT=100000, frames=1)

    Where:
      - devices, list of spectrometers, currently assumed to be Ocean Optics device initialized with pySeabreeze
        For testing without spectrometer, set devices = None
      - stage, newport ESP stage object. For testing code without stage, set stage = None
    Optional:
      - devID, select member from devices[], default = 0
      - scanRange (fs), default = [-100,100]
      - t0 position (fs), default = 0
      - intT, spectrometer integration time (us), default=100000
      - frames, spectrometer frames/captures to sum, default=1

    help(frog) for a full class listing.

    """


    # Load definitions from modules (files).
    from ._temporalDef import delays, fsmm
    from ._ROI import setROI, crop, interpROI
    from ._recon import setRecon, reconFL
    from ._spec import darkScan, specRun, specStability
    from ._scan import scan
    from ._IOdef import saveFrog, loadFrog
    from ._plotFr import plot


    #Init object - set empty params, and some sensible defaults.
    def __init__(self, devices=None, stage=None, devID=0, scanRange=[-100, 100], t0=0, intT=100000, frames=1):

        # Set hardware
        self.devices = devices
        self.devID = 0
        self.stage = stage

        # Set parameters - motion
        self.t0=t0
        self.scanRange=scanRange

        # Set parameters - spectrum
        self.intT=intT
        self.frames=frames

        # Get wavelength range from spectrometer
        if self.devices is not None:
            _, self.wavelengths = OO.capture(devices, devID=devID, frames=1)
            self.dark = np.zeros(len(self.wavelengths))
        else:
            self.wavelengths = np.zeros(128)

        # Set delays
        self.delays()
        # self.data = np.zeros((len(self.wavelengths),len(self.mm)))

        # Data save parameters
        self.fileName = None
        self.savePath = None
        self.saveType = 'p'     # Set default to pickle object

        # Init data structures for ROI and recon (as subclasses)
        self.ROI = self.setROI()
        self.recon = self.setRecon(WR = (self.wavelengths[0],self.wavelengths[-1]))  # Default to full wavelength range.
        
