#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from skyfield.api import EarthSatellite, load
import plotly.graph_objects as go
from scipy.interpolate import griddata


line1 = '1 92920U 17049A   23141.04166667  .00000000  00000+0  43614-4 0  9991'
line2 = '2 92920  97.6407 223.1803 0011733 244.4023 141.8465 15.00937976   -30'

data = load('de421.bsp')
ts = load.timescale()

satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)

num_points = 1000

times = ts.utc(2023, 7, 12, np.linspace(0, 5, num_points))
geocentric = satellite.at(times)
subpoint = geocentric.subpoint()

longitudes = subpoint.longitude.degrees
latitudes = subpoint.latitude.degrees

fig = go.Figure()

fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes, mode='markers', marker=dict(color='red', size=1)))

fig.write_html('/Users/yw/desktop/interactive_plot.html')

