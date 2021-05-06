# 06/05/21 Added imports here as they seem to be broken currently (testing in Python 3.9)
import numpy as np
import matplotlib.pyplot as plt

# Import froglib for frog reconstruction routines
try:
    # sys.path.append(os.path.join(os.curdir,'froglib-master'))      # Set explicit path if desired
    import froglib as frlib
except ImportError as e:
    if e.msg != "No module named 'froglib'":
        raise
    print('* Froglib not found, FROG reconstruction routines not available. ')


class setRecon():
    """Class for reconstruction params & resutls.

    Currently assumes froglib, and has settings to match.
    """
    def __init__(self, WR = None):

        self.WR = WR   # Wavelength range

        self.mode = 'blind'
        self.SVD = 'svd'   # Set 'svd' or 'power'
        self.iterMax = 50

        self.gp = None
        self.sp = None


 #*** FROG reconstruction using froglib
#FIXME: currently requires SQUARE array for measurements, and power of 2 size, added in a very ugly fashion. Adding wavelength selectrion range might help here?
#FIXME: Works OK with small input array (100x100), but seems to hang for larger arrays, regardless of output size - issues with crop? AH, issue with s, now set to scale with ROI size.
def reconFL(self, waveLim = None, fsLim = None, dimInterp = None):

    # Crop data to specified wavelength range if set
    # if wavelengths is not None:
    #    self.reconWR = np.logical_and(self.wavelengths >= wavelengths[0], self.wavelengths <= wavelengths[1])     # Outputs logical vector, size self.wavelengths
    # else:
    #    self.reconWR = np.ones(self.wavelengths.shape[0], dtype = bool )

#        # Check dims - recon code needs pow(2), square image
#        if self.data[self.reconWR].shape[0] != self.data[self.reconWR].shape[1]:
#
#            # TODO: 27/08/18 Interp routine fixed, but now issue with data comparison later!
#            # Set new size - downsample to min axis size
#            newDim = 2**np.ceil(np.log2(np.min(self.data[self.reconWR].shape)))   # For power of 2
#            # newDim = np.min(self.data[self.reconWR].shape)
#            print(newDim)
#            self.interp(newDim)
#
#            # Run recon - interp data
#            self.reconRes = frlib.simplerec(self.dataInterp, iterations=self.reconIter, mode=self.reconMode)
#
#        else:
#            # Run recon - raw data
#            self.reconRes = frlib.simplerec(self.data[self.reconWR], iterations=self.reconIter, mode=self.reconMode)
#
#        # Plot results
#        frlib.simplerecresult(self.data[self.reconWR], self.reconRes, wRange = self.wavelengths[self.reconWR], tRange = self.fs)
#        plt.show()

    #*** UPDATED code 27/08/18
    # Now use self.crop(), already has routine for selection of limits etc.

    # Crop data, this sets elements in ROI subclass
    self.ROI = self.setROI(fsLim = fsLim, waveLim = waveLim, dimInterp = dimInterp)
    # Cropped data set as self.ROI.data
    print('Cropping')
    self.crop()
    print('Cropped')

    # Check dims - recon code needs pow(2), square image: interpolate to resize if necessary
    if self.ROI.data.shape[0] != self.ROI.data.shape[1]:
        # Run interp routine to return interpolated square array for recon code
        if self.ROI.dimInterp is None:
            self.ROI.dimInterp = 2**np.ceil(np.log2(np.min(self.ROI.data.shape)))

        self.ROI.dimInterp = [self.ROI.dimInterp, self.ROI.dimInterp, self.ROI.dimInterp**2]
        print('Resizing ROI to square array: ', self.ROI.dimInterp)
        self.interpROI()

    # TODO: very ugly... use a flag and/or recon structure here?
    else:
        self.ROI.dataInterp = self.ROI.data
        self.ROI.waveInterp = self.ROI.wavelengths
        self.ROI.fsInterp = self.ROI.fs

    # Run recon - pass data or sqrt(data) for fitting ("amplitude" data)
    # 06/05/21 - removed self.reconIter
    self.reconRes = frlib.simplerec(self.ROI.dataInterp, iterations=self.recon.iterMax,
                                    mode=self.recon.mode, gatepulse = self.recon.gp, svd = self.recon.SVD)
    # self.reconRes = frlib.simplerec(np.sqrt(self.ROI.dataInterp+np.abs(np.min(self.ROI.dataInterp))), iterations=self.reconIter, mode=self.reconMode, gatepulse = self.gatepulse, svd = self.reconSVD)

    # Plot results
    # frlib.simplerecresult(self.ROI.dataInterp, self.reconRes, wRange = self.ROI.wavelengths, tRange = self.ROI.fs)
    # frlib.simplerecresult(self.ROI.dataInterp, self.reconRes, wRange = self.ROI.waveInterp, tRange = self.ROI.fsInterp)
    frlib.simplerecresult(self.ROI.dataInterp, self.reconRes)   # wRange and tRange only supported in modified froglib code, not original.
    plt.show()
