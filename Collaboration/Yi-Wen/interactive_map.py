#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 23:22:01 2023

@author: yw
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.interpolate import griddata
from skyfield.api import EarthSatellite, load

#常量定義
DATA_PICKLE_SCATTER = '/Users/yw/desktop/file_orbit_and_saa/df_for_scatter.pkl'
DATA_PICKLE_CONTOUR = '/Users/yw/desktop/file_orbit_and_saa/df_for_contour.pkl'
GRID_X_POINTS = 1000
GRID_Y_POINTS = 1000
CONTOUR_LEVELS = 10
CONTOUR_SPECIFIC_LEVEL = 5000

#從pickle文件加載數據
def load_data_from_pickle(pickle_file):
    return pd.read_pickle(pickle_file)

#創建經緯度網格
def create_grid(x_range, y_range, x_points, y_points):
    return np.meshgrid(np.linspace(*x_range, x_points), np.linspace(*y_range, y_points))

#主函數
def main():
    df_scatter = load_data_from_pickle(DATA_PICKLE_SCATTER)
    df_contour = load_data_from_pickle(DATA_PICKLE_CONTOUR)

    #創建經緯度網格並插值數據
    x_range = (0, 360)
    y_range = (-90, 90)
    x_mesh, y_mesh = create_grid(x_range, y_range, GRID_X_POINTS, GRID_Y_POINTS)
    z_mesh = griddata((df_contour['Longitude'], df_contour['Latitude']), df_contour['Integrated SAA Flux'], (x_mesh, y_mesh), method='nearest')

    #繪圖
    fig, ax = plt.subplots()
    ax.scatter(df_scatter['Longitude'], df_scatter['Latitude'], s=1, color='gray')
    contour = ax.contour(x_mesh, y_mesh, z_mesh, levels=CONTOUR_LEVELS, cmap="rainbow")
    ax.contour(x_mesh, y_mesh, z_mesh, levels=[CONTOUR_SPECIFIC_LEVEL], linewidths=1, colors='black')

    xx_all, yy_all = [], []
    for p in contour.collections[0].get_paths():
        v = p.vertices
        xx_all.append(v[:, 0])
        yy_all.append(v[:, 1])

    ax.set_xlim([0, 360])
    ax.set_ylim([-90, 90])

    #創建交互式地圖
    fig = go.Figure()
    for xx, yy in zip(xx_all, yy_all):
        fig.add_trace(go.Scattergeo(lon=xx, lat=yy, mode='lines', line=dict(color='blue', width=1)))
    fig.write_html('SAA_contour.html')

    #TLE
    line1 = '1 92920U 17049A   23141.04166667  .00000000  00000+0  43614-4 0  9991'
    line2 = '2 92920  97.6407 223.1803 0011733 244.4023 141.8465 15.00937976   -30'

    data = load('de421.bsp')
    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)

    num_points = 1000
    times = ts.utc(2023, 7, 12, np.linspace(0, 5, num_points))
    geocentric = satellite.at(times)
    subpoint = geocentric.subpoint()
    longitudes_pred = subpoint.longitude.degrees
    latitudes_pred = subpoint.latitude.degrees

    #標記軌道出現在SAA內的部分
    saa_indices = np.where(z_mesh > CONTOUR_SPECIFIC_LEVEL)
    saa_longitudes = x_mesh[saa_indices]
    saa_latitudes = y_mesh[saa_indices]

    #添加預測軌道和標記
    fig.add_trace(go.Scattergeo(lon=longitudes_pred, lat=latitudes_pred, mode='lines', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scattergeo(lon=saa_longitudes, lat=saa_latitudes, mode='markers', marker=dict(color='red', size=3)))

    fig.write_html('interactive_map.html')

if __name__ == "__main__":
    main()