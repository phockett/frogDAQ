# Define temporal params

# Imports
import numpy as np
from scipy import constants as scipy_constants

# Set delays for scan, with sensible defaults
def delays(self,points=None,step=None):

    # Set default scan range
    if points is None:
        points = 25

    if step is None:
        self.fs = np.linspace(self.scanRange[0],self.scanRange[1],points)   # Delays defined as start:stop in N points, defaults to N=50 if not specified
    else:
        self.fs = np.arange(self.scanRange[0],self.scanRange[1]+step,step)               # Delays defined as start:step:stop

    # Set precision
    self.fs=self.fs.round(decimals=2)

    # Set mm values
    self.fsmm()

    # Reset data array - do this here to allow for cases where delays() is called directly
    self.data = np.zeros((len(self.wavelengths),len(self.mm)))


# Conversion of fs to stage position (mm)
def fsmm(self):
    c=scipy_constants.c    # Speed of light in m/s

    # Calculate positions
    mm=0.5*(self.fs*1e-15*c)/1e-3        # Calculate positions in mm, assumes factor of 2 for geometry.
    mm=mm+self.t0                        # Offset position by t0 (if defined)
    self.mm=mm.round(decimals=4)         # Set values with stage precision - SHOULD BE able to get from stage...?
    self.fs=(self.mm-self.t0)*1e-3/(0.5*1e-15*c)   # Reset fs values based on actual stage values
    #TODO check this - buggy/incorrect fs values in some cases???
