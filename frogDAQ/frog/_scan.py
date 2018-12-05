
# Run a frog scan

# Frog scan, no plotting by deafult
def scan(self, plotFlag=None):

    print('*** Running FROG scan, ' + str(len(self.fs)) + ' points')

    if plotFlag is not None:
        fig = plt.figure(figsize=(16,12))   # Set figure

    # Loop over delays and get data
    for n in range(len(self.mm)):

        # Set stage position (absolute), wait for motion to finish (MAY NOT BE WORKING?)
        # For testing, set stage = None and skip motion
        if self.stage is None:
            pass
        else:
            self.stage.move_to(self.mm[n],wait=True)

        # Report - could do with some better formatting here!
        print('Position: \t' + str(self.fs[n]) + ' fs \t(' + str(self.mm[n]) + ' mm) \t Step ' + str(n+1) + ' of ' + str(len(self.mm)))

        if self.devices is not None:
            # Grab spectrum
            intensities,_ = OO.capture(self.devices, devID=self.devID, intT=self.intT, frames=self.frames)

            if self.frames > 1:
                self.data[:,n] = intensities.sum(axis=0) - self.dark
            else:
                self.data[:,n] = intensities - self.dark

            # Plot each delay - at the moment, this doesn't work, just shows a blank figure during capture (even with slow capture). Update/focus issue?
            #TODO: May need to change to axes update style, as per OOfunc code, but this will need a rewrite of plotting method.
#                if plotFlag is not None:
#                    self.plot(fig = fig)

        else:
            pass

    # Plot after capture, since this is shonky otherwise.  Better method for online plotting...?  Actually, might just be an ax clear issue?
    if plotFlag is not None:
        self.plot(fig = fig)
#            # Set figure
#            fig = plt.figure(figsize=(16,12))
#            fig.canvas.set_window_title('Frog v0.1')
#            ax = fig.add_subplot(1,1,1)
#            ax.imshow(self.data, aspect='auto')
#            plt.show()

    # Return to t0
    self.stage.move_to(self.t0, wait=True)
