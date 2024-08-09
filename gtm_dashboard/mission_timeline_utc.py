#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:30:40 2023

@author: jasonpbu
"""

### package ###
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from skyfield.api import EarthSatellite, load

import shapely
from shapely.geometry import LineString, Point, Polygon
from scipy import spatial
#====================

### function ###
def load_tle(file):
    
    # Open and extract info.
    tle = []
    with open(file) as f:
        for line in f:
            if line[0] == '1': # line 1
                tle.append(line)
            if line[0] == '2': # line 2
                tle.append(line)
    
    return tle

def calculate_orbit_eclipse(tle, utc, mins):
    
    ts = load.timescale(builtin=True)
    minutes = np.arange(utc[4], utc[4]+mins, 0.5)
    times = ts.utc(utc[0], utc[1], utc[2], utc[3], minutes, utc[5])
    
    satellite = EarthSatellite(tle[0], tle[1])
        
    # Calculate orbit
    geocentric = satellite.at(times)
    subpoint = geocentric.subpoint()
    orbit_lon = subpoint.longitude.degrees
    orbit_lat = subpoint.latitude.degrees
    orbit_alt = subpoint.elevation.km
    orbit = np.column_stack((orbit_lon, orbit_lat))
    
    Re = 6378.137 #km

    data  = load('de421.bsp')
    Earth = data['earth']
    Sun   = data['sun']
    Sat   = Earth + satellite

    sunpos, earthpos, satpos = [thing.at(times).position.km for thing in (Sun, Earth, Sat)]

    sunearth, sunsat         = earthpos-sunpos, satpos-sunpos

    sunearthnorm, sunsatnorm = [vec/np.sqrt((vec**2).sum(axis=0)) for vec in (sunearth, sunsat)]

    angle                    = np.arccos((sunearthnorm * sunsatnorm).sum(axis=0))

    sunearthdistance         = np.sqrt((sunearth**2).sum(axis=0))

    sunsatdistance           = np.sqrt((sunsat**2).sum(axis=0))

    limbangle                = np.arctan2(Re, sunearthdistance)

    is_sunlight = []
    for idx, value in enumerate(angle):
        is_sunlight.append(((angle[idx] > limbangle[idx]) or (sunsatdistance[idx] < sunearthdistance[idx])))
    
    return times, orbit, is_sunlight, minutes, orbit_alt

def circle_saa(file, level):
    
    # Load pkl as df
    df = pd.read_pickle(file)
    
    # Extract useful data
    x_orig = np.array((df['Longitude'][df['Longitude']>180]-360).tolist() + df['Longitude'][df['Longitude']<=180].tolist())
    y_orig = np.array(df['Latitude'][df['Longitude']>180].tolist() + df['Latitude'][df['Longitude']<=180].tolist())
    z_orig = np.array(df['Integrated SAA Flux'][df['Longitude']>180].tolist() + df['Integrated SAA Flux'][df['Longitude']<=180].tolist())
     
    # Make a grid
    x_arr          = np.linspace(-180, 180, 500)
    y_arr          = np.linspace(-90, 90, 500)
    x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)
     
    # Grid the values
    z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='nearest')
    
    # Find contour figure
    fig, ax = plt.subplots(dpi=300)
    contour = ax.contour(x_mesh, y_mesh, z_mesh, levels=[level])
    # plt.show()
    plt.close()
    
    # Collect all contour
    xx_all = []
    yy_all = []
    for p in contour.collections[0].get_paths():
        v = p.vertices
        xx = v[:,0]
        xx_all.append(xx)
        yy = v[:,1]
        yy_all.append(yy)
    
    # Extract main two contours
    saa_lon = max(xx_all, key=len).tolist()
    saa_lat = max(yy_all, key=len).tolist()
    saa = np.column_stack((np.array(saa_lon), np.array(saa_lat)))
    
    return saa, df

def in_saa(time, line_saa, line_orbit):
    
    # Split orbit and time
    splitted_orbit = []
    splitted_time = []
    jump_arg = np.where(np.diff(line_orbit[:, 0]) > 0)[0]+1
    splitted_orbit.append(line_orbit[:jump_arg[0]])
    splitted_time.append(time[:jump_arg[0]])
    for jump_idx, jump in enumerate(jump_arg):
        if jump_idx == len(jump_arg)-1:
            splitted_orbit.append(line_orbit[jump:])
            splitted_time.append(time[jump:])
        else:
            splitted_orbit.append(line_orbit[jump:jump_arg[jump_idx+1]])
            splitted_time.append(time[jump:jump_arg[jump_idx+1]])
    
    # Run all orbit
    all_in_out_times = []
    intersection_x = []
    intersection_y = []
    for orbit_idx, orbit in enumerate(splitted_orbit):
        
        nomal_flag = True
        
        if orbit_idx == 0:
            start_point = Point(orbit[0, 0], orbit[0, 1])
            polygon = Polygon(line_saa)
            nomal_flag = not polygon.contains(start_point)
        
        if orbit_idx == len(splitted_orbit)-1:
            end_point = Point(orbit[-1, 0], orbit[-1, 1])
            polygon = Polygon(line_saa)
            nomal_flag = not polygon.contains(end_point)
        
        # Find intersection
        line1 = LineString(line_saa)
        try:
            line2 = LineString(orbit)
        except:
            line2 = LineString([[-179, 0], [-178, 0]])
        points = line1.intersection(line2)
    
        # Collect intersection
        arg_list = []
        if not isinstance(points, shapely.geometry.linestring.LineString):
            
            if isinstance(points, shapely.geometry.multipoint.MultiPoint):
                for point in points.geoms:
                    intersection_x.append(point.x)
                    intersection_y.append(point.y)
                    
                    # Find the nearest info
                    nearest_idx = spatial.KDTree(orbit).query([point.x, point.y])[1]
                    arg_list.append(nearest_idx)
                    
            if isinstance(points, shapely.geometry.point.Point):
                intersection_x.append(points.x)
                intersection_y.append(points.y)
                
                # Find the nearest info
                nearest_idx = spatial.KDTree(orbit).query([points.x, points.y])[1]
                arg_list.append(nearest_idx)
            
            arg_list.sort() # from min to max
    
            # Pickup all in & out times
            in_out_times = splitted_time[orbit_idx][arg_list].tt.tolist()
            
            if nomal_flag == True:
                
                # Group to out & in
                out_in_times_group = np.array(in_out_times[1:-1]).reshape((int((len(in_out_times)-2)/2), 2))
            
                # Delete gap when new_in - old_out too quick!
                delete_list = []
                for out_in_times_idx, out_in_times in enumerate(out_in_times_group):
                    out_time = out_in_times[0]
                    in_time = out_in_times[1]
                    if (in_time - out_time) < 0.0035: # ~ 5mins (1min ~ tt=0.00069)
                        delete_list.append(out_in_times_idx)
                out_in_times_group = np.delete(out_in_times_group, delete_list, axis=0)
                out_in_times_group = out_in_times_group.flatten().tolist()
            
                # Recover in & out times
                recover_in_out_times = [in_out_times[0]] + out_in_times_group + [in_out_times[-1]]
                all_in_out_times.append(recover_in_out_times)
            
            else:
                
                if orbit_idx == 0:
                    
                    if len(in_out_times) != 1:
                    
                        # Group to out & in
                        out_in_times_group = np.array(in_out_times[:-1]).reshape((int((len(in_out_times)-1)/2), 2))
                    
                        # Delete gap when new_in - old_out too quick!
                        delete_list = []
                        for out_in_times_idx, out_in_times in enumerate(out_in_times_group):
                            out_time = out_in_times[0]
                            in_time = out_in_times[1]
                            if (in_time - out_time) < 0.0035: # ~ 5mins (1min ~ tt=0.00069)
                                delete_list.append(out_in_times_idx)
                        out_in_times_group = np.delete(out_in_times_group, delete_list, axis=0)
                        out_in_times_group = out_in_times_group.flatten().tolist()
                    
                        # Recover in & out times
                        recover_in_out_times = [splitted_time[orbit_idx][0].tt] + out_in_times_group + [in_out_times[-1]]
                        all_in_out_times.append(recover_in_out_times)
                    
                    else:
                        recover_in_out_times = [splitted_time[orbit_idx][0].tt] + in_out_times
                        all_in_out_times.append(recover_in_out_times)
                        
                    
                else:
                    
                    if len(in_out_times) != 1:
                        
                        # Group to out & in
                        out_in_times_group = np.array(in_out_times[1:]).reshape((int((len(in_out_times)-1)/2), 2))
                    
                        # Delete gap when new_in - old_out too quick!
                        delete_list = []
                        for out_in_times_idx, out_in_times in enumerate(out_in_times_group):
                            out_time = out_in_times[0]
                            in_time = out_in_times[1]
                            if (in_time - out_time) < 0.0035: # ~ 5mins (1min ~ tt=0.00069)
                                delete_list.append(out_in_times_idx)
                        out_in_times_group = np.delete(out_in_times_group, delete_list, axis=0)
                        out_in_times_group = out_in_times_group.flatten().tolist()
                    
                        # Recover in & out times
                        recover_in_out_times = [in_out_times[-1]] + out_in_times_group + [splitted_time[orbit_idx][-1].tt]
                        all_in_out_times.append(recover_in_out_times)
                        
                    else:
                        recover_in_out_times = in_out_times + [splitted_time[orbit_idx][-1].tt]
                        all_in_out_times.append(recover_in_out_times)
                        
    # Recover arg and group
    recover_arg_group = np.searchsorted(time.tt, np.array(all_in_out_times))
    
    is_saa = [0] * len(time)
    for arg_range in recover_arg_group:
        is_saa[arg_range[0]: arg_range[1]+1] = [1] * (arg_range[1]+1 - arg_range[0])
    
    return is_saa, intersection_x, intersection_y
#====================
