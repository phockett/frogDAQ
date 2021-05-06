# 06/05/21 Added imports here as they seem to be broken currently (testing in Python 3.9)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Plot data. Optional limits can be passed as lists, defaults to full range
def plot(self, fsLim = None, waveLim = None, fig = None):

    # Crop data for plotting, this sets elements in ROI subclass
    self.ROI = self.setROI(fsLim = fsLim, waveLim = waveLim)
    self.crop()

    # Plot

    # Set new figure if one is not passed
    if fig is None:
        fig = plt.figure(figsize=(16,12))

    fig.canvas.set_window_title('Frog v0.3')

    # ax = fig.add_subplot(1,1,1)
    gs = GridSpec(6,6)

    # 2D image
    ax1 = plt.subplot(gs[:-1,:-1])
    ax1.imshow(self.ROI.data, aspect='auto', extent = [self.ROI.fsLim[0],self.ROI.fsLim[1],self.ROI.waveLim[1],self.ROI.waveLim[0]], interpolation='gaussian')
    ax1.axes.xaxis.tick_top()
    ax1.set_xlabel('t/fs')
    ax1.axes.xaxis.set_label_position('top')
    ax1.set_ylabel('$\lambda$/nm')

    # Integrated over spectrum
    ax2 = plt.subplot(gs[-1,:-1])
    ax2.plot(self.ROI.fs,self.ROI.data.sum(axis=0)/np.max(self.ROI.data.sum(axis=0)))
    ax2.set_xlim(self.ROI.fsLim)
    ax2.axes.grid()
    ax2.set_xlabel('t/fs')

    # Integrated over time
    # TODO: fix axis scaling... weird bug with axis dirn here, works except for defaults...???
    ax3 = plt.subplot(gs[:-1,-1])
    ax3.plot(self.ROI.data.sum(axis=1)/np.max(self.ROI.data.sum(axis=1)),self.ROI.wavelengths)
    # ax3.set_ylim(waveLim)
    ax3.set_ylim([self.ROI.waveLim[1],self.ROI.waveLim[0]])   # Reverse order of limits to match axis to main plot
    # ax3.plot(self.data.sum(axis=1),np.arange(0,self.data.shape[0]))
    # ax3.invert_yaxis()
    ax3.axes.yaxis.tick_right()
    ax3.axes.grid()
    ax3.set_ylabel('$\lambda$/nm')
    ax3.axes.yaxis.set_label_position('right')


    # With rotation - not really the right thing to do, should just be able to switch axes...
    # https://stackoverflow.com/questions/22540449/how-can-i-rotate-a-matplotlib-plot-through-90-degrees#28372659
    # base = plt.gca().transData
    # rot = transforms.Affine2D().rotate_deg(90)
    # ax3 = plt.subplot(gs[:-1,-1])
    # ax3.plot(self.data.sum(axis=1), transform = rot+base)

    # Title with fileName, if set
    if self.fileName is not None:
        fig.suptitle('Frog scan \n\n Data: ' + self.fileName)


    plt.show()
