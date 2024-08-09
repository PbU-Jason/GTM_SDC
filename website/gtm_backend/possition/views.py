from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

import os
from django.conf import settings

def now_lon_lat(request):

    ### main code ###
    tle = load_tle(os.path.join(settings.BASE_DIR, 'possition/data/FS8B_20230521_0100.nor'))

    import datetime
    now_utc = datetime.datetime.utcnow()
    times, orbit, is_sunlight, minutes, orbit_alt = \
    calculate_orbit_eclipse(tle, 
                            (now_utc.year, 
                            now_utc.month, 
                            now_utc.day, 
                            now_utc.hour, 
                            now_utc.minute, 
                            now_utc.second), 
                            720)

    saa, df = circle_saa(os.path.join(settings.BASE_DIR, 'possition/data/df_for_contour.pkl'), 200000)
    is_saa, intersection_x, intersection_y = in_saa(times, saa, orbit)

    color_list = []
    for time_idx, time in enumerate(minutes):
        if is_sunlight[time_idx] == 1:
            color_list.append('gray')
        else:
            if is_saa[time_idx] == 0:
                color_list.append('green')
            else:
                color_list.append('red')

    # Use plotly to plot world map
    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=saa[:, 0],
            lat=saa[:, 1],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False,
            hoverinfo='none'
            )
        )
    fig.add_trace(
        go.Scattergeo(
            lon=orbit[:, 0],
            lat=orbit[:, 1],
            mode='markers',
            marker=dict(color=color_list, size=5),
            showlegend=False,
            customdata=np.column_stack((np.array(times.utc_strftime()), orbit_alt)),
            hovertemplate=
            "Time: %{customdata[0]}<br>" +
            "Lon: %{lon:.3f} deg<br>" +
            "Lat: %{lat:.3f} deg<br>" +
            "Height: %{customdata[1]:.3f} km" +
            "<extra></extra>",
            hoverlabel=dict(font_size=20),
            )
        )
    fig.add_trace(
        go.Scattergeo(
            lon=[orbit[0, 0]],
            lat=[orbit[0, 1]],
            mode='markers',
            marker=dict(size=10, symbol='cross-thin', line=dict(width=3, color='blue')),
            showlegend=False,
            hoverinfo='none'
            )
        )

    # output fig with div type
    fig.update_layout(height=800)
    plot_json_2d = fig.to_json()
    # plot_div_2d = plot(fig, output_type='div', include_plotlyjs=False)
        
    fig.update_geos(projection_rotation_lon=orbit[0, 0], 
                    projection_rotation_lat=orbit[0, 1],
                    projection_type='orthographic')

    # output fig with div type
    fig.update_layout(margin=dict(l=50, r=50, t=50, b=0), height=800)
    plot_json_3d = fig.to_json()
    # plot_div_3d = plot(fig, output_type='div', include_plotlyjs=False)
    #====================

    return JsonResponse({'alt': f'{np.around(orbit_alt[0], 1)}', 'lon': f'{np.around(orbit[0,0], 3)}', 'lat': f'{np.around(orbit[0,1], 3)}',
    'plot_json_2d': plot_json_2d, 'plot_json_3d': plot_json_3d,})



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

import plotly.graph_objects as go
from plotly.offline import plot
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

    # fig, ax = plt.subplots(dpi=300)
    # contour = ax.contour(x_mesh, y_mesh, z_mesh, levels=20, linewidths=0.5, cmap="RdBu_r")
    # fig.colorbar(contour, ax=ax)
    # plt.show()
    # plt.close()
    
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