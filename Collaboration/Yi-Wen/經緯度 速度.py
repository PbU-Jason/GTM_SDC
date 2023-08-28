#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:08:27 2023

@author: yw
"""

from skyfield.api import EarthSatellite, Topos, load

line1 = '1 92920U 17049A   23141.04166667  .00000000  00000+0  43614-4 0  9991'
line2 = '2 92920  97.6407 223.1803 0011733 244.4023 141.8465 15.00937976   -30'


data = load('de421.bsp')
ts = load.timescale()

satellite = EarthSatellite(line1, line2, name='ISS (ZARYA)', ts=ts)

t = ts.utc(2023, 7, 12, 20, 00, 00)
geocentric = satellite.at(t)

#轉換為地心坐標系
subpoint = geocentric.subpoint()

longitude = subpoint.longitude.degrees
latitude = subpoint.latitude.degrees
speed = geocentric.velocity.km_per_s

print("Longitude:", longitude)
print("Latitude:", latitude)
print("Speed:", speed)
 