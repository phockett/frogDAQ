"""
Femtolab FROG DAQ
Demo scripts

See readme.rst for further details.

"""


#%% ********** ESP stage control

# Import
from frogDAQ.stage.newportInit import newportInitComms

# Set serial port for ESP controller
port = '/dev/ttyUSB0'
stageID = 1

# Init stage
esp, stage = newportInitComms(port,stageID)

# Turn on
stage.on()

#%% Example usage...
# Log current position
position = stage.position

# Home search
stage.home_search

# Move
stage.move_to(position)


#%% ********** Spectrometer control

# Imports
from frogDAQ.spec import OOfunc as OO
from frogDAQ.spec.OOinit import OOinit

# Init and test spectrometer(s)

devices = OOinit()


#%% Example usage...

#*** SPECTRA
# Capture 15 frames (no plotting)
intensities,_=OO.capture(devices,frames=15)

# Run spectrometer for 1 capture, then use as reference and run with plotting
dark,_ = OO.capture(devices, frames=1)
intensities,_ = OO.run(devices, frames=20,refSpec=dark)

# Run with previous result as displayed spectra
intensities,_ = OO.run(devices, frames=20,refSpec=dark,dispSpec=intensities)

# Run spectrometer for 100 captures with plotting, 5 frame averaging
intensities,_ = OO.run(devices, frames=100, avg=5)


#%% ********** FROG measurements
# Import frog class
import frogDAQ.frog as fr

# Set current position as t0
t0 = stage.position

# Set up an object - TEST case with stage, t0 = position as defined above
X = fr.frog(devices, stage, devID=devID, t0 = t0, intT=100000, scanRange=[-250, 250],frames=5)

# Set additional delay points
X.delays(points = 128)

# Set dark spectrum
stage.move_to(t0-1.0, wait=True) # For dark scan away from t0
X.darkScan()
#TODO subtraction settings to check.

# Return to t0
stage.move_to(t0, wait=True)

#%% Run a scan (default settings)
X.scan(plotFlag = True)

#%% Save data (defaults to current DIR, datestamp format)
X.save()

#%% View spectra with same settings

# Stage to t0
stage.move_to(t0)

# Set wavelength range of interest
X.ROI.waveLim = [700, 900]

# Run spectrometer, push any key to stop
X.spec()

#%% ********** FROG analysis 
