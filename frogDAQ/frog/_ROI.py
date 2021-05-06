# 06/05/21 Added imports here as they seem to be broken currently (testing in Python 3.9)
import numpy as np
from scipy import interpolate
# import matplotlib.pyplot as plt

# Set nested classes to use for structure-like objects for ROIs and recon
# Empty class is like a dynamic structure, although may have side-effects.
# Otherwise need a proper constructor.
# Is this bad form?  Useful for '.' notation!
# TODO: set constructors here! Think of alternatives...?

class setROI():
    def __init__(self, fsLim = None, waveLim = None, dimInterp = None, dataInterp = None):
        self.waveLim = waveLim
        self.fsLim = fsLim
        self.waveRange = None
        self.fsRange = None
        self.wavelengths = None
        self.fs = None
        self.data = None
        self.dataInterp = dataInterp
        self.dim = None
        self.dimInterp = dimInterp
        self.s = None

# Crop data to region of interest, using ROI structure for settings
def crop(self, waveLim = None, fsLim = None, interpFlag = False):
    
    # Set limits to defaults, or use preset values, if not specified.
    if fsLim is None and self.ROI.fsLim is None:
        self.ROI.fsLim = [self.fs[0], self.fs[-1]]
    if waveLim is None and self.ROI.waveLim is None:
        self.ROI.waveLim = [self.wavelengths[0], self.wavelengths[-1]]

    # Set data ranges
    self.ROI.waveRange = np.logical_and(self.wavelengths >= self.ROI.waveLim[0], self.wavelengths <= self.ROI.waveLim[1])
    self.ROI.fsRange = np.logical_and(self.fs >= self.ROI.fsLim[0], self.fs <= self.ROI.fsLim[1])

    # TODO: fix ugly crop routine
    # self.ROI = self.data[waveRange,fsRange] # This doesn't work due to dimensionality, but should be a fix...
    self.ROI.data = self.data[self.ROI.waveRange,:]   # Two-step ugly hack for above
    self.ROI.data = self.ROI.data[:,self.ROI.fsRange]
    self.ROI.fs = self.fs[self.ROI.fsRange]
    self.ROI.wavelengths =  self.wavelengths[self.ROI.waveRange]

    print('Set data ROI to : ', self.ROI.data.shape)


#*** Interpolation codes. See "scipy_interp_test_190918.py" for prototypes, and https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#multivariate-data-interpolation-griddata

# DEPRECATED (may also be incorrect!): Interpolate recorded data for FROG recon - square image and pow(2) size
# newDim = integer for new size
# s controls interpolation smooting
#    def interp(self, newDim, s = 0.1):
#        # Set original gridding
#        dims = self.data[self.reconWR].shape
#        x, y = np.mgrid[-1:1:(dims[0]*1j), -1:1:(dims[1]*1j)]
#
#        # Interp to newDim
#        xnew, ynew = np.mgrid[-1:1:(newDim*1j), -1:1:(newDim*1j)]   # Weird - apparently using complex here provides grid inclusive of stop value, see https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.mgrid.html
#        tck = interpolate.bisplrep(x, y, self.data[self.reconWR], s = s) # , s=0)
#        self.dataInterp  = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)

# Interpolate data using splines, used for setting square array as input for recon function.
# As interp(), but for ROI - hack job, should rewrite in a more elegant fashion!!!
def interpROI(self, s = None, plotFlag = False):
    # Set dimension
    dim = self.ROI.data.shape
    self.ROI.dim = [dim[0], dim[1], dim[0]*dim[1]]

    newDim = self.ROI.dimInterp[0].astype(int) # Force to int for linspace etc. 

    # Set value for s, if not passed - choose very roughly by ROI size. If s is too small, interp tends to hang.
    if s is None:
        s = self.ROI.dim[2]*1E-4
        print('Interpolating, s = ', s)
        self.ROI.s = s

    # Set original gridding
    # dims = self.ROI.data.shape

    # Arb axes
    # x, y = np.mgrid[-1:1:(dims[0]*1j), -1:1:(dims[1]*1j)]

    # Real axes
    # x, y = np.meshgrid(self.ROI.wavelengths, self.ROI.fs)
    x, y = np.meshgrid(self.ROI.fs, self.ROI.wavelengths)

    # Interp to newDim
    # Arb units
    # xnew, ynew = np.mgrid[-1:1:(newDim*1j), -1:1:(newDim*1j)]   # Weird - apparently using complex here provides grid inclusive of stop value, see https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.mgrid.html
    # Real units
    # TODO: this currently assumes linear sampling... may not be totally accurate
    self.ROI.fsInterp = np.linspace(self.ROI.fsLim[0], self.ROI.fsLim[1], num = newDim)
    self.ROI.waveInterp = np.linspace(self.ROI.waveLim[0], self.ROI.waveLim[1], num = newDim)
    #xnew, ynew = np.meshgrid(self.ROI.waveInterp, self.ROI.fsInterp)
    xnew, ynew = np.meshgrid(self.ROI.fsInterp, self.ROI.waveInterp)

    tck = interpolate.bisplrep(x, y, self.ROI.data/self.ROI.data.max(), s = s) # , s=0)
    self.ROI.dataInterp = interpolate.bisplev(xnew[0,:], ynew[:,0], tck)
    self.ROI.dataInterp = self.ROI.dataInterp.T

    # Plot interp data if flag is set
    if plotFlag:
        plt.figure()
        plt.subplot(121)
        plt.pcolor(x, y, self.ROI.data)
        plt.colorbar()
        plt.title("Original data.")

        plt.subplot(122)
        plt.pcolor(xnew, ynew, self.ROI.dataInterp)
        plt.colorbar()
        plt.title("Interpolated data.")
        plt.show()
