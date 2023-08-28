#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 13:45:26 2023

@author: yw
"""

import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import EarthSatellite, load
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter

#TLE
line1 = '1 92920U 17049A   23141.04166667  .00000000  00000+0  43614-4 0  9991'
line2 = '2 92920  97.6407 223.1803 0011733 244.4023 141.8465 15.00937976   -30'

#加載天體數據
data = load('de421.bsp')
ts = load.timescale()

#創建衛星對象
satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)

#計算軌道點的數量
num_points = 1000

#計算軌道上的位置點
times = ts.utc(2023, 7, 12, np.linspace(0, 5, num_points))
geocentric = satellite.at(times)
subpoint = geocentric.subpoint()

#提取經度和緯度
longitudes = subpoint.longitude.degrees
latitudes = subpoint.latitude.degrees

#創建地圖投影
fig = plt.figure(figsize=(20, 20))
ax = plt.axes(projection=ccrs.PlateCarree())

#添加地圖背景
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=0.5)

#設置坐標軸範圍
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

#添加經度和緯度刻度
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=1)
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

#繪製軌道
ax.plot(longitudes, latitudes, '.', markersize=1, color='red', linewidth=0.5, transform=ccrs.Geodetic())

#添加標題和標籤
plt.title(" ")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

#顯示圖形
plt.show()
