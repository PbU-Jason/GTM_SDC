#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 00:42:51 2023

@author: yw
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.interpolate import griddata

#常量定義
DATA_PICKLE_SCATTER = '/Users/yw/desktop/file_orbit_and_saa/df_for_scatter.pkl'
DATA_PICKLE_CONTOUR = '/Users/yw/desktop/file_orbit_and_saa/df_for_contour.pkl'
GRID_X_POINTS = 1000
GRID_Y_POINTS = 1000
CONTOUR_LEVELS = 10
CONTOUR_SPECIFIC_LEVEL = 3000

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
    
    #繪製交互式地圖
    fig = go.Figure()
    for xx, yy in zip(xx_all, yy_all):
        fig.add_trace(go.Scattergeo( lon=xx,lat=yy, mode='lines', line=dict(color='blue', width=1)))
    fig.write_html('SAA_contour.html')
    
    
if __name__ == "__main__":
    main()
