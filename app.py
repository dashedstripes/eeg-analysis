import pyedflib
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import matplotlib.patches as patches

file_name = 'dataset/S001/S001R03.edf'
f = pyedflib.EdfReader(file_name)
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
  sigbufs[i, :] = f.readSignal(i)


# Function to update the visualization based on the time index
def update_plot(time_index):
    plt.clf()
    plt.imshow(img)
    for i, label in enumerate(signal_labels):
        # Placeholder for actual channel positions
        x, y = i, i # Replace these with actual x, y coordinates
        # Modulate the alpha value based on the signal amplitude at the current time index
        alpha_val = (sigbufs[i, time_index] - min_signal) / (max_signal - min_signal)
        circle = patches.Circle((x, y), radius=5, alpha=alpha_val, color='red')
        plt.gca().add_patch(circle)
    
    plt.axis('off')
    plt.show()

# Load the EEG channel layout image
img = plt.imread('dataset/64_channel_sharbrough.png')

# Find the maximum and minimum signal values for normalization
min_signal = sigbufs.min()
max_signal = sigbufs.max()

# Create the slider widget
slider = widgets.IntSlider(
    value=0,
    min=0,
    max=sigbufs.shape[1] - 1,  # Number of time points
    step=1,
    description='Time Index',
    continuous_update=False
)

# Display the slider and connect the update function to it
widgets.interactive(update_plot, time_index=slider)
