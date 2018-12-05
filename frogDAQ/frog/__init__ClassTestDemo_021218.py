# Test __init__ class behaviour with multiple files - this works.
# See https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files

# Init frog class based on local definitions
class frog():
    # Load definitions
    from ._temporalDef import delays, fsmm

    def __init__(self):
        self.scanRange=[-100, 100]
        self.delays()


#     #Init object - set empty params, and some sensible defaults.
#     def __init__(self, devices, stage, devID=0, scanRange=[-100, 100], t0=0, intT=100000, frames=1):
#
#         # Set hardware
#         self.devices = devices
#         self.devID = 0
#         self.stage = stage
#
#         # Set parameters - motion
#         self.t0=t0
#         self.scanRange=scanRange
#
#         # Set parameters - spectrum
#         self.intT=intT
#         self.frames=frames
#
#         # Get wavelength range from spectrometer
#         if self.devices is not None:
# #            import OOfunc as OO
#             _, self.wavelengths = OO.capture(devices, devID=devID, frames=1)
#             self.dark = np.zeros(len(self.wavelengths))
#         else:
#             self.wavelengths = np.zeros(128)
#
#         # Set delays
#         self.delays()
#         # self.data = np.zeros((len(self.wavelengths),len(self.mm)))
#
#         # Set params for reconstruction
#         self.reconWR = (self.wavelengths[0],self.wavelengths[-1])   # Wavelength range, default to full spectrum
#         self.reconMode = 'blind'
#         self.reconIter = 50
#         self.gatepulse = None
#         self.reconSVD = 'svd'   # Set 'svd' or 'power'
#
#         # Data save parameters
#         self.fileName = None
#         self.savePath = None
#         self.saveType = 'p'     # Set default to pickle object
#
#         # Init data structures for ROI and recon
#         # TODO: Set recon data structure. Nest recon method in subclass too?
#         self.ROI = self.setROI()
#         # self.reconData = self.setRecon()
