# -*- coding: utf-8 -*-
"""

Functions for Ocean Optics spectrometers with pySeabreeze

Prerequisites:
    - pySeabreeze: https://github.com/ap--/python-seabreeze

To do:
    - Convert to class-based structure
    - Implement save function

06/09/18    Added waveLim passing functionality, and (basic) keypress exit - still needs some work.
[Missing history]

This code:
    Paul Hockett
    paul@femtolab.ca
    femtolab.ca
    github.com/phockett  [not yet posted]

Created on Fri Aug  3 09:44:13 2018
@author: femtolab
"""

try:
    import seabreeze.spectrometers as sb
except ImportError as e:
    if e.msg != "No module named 'seabreeze'":
        raise
    print('* Seabreeze not found, Ocean Optics Spectrometers not available. ')

import numpy as np
import matplotlib.pyplot as plt

global keyPressed


# def run(devList, devID=0, intT=100000, frames=50, avg=10, pltPause=0.1, refSpec=None, dispSpec=None):
# Function to run an OO spectrometer on a loop, with moving average
# Inputs:
#   - devList       list of available devices returned by seabreeze
#   - devID         the device to use
#   - intT          the integration time (int, units are microseconds)
#   - frames        frames to capture (int)
#   - waveLim       wavelength range for plotting [lambda1 lambda2], default is full wavelength range
#   - avg           frames for moving average (int)
#   - pltPause      Pause between frames (float, units are seconds)
#   - refSpec       Referecnce (dark) spectrum for subtraction
#   - dispSpec      Additional spectra for display on plot
#
# Default: 10Hz refresh with maximal int. time (100ms)
#
# Special cases:
#   - frames=1      Return one frame of data, no averaging.
#
# Returns:
#   - intensities   2D np array containing last set of traces, size=(avg,pixels)
#   - wavelength    1D np array of wavelengths, size=pixels
#
# TODO: Modes for specific cases (sets of parameters) - once this has been used a bit!
# TODO: Hotkey stop from plotting window.
#
def run(devList, devID=0, intT=100000, frames=0, avg=10, waveLim = None, pltPause=0.1, refSpec=None, dispSpec=None):

    print('Running capture, hit q to quit, any other key to stop.')

    # Set infinte running mode
    if frames == 0:
        frames = 1000000000

    # Init devices
    spec = sb.Spectrometer(devList[devID])

    # Set integration time
    spec.integration_time_micros(intT)

    # Set refSpec default
    if refSpec is None:
        refSpec = np.zeros(spec.pixels)

    # Reset plot refresh rate if it's less than int. time - this doesn't seem to be required, just get repeated data in cases pltPause<intT?
#    if (intT*1e-6)>pltPause:
#        pltPause = intT*1e-6

    # Set figure
    fig = plt.figure(figsize=(16,12))
    fig.canvas.set_window_title('OO Capture')
    ax = fig.add_subplot(1,1,1)

    # Event handlers
    global keyPressed
    keyPressed = None   # Clear global key buffer
    runFlag = True

    # Grab a spectrum to init var
    wavelength = spec.wavelengths()
    intensities = spec.intensities() - refSpec

    if frames==1:
        ax.plot(wavelength, intensities,'r')

    else:
        try:
            # Loop over range for moving average and plot
            for i in range(frames):
    #        for i in (i in range(frames) if runFlag):

                ax.clear()
                # ax.plot(wavelength, intensities.T,'g')    # Stacks plots 1:avg

                if i>0:         # Plot with moving avg., make sure dimension >1
                    # Styles...
                    # (1) Basic
                    #   ax.plot(wavelength, intensities.T, wavelength, intensities.mean(axis=0),'r')
                    # (2) Add shaded std. bounds (with multiplier)
                    #   m=3
                    #   ax.fill_between(wavelength, intensities.mean(axis=0)-(m*intensities.std(axis=0)), intensities.mean(axis=0)+(m*intensities.std(axis=0)))
                    # (3) Plot and add std. as error bar
                    #   ax.errorbar(wavelength, intensities.mean(axis=0), yerr = intensities.std(axis=0), fmt = 'r', errorevery = 10)
                    # (4) Plot with fill_between(), requires loop and n>0
                    [ax.fill_between(wavelength, intensities[n,:], intensities[n,3], facecolor='green', alpha = 0.5/avg) for n in range(intensities.shape[0])]
                    # Add moving average
                    ax.plot(wavelength, intensities.mean(axis=0),'r')

    #                if spec.model == 'USB2000PLUS':     # For Flame, cut at 180nm to avoid intensity spikes, and reset y range.
    #                                                    # May be necessary for other cases?
    #                    plt.xlim(180,870)
    #                    plt.ylim(intensities[:,2:].min(),intensities[:,2:].max())


                if "any" in dir(dispSpec):      # Test for np array type via dir(var) as proxy
                    ax.plot(wavelength,dispSpec.T)  # Assumes 2D and as per intensities defined above


                # Additioanl plot style(s) and formatting
                ax.axes.grid()
                if waveLim is not None:
                    ax.set_xlim(waveLim)


                plt.pause(pltPause)      # Use plt.pause(), not time.sleep(), to allow UI control

                # Check for key press
                cid = fig.canvas.mpl_connect('key_press_event', on_key)

                # TODO: fix this ugly code, and proper event handling. Checking for specific key doesn't work, why??? (Also the case if tested in event handler.)
                # if keyPressed is 'e':     # DOESN'T WORK???
                # if i>10:                  # Works
                if keyPressed is not None:  # Works
                    print(keyPressed)
                    print('Key pressed - stopping capture')
                    raise StopIteration

                    # Close spectrometer and return current intensities list if user quits - THIS doesn't work... not sure why, something about iterator behaviour?
                    #spec.close()
                    #return  intensities, wavelength
                    #print('return')


                # Stack spectra
                intensities = np.vstack((intensities,spec.intensities()-refSpec))

                # Treat as a buffer, remove oldest values
                if i>(avg-2):
                    intensities = intensities[1:,:]

               # print(i, keyPressed)

        except StopIteration:
                spec.close()
                return  intensities, wavelength


    # Close spectrometer and return current intensities list
    spec.close()
    return  intensities, wavelength

# Save data
def save():
    # print("Not yet implemented")
    pass

# Key press handler for Matplotlib, will use for save/quit free-running case functionality...
# See https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.KeyEvent
def on_key(event):
    global keyPressed
   # print('you pressed', event.key, event.xdata, event.ydata)
    keyPressed = event.key


# def capture (as run(), but no plotting, and return all frames)... could do with a flag?
def capture(devList, devID=0, intT=100000, frames=50, refSpec=None):

    # Init devices
    spec = sb.Spectrometer(devList[devID])

    # Set integration time
    spec.integration_time_micros(intT)

    # Set refSpec default
    if refSpec is None:
        refSpec = np.zeros(spec.pixels)

    # Grab a spectrum to init var
    wavelength = spec.wavelengths()
    intensities = spec.intensities() - refSpec

    # Loop over frames
    for i in range(frames-1):
         # Stack spectra
         intensities = np.vstack((intensities,spec.intensities()-refSpec))

    # Close spectrometer and return current intensities list
    spec.close()
    return intensities, wavelength
