import pyedflib
import numpy as np
import plotly.graph_objects as go
import base64

file_name = "dataset/S001/S001R03.edf"
f = pyedflib.EdfReader(file_name)
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)

# Coordinates for each EEG location on your image (this is dummy data; you'll need to provide the actual coordinates)
eeg_coords = {
    "Fc5.": (100, 100),
    "Fc3.": (200, 100),
    "Fc1.": (100, 100),
    "Fcz.": (100, 100),
    "Fc2.": (100, 100),
    "Fc4.": (100, 100),
    "Fc6.": (100, 100),
    "C5..": (100, 100),
    "C3..": (100, 100),
    "C1..": (100, 100),
    "Cz..": (100, 100),
    "C2..": (100, 100),
    "C4..": (100, 100),
    "C6..": (100, 100),
    "Cp5.": (100, 100),
    "Cp3.": (100, 100),
    "Cp1.": (100, 100),
    "Cpz.": (100, 100),
    "Cp2.": (100, 100),
    "Cp4.": (100, 100),
    "Cp6.": (100, 100),
    "Fp1.": (250, 100),
    "Fpz.": (300, 100),
    "Fp2.": (350, 110),
    "Af7.": (100, 100),
    "Af3.": (100, 100),
    "Afz.": (100, 100),
    "Af4.": (100, 100),
    "Af8.": (100, 100),
    "F7..": (100, 100),
    "F5..": (100, 100),
    "F3..": (100, 100),
    "F1..": (100, 100),
    "Fz..": (100, 100),
    "F2..": (100, 100),
    "F4..": (100, 100),
    "F6..": (100, 100),
    "F8..": (100, 100),
    "Ft7.": (100, 100),
    "Ft8.": (100, 100),
    "T7..": (100, 100),
    "T8..": (100, 100),
    "T9..": (100, 100),
    "T10.": (100, 100),
    "Tp7.": (100, 100),
    "Tp8.": (100, 100),
    "P7..": (100, 100),
    "P5..": (100, 100),
    "P3..": (100, 100),
    "P1..": (100, 100),
    "Pz..": (100, 100),
    "P2..": (100, 100),
    "P4..": (100, 100),
    "P6..": (100, 100),
    "P8..": (100, 100),
    "Po7.": (100, 100),
    "Po3.": (100, 100),
    "Poz.": (100, 100),
    "Po4.": (100, 100),
    "Po8.": (100, 100),
    "O1..": (100, 100),
    "Oz..": (100, 100),
    "O2..": (100, 100),
    "Iz..": (100, 100),
}

# Create a figure
fig = go.Figure()

image_filename = "dataset/64_channel_sharbrough.png"
brain_image = base64.b64encode(open(image_filename, "rb").read())

fig = go.Figure(go.Image(source="data:image/png;base64,{}".format(brain_image.decode())))
# fig.show()

# # Set the axes properties
fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
fig.update_yaxes(showgrid=False, zeroline=False, visible=False)


global_min = np.min(sigbufs)
global_max = np.max(sigbufs)


# Function to create scatter for a given timestep
def create_scatter_for_timestep(timestep):
    return go.Scatter(
        x=[eeg_coords[label][0] for label in signal_labels],
        y=[eeg_coords[label][1] for label in signal_labels],
        mode="markers",
        marker=dict(
            size=20,
            color=sigbufs[
                :, timestep
            ],  # Set the color of markers to the EEG signal values at the given timestep
            colorscale="Viridis",  # Colorscale for the EEG signal strength
            showscale=True,
            cmin=global_min,  # Set the fixed minimum for the color scale
            cmax=global_max,
        ),
        text=signal_labels,
    )

# add traces for every step
for i in range(sigbufs.shape[1] // 100):  # Assuming the second dimension of sigbufs is the number of timesteps
    fig.add_trace(create_scatter_for_timestep(i * 100))


initial_visibility = [True] + [False] * (len(fig.data) - 1)

steps = []
for i in range(sigbufs.shape[1] // 100):  # Assuming the second dimension of sigbufs is the number of timesteps
    step = dict(
        method="update",
        args=[
            {"visible": initial_visibility.copy()},
            {"title": f"Timestep: {i}"},
        ],  # layout attribute
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)

sliders = [dict(active=0, currentvalue={"prefix": "Timestep: "}, steps=steps)]

fig.update_layout(sliders=sliders)

fig.show()
