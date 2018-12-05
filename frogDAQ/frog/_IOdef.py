# File IO routines
# types implemented:
#   'p' for pickle
#   'f' for .fr (Trebino group)

import pickle
import os, sys
from datetime import datetime as dt # Import datetime.datetime for now() function

def saveFrog(self, fileName = None, saveType = None, savePath = None):
    #TODO: save method - set default as pickle.
    #TODO: set save variables in init?

    # Set fileName, defaults to time-stamp version in current dir
    # TODO: decide on protocol here - for resaving as .frg it's good to keep the fileName, but not if just recording data.
    if fileName is None and self.fileName is None:
        timeString = dt.now()
        self.fileName = timeString.strftime('%Y-%m-%d_%H-%M-%S') + '_frog'
    elif fileName is not None:
        self.fileName = fileName
    else:
        pass

    if savePath is None and self.savePath is None:
        self.savePath = os.getcwd()
    elif savePath is not None:
        self.savePath = savePath
    else:
        pass


    # Change saveType if set, otherwise use default
    if saveType is not None:
        self.saveType = saveType

    # Write data
    # TODO: At the moment can't save full object with pickle?  Throws an error. For now just grab relevant data
    if self.saveType == 'p':
        with open(os.path.join(self.savePath, self.fileName + '.pkl'), 'wb') as fout:
            pickle.dump(self.wavelengths, fout)
            pickle.dump(self.fs, fout)
            pickle.dump(self.data, fout)

#        if self.saveType == 'np':
#            np.save(savename,self.data)

    # Write data as ".frg" frog format, as defined by Trebino group Frog code
    # Header line: dim_t dim_lam dt dlambda centreLambda
    # Data: array, space delimited
    if self.saveType == 'f':
        # Raw data
        with open(os.path.join(self.savePath, self.fileName + '.frg'), 'w') as fout:
            print(f'{self.data.shape[1]}\t{self.data.shape[0]}\t{(np.abs(self.fs[1]-self.fs[0]))}\t{(np.abs(self.wavelengths[1]-self.wavelengths[0]))}\t{(self.wavelengths[np.int(np.round(self.wavelengths.shape[0]/2))])}\n',file=fout)
            np.savetxt(fout,self.data,fmt='%.2f')

        # ROI if set
        if self.ROI.waveRange is not None:
            with open(os.path.join(self.savePath, self.fileName + '_ROI.frg'), 'w') as fout:
                print(f'{self.ROI.data.shape[1]}\t{self.ROI.data.shape[0]}\t{np.abs(self.ROI.fs[1]-self.ROI.fs[0])}\t{np.abs(self.ROI.wavelengths[1]-self.ROI.wavelengths[0])}\t{self.ROI.wavelengths[np.int(np.round(self.ROI.wavelengths.shape[0]/2))]}\n',file=fout)
                np.savetxt(fout,self.ROI.data,fmt='%.2f')

            with open(os.path.join(self.savePath, self.fileName + '_ROIinterp.frg'), 'w') as fout:
                print(f'{self.ROI.dataInterp.shape[1]}\t{self.ROI.dataInterp.shape[0]}\t{np.abs(self.ROI.fsInterp[1]-self.ROI.fsInterp[0])}\t{np.abs(self.ROI.waveInterp[1]-self.ROI.waveInterp[0])}\t{self.ROI.waveInterp[np.int(np.round(self.ROI.waveInterp.shape[0]/2))]}\n',file=fout)
                np.savetxt(fout,self.ROI.dataInterp,fmt='%.2f')

# Read in data, overwrites current data
# TODO: Note this code works for cases where fileName includes full path, since os.path.join() will just take last item. Bug or feature?
def loadFrog(self, fileName, saveType = None, savePath = None):

    self.fileName = fileName

    # Set path, default to working dir
    if savePath is not None:
        self.savePath = savePath
    else:
        self.savePath = os.getcwd()

    # Change saveType if set, otherwise use default
    if saveType is not None:
        self.saveType = saveType

    # Read in previously saved data, pickle only so far
    if self.saveType == 'p':
        with open(os.path.join(self.savePath, self.fileName + '.pkl'), 'rb') as fout:
            self.wavelengths = pickle.load(fout)
            self.fs = pickle.load(fout)
            self.data = pickle.load(fout)
