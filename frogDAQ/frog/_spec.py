
# Methods for basic spectrometer IO
from frogDAQ.spec import OOfunc as OO

# Define reference spectrum
def darkScan(self):
    intensities,_ = OO.capture(self.devices, devID=self.devID, intT=self.intT, frames=self.frames)

    if self.frames > 1:
        self.dark = intensities.sum(axis=0)
    else:
        self.dark = intensities

# Basic call for just showing spectra (free run)
def specRun(self):
    if self.devices is not None:
        # Grab spectrum
        intensities,_ = OO.run(self.devices, devID=self.devID, intT=self.intT, frames=0, waveLim=self.ROI.waveLim)

# Spectra with long-term logging, display and averaging
def specStability(self, period=None, poll=None):

    if period is not None:
        #TODO: Check time, and set to run for defined
        pass

    if self.devices is not None:
        # Grab spectrum
        intensities,_ = OO.run(self.devices, devID=self.devID, intT=self.intT, frames=0, waveLim=self.ROI.waveLim)
