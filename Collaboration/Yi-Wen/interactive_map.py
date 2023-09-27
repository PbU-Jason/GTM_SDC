#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:51:08 2023

@author: yw
"""

import numpy as np
from skyfield.api import EarthSatellite, load
import pandas as pd
import scipy as sp
from scipy.interpolate import griddata
import plotly.graph_objects as go
import matplotlib.pyplot as plt

CONTOUR_SPECIFIC_LEVEL = 5000

# TLE data for the satellite
line1 = '1 92920U 17049A   23141.04166667  .00000000  00000+0  43614-4 0  9991'
line2 = '2 92920  97.6407 223.1803 0011733 244.4023 141.8465 15.00937976   -30'

# Load the satellite data
data = load('de421.bsp')
ts = load.timescale()
satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)

# Number of points for the satellite's path
num_points = 5000
times = ts.utc(2023, 7, 12, np.linspace(0, 5, num_points))
geocentric = satellite.at(times)
subpoint = geocentric.subpoint()
longitudes = subpoint.longitude.degrees
latitudes = subpoint.latitude.degrees

# Load your contour data and grid it as needed
df_for_contour = pd.read_pickle(
    '/Users/yw/desktop/file_orbit_and_saa/df_for_contour.pkl')

# The original data
x_orig = np.asarray(df_for_contour['Longitude'].tolist())
y_orig = np.asarray(df_for_contour['Latitude'].tolist())
z_orig = np.asarray(df_for_contour['Integrated SAA Flux'].tolist())

# Make a grid
x_arr = np.linspace(0, 360, 500)
y_arr = np.linspace(-90, 90, 500)
x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='nearest')

# Create the contour plot
fig = go.Figure()

xx_all = []
yy_all = []

contour = plt.contour(x_mesh, y_mesh, z_mesh, levels=[
                      CONTOUR_SPECIFIC_LEVEL], linewidths=2, colors='k')

for p in contour.collections[0].get_paths():
    v = p.vertices
    xx = v[:, 0]
    xx_all.append(xx)
    yy = v[:, 1]
    yy_all.append(yy)
for i in range(len(xx_all)):
    fig.add_trace(
        go.Scattergeo(lat=yy_all[i],lon=xx_all[i],mode='lines',line=dict(color='blue', width=2),showlegend=False))

# Record entry and exit points
entry_exit_points = []

inside_contour = False

for i in range(num_points):
    satellite_longitude = longitudes[i]
    satellite_latitude = latitudes[i]
    interpolated_flux = griddata(
        (x_orig, y_orig), z_orig, (satellite_longitude, satellite_latitude), method='nearest')

    # Check if certain conditions are met
    if interpolated_flux >= CONTOUR_SPECIFIC_LEVEL:
        if not inside_contour:
            entry_exit_points.append(("Enter", satellite_longitude, satellite_latitude, times.utc_iso()[i]))
            inside_contour = True
    else:
        if inside_contour:
            entry_exit_points.append(("Exit", satellite_longitude, satellite_latitude, times.utc_iso()[i]))
            inside_contour = False

# Plot satellite's path
fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
              mode='markers', marker=dict(color='grey', size=2)))

fig.update_layout(width=1200, height=800)

for data in entry_exit_points:
    if data[0] == "Enter":
        event_color = 'green'
    elif data[0] == "Exit":
        event_color = 'red'
    else:
        continue

    hover_text = f"位置: {data[1]}, {data[2]}<br>時間: {data[3]}"
    fig.add_trace(go.Scattergeo(
        lon=[data[1]],
        lat=[data[2]],
        mode='markers',
        marker=dict(color=event_color, size=5),
        text=[hover_text],
        hoverinfo='text'
    ))
    
# Save the figure as an HTML file
fig.write_html('interactive_map.html')

# Print entry and exit points
print("Entry and Exit Points:")
for event, lon, lat, time in entry_exit_points:
    print(f"{event} - Longitude: {lon}, Latitude: {lat}, Time: {time}")
