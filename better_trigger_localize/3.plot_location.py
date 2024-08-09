#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
import numpy as np
import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.style.use('default')

from pyquaternion import Quaternion

from skyfield.positionlib import Geocentric
from skyfield.api import load, Distance, wgs84

from astropy import units
from astropy.time import Time
from astropy.coordinates import get_sun, SkyCoord
#====================

### variable ###

# GRB properties
# test_fluence = 4e-6 # erg/cm^2
test_fluence = 4e-5 # erg/cm^2
grb_theta = 45 # deg, in mass-model coordinate
grb_phi   = 60 # deg, in mass-model coordinate

table1 = np.array(pd.read_csv('./0.table/linear_big_typical1_response.csv')) # middle big
table2 = np.array(pd.read_csv('./0.table/linear_big_typical2_response.csv')) # hard energy big
table3 = np.array(pd.read_csv('./0.table/linear_big_typical3_response.csv')) # soft energy big

# HSL from 270deg, 100% & 50% to 270deg, 100% & 100%
cmap = np.zeros([256, 4])
cmap[:, 0] = np.linspace(128/256, 255/256, 256) # R start to end
cmap[:, 1] = np.linspace(0/256  , 255/256, 256) # G start to end
cmap[:, 2] = np.linspace(255/256, 255/256, 256) # B start to end
cmap[:, 3] = np.flip(np.linspace(0.9, 0.9, 256)) # A start to end
cmap = ListedColormap(cmap)

#====================

### function ###
def spherical2cartesian(input_theta, input_phi): # [deg]
    output_x = np.sin(input_theta * (np.pi/180)) * np.cos(input_phi * (np.pi/180))
    output_y = np.sin(input_theta * (np.pi/180)) * np.sin(input_phi * (np.pi/180))
    output_z = np.cos(input_theta * (np.pi/180))
    return np.array([output_x, output_y, output_z])

def cartesian2spherical(input_x, input_y, input_z):
    output_theta = np.arctan2(np.sqrt(input_x**2 + input_y**2), input_z) * (180/np.pi) # always work
    output_phi   = np.arctan2(input_y, input_x) * (180/np.pi)
    return np.array([output_theta, output_phi]) # [deg]

def eci2equatorial(input_x, input_y, input_z):
    output_ra  = np.mod(np.arctan2(input_y, input_x) * (180/np.pi), 360) # phi in 0 to 360
    output_dec = np.arctan2(input_z, np.sqrt(input_x**2 + input_y**2)) * (180/np.pi) # theta in -90 to 90
    return output_ra, output_dec # [deg]
#====================

### main ###

# Load trigger output to extract bkg and src counts
trigger_data = pd.read_csv(f'./2.trigger/trigger_output_{test_fluence}_{grb_theta}_{grb_phi}.csv')
bkg_count = np.array(np.array(trigger_data)[0, 12: 12+8])
src_count = np.array(np.array(trigger_data)[0, 4: 4+8])
total_count = bkg_count + src_count

# Mesh data to fit
src_count_mesh, _ = np.meshgrid(src_count, np.arange(0, len(table1)))
total_count_mesh, _ = np.meshgrid(total_count, np.arange(0, len(table1)))

# Calculate Chi-squared, (S - N*T)^2 / O
n1 = np.sum(src_count_mesh * table1[:, 3:11] / total_count_mesh, 1) / \
     np.sum(table1[:, 3:11]**2 / total_count_mesh, 1)
chi_square1 = np.sum(src_count_mesh**2 / total_count_mesh, 1) \
              - 2 * n1 * np.sum(src_count_mesh * table1[:, 3:11] / total_count_mesh, 1) \
              + n1**2 * np.sum(table1[:, 3:11]**2 / total_count_mesh, 1)
n2 = np.sum(src_count_mesh * table2[:, 3:11] / total_count_mesh, 1) / \
     np.sum(table2[:, 3:11]**2 / total_count_mesh, 1)
chi_square2 = np.sum(src_count_mesh**2 / total_count_mesh, 1) \
              - 2 * n2 * np.sum(src_count_mesh * table2[:, 3:11] / total_count_mesh, 1) \
              + n2**2 * np.sum(table2[:, 3:11]**2 / total_count_mesh, 1)
n3 = np.sum(src_count_mesh * table3[:, 3:11] / total_count_mesh, 1) / \
     np.sum(table3[:, 3:11]**2 / total_count_mesh, 1)
chi_square3 = np.sum(src_count_mesh**2 / total_count_mesh, 1) \
              - 2 * n3 * np.sum(src_count_mesh * table3[:, 3:11] / total_count_mesh, 1) \
              + n3**2 * np.sum(table3[:, 3:11]**2 / total_count_mesh, 1)

# Find the best fit
which_table = np.argmin(np.array([np.min(chi_square1), np.min(chi_square2), np.min(chi_square3)]))
if which_table == 0:
    table        = table1
    chi_min_idx  = np.argmin(chi_square1)
    chi_square   = chi_square1
    location_xyz = table1[chi_min_idx, 0:3]
elif which_table == 1:
    table        = table2
    chi_min_idx  = np.argmin(chi_square2)
    chi_square   = chi_square2
    location_xyz = table2[chi_min_idx, 0:3]
elif which_table == 2:
    table        = table3
    chi_min_idx  = np.argmin(chi_square3)
    chi_square   = chi_square3
    location_xyz = table3[chi_min_idx, 0:3]
location_theta, location_phi  = cartesian2spherical(location_xyz[0], location_xyz[1], location_xyz[2])

# Load real GRB info. to compare best fit
real_grb_info = pd.read_csv(f'./1.input/real_grb_info_{test_fluence}_{grb_theta}_{grb_phi}.csv')
real_grb_table = real_grb_info['Table Number'][0]
real_grb_theta = real_grb_info['GRB Theta (TASA)'][0]
real_grb_phi = real_grb_info['GRB Phi (TASA)'][0]
real_grb_x, real_grb_y, real_grb_z  = spherical2cartesian(real_grb_theta, real_grb_phi)
print('real_table:', real_grb_table)
print('real_theta:', real_grb_theta)
print('real_phi:', real_grb_phi)
print('fit_table:', which_table+1)
print('fit_theta:', location_theta)
print('fit_phi:', location_phi)
print('====================')

# Deal with rotation by quaternion for GRB and table, and transform to Ra & Dec
q_sc = Quaternion(trigger_data['Qw'][0], trigger_data['Qx'][0], trigger_data['Qy'][0], trigger_data['Qz'][0])
q_real_grb = Quaternion(0, real_grb_x, real_grb_y, real_grb_z)
q_location = Quaternion(0, location_xyz[0], location_xyz[1], location_xyz[2])
q_real_grb_eci = q_sc.inverse * q_real_grb * q_sc
q_location_eci = q_sc.inverse * q_location * q_sc
real_grb_ra, real_grb_dec = eci2equatorial(q_real_grb_eci[1], q_real_grb_eci[2], q_real_grb_eci[3])
location_ra, location_dec = eci2equatorial(q_location_eci[1], q_location_eci[2], q_location_eci[3])
print('real_ra:', real_grb_ra)
print('real_dec:', real_grb_dec)
print('fit_ra:', location_ra)
print('fit_dec:', location_dec)
print('====================')
table_ra = np.array([])
table_dec = np.array([])
for direction_idx in range(len(table)):
    q_table = Quaternion(0, table[direction_idx, 0], table[direction_idx, 1], table[direction_idx, 2])
    q_table_eci = q_sc.inverse * q_table * q_sc
    table_ra_temp, table_dec_temp = eci2equatorial(q_table_eci[1], q_table_eci[2], q_table_eci[3])
    table_ra = np.append(table_ra, table_ra_temp)
    table_dec = np.append(table_dec, table_dec_temp)

# Select time arbitrary
time_obj = datetime.strptime('2024_02_07_00_00_00.000000', '%Y_%m_%d_%H_%M_%S.%f')

# Calculate position of earth (center is fixed, but skyfield package depends on time)
ts = load.timescale()
t = ts.utc(time_obj.year, time_obj.month, time_obj.day, time_obj.hour, time_obj.minute, time_obj.second)
d = Distance(m=[trigger_data['ECIx']*1000, trigger_data['ECIy']*1000, trigger_data['ECIz']*1000]) # km to m
p = Geocentric(d.au, t=t)
g = wgs84.subpoint(p)
sc_height = g.elevation.m
earth_r = np.sqrt(
    np.sum([(trigger_data['ECIx']*1000)**2,
            (trigger_data['ECIy']*1000)**2,
            (trigger_data['ECIz']*1000)**2])
    )
earth_eci = np.array([-trigger_data['ECIx'], -trigger_data['ECIy'], -trigger_data['ECIz']])
earth_ra, earth_dec = eci2equatorial(earth_eci[0], earth_eci[1], earth_eci[2])

# Infer earth obstacle (not yet check detail, looks correct!!!)
obstacle_angle = (90 - np.arccos(earth_r / (earth_r + sc_height)) * (180/np.pi)) * (np.pi/180)
t_angle = np.arange(0, 2*np.pi, np.pi/100)
horizon_x =  (np.sin(obstacle_angle)*np.cos(-earth_dec/180*np.pi+np.pi*0.5)*np.cos(earth_ra/180*np.pi))*np.cos(t_angle)\
            -(np.sin(obstacle_angle)*np.sin( earth_ra /180*np.pi))*np.sin(t_angle)\
            +(np.cos(obstacle_angle)*np.sin(-earth_dec/180*np.pi+np.pi*0.5)*np.cos(earth_ra/180*np.pi))
horizon_y =  (np.sin(obstacle_angle)*np.cos(-earth_dec/180*np.pi+np.pi*0.5)*np.sin(earth_ra/180*np.pi))*np.cos(t_angle)\
            -(np.sin(obstacle_angle)*np.cos( earth_ra /180*np.pi))*np.sin(t_angle)\
            +(np.cos(obstacle_angle)*np.sin(-earth_dec/180*np.pi+np.pi*0.5)*np.sin(earth_ra/180*np.pi))
horizon_z = -(np.sin(obstacle_angle)*np.sin(-earth_dec/180*np.pi+np.pi*0.5))*np.cos(t_angle)\
            + np.cos(obstacle_angle)*np.cos(-earth_dec/180*np.pi+np.pi*0.5)
horizon_ra = np.array([])
horizon_dec = np.array([])
for horizon_idx in range(len(horizon_x)):
    horizon_ra_temp, horizon_dec_temp = eci2equatorial(horizon_x[horizon_idx],
                                                       horizon_y[horizon_idx],
                                                       horizon_z[horizon_idx])
    horizon_ra = np.append(horizon_ra, horizon_ra_temp)
    horizon_dec = np.append(horizon_dec, horizon_dec_temp)
if np.count_nonzero(np.abs(np.diff(horizon_ra))>300)==1:
    is_horizon_split = False
    horizon_dec = horizon_dec[np.argsort(horizon_ra)]
    horizon_ra  = horizon_ra[np.argsort(horizon_ra)]
    horizon_ra = np.append(horizon_ra,np.ones(50)*359.99)
    horizon_ra = np.append(horizon_ra,np.ones(50)*0.01)
    if earth_dec < 0:
        horizon_dec = np.append(horizon_dec, np.linspace(horizon_dec[-1],-90,num=50))
        horizon_dec = np.append(horizon_dec, np.linspace(-90,horizon_dec[0],num=50))
    else:
        horizon_dec = np.append(horizon_dec, np.linspace(horizon_dec[-1],90,num=50))
        horizon_dec = np.append(horizon_dec, np.linspace(90,horizon_dec[0],num=50))
elif np.count_nonzero(np.abs(np.diff(horizon_ra))>300)==2:
    is_horizon_split = True
    split_index_1 = np.where(np.abs(np.diff(horizon_ra))>300)[0][0]
    split_index_2 = np.where(np.abs(np.diff(horizon_ra))>300)[0][1]
    horizon_ra_1  = np.roll(horizon_ra,-split_index_1-1)[0:(split_index_2-split_index_1)]
    horizon_ra_2  = np.roll(horizon_ra,-split_index_2-1)[0:len(horizon_ra)-(split_index_2-split_index_1)]
    horizon_dec_1 = np.roll(horizon_dec,-split_index_1-1)[0:(split_index_2-split_index_1)]
    horizon_dec_2 = np.roll(horizon_dec,-split_index_2-1)[0:len(horizon_ra)-(split_index_2-split_index_1)]
    horizon_ra_1  = np.append(horizon_ra_1,np.ones(50)*359.99)
    horizon_ra_2  = np.append(horizon_ra_2,np.ones(50)*0.01)
    horizon_dec_1 = np.append(horizon_dec_1,np.linspace(horizon_dec_1[-1],horizon_dec_1[0],num=50))
    horizon_dec_2 = np.append(horizon_dec_2,np.linspace(horizon_dec_2[-1],horizon_dec_2[0],num=50))
else:
    is_horizon_split = False
    
# Calculate position of sun (change with time, day is obvious)
sun_coords = get_sun(Time(time_obj, scale='utc'))
sun_ra = sun_coords.ra.degree
sun_dec = sun_coords.dec.degree

# Calculate position of milkyway's disk and core (fix in equatorial)
longitude = np.linspace(0, 360, 100) # disk
latitude = np.zeros(100) # disk
milkyway = SkyCoord(longitude, latitude, unit=units.deg, frame='galactic')
milkyway_equatorial = milkyway.transform_to('icrs') # ~ equatorial ~ eci
milkyway_ra, milkyway_dec = milkyway_equatorial.ra.degree, milkyway_equatorial.dec.degree
milkyway_center_ra = milkyway_ra[0] # core @ longitude = 0
milkyway_center_dec = milkyway_dec[0] # core @ latitude = 0
milkyway_dec = milkyway_dec[np.argsort(milkyway_ra)]
milkyway_ra = milkyway_ra[np.argsort(milkyway_ra)]

# Plot figure
fig1, ax1 = plt.subplots(1, 1, figsize=(10, 5), 
                         subplot_kw={'projection': 'mollweide'}, constrained_layout=True)

# Define some plot info
chi_min = np.min(chi_square)
chi_max = np.min(chi_square) + 9.6
plot_index = chi_square < chi_max

# Plot earth center
ax1.scatter(earth_ra * (np.pi/180) - np.pi, earth_dec * (np.pi/180), 
            marker='x', s=100, linewidth=1, color='deepskyblue', zorder=7)

# Plot earth obstacle (not yet check detail, looks correct!!!)
if is_horizon_split==True:
    print('test')
    ax1.plot(horizon_ra_1 * (np.pi/180) - np.pi, horizon_dec_1 * (np.pi/180), color='skyblue', alpha=0.3, zorder=8)
    ax1.fill(horizon_ra_1 * (np.pi/180) - np.pi, horizon_dec_1 * (np.pi/180), color='skyblue', alpha=0.3, zorder=8)
    ax1.plot(horizon_ra_2 * (np.pi/180) - np.pi, horizon_dec_2 * (np.pi/180), color='skyblue', alpha=0.3, zorder=8)
    ax1.fill(horizon_ra_2 * (np.pi/180) - np.pi, horizon_dec_2 * (np.pi/180), color='skyblue', alpha=0.3, zorder=8)
else:
    ax1.plot(horizon_ra * (np.pi/180) - np.pi, horizon_dec * (np.pi/180), 
             linewidth=1, color='skyblue', alpha=0.3, zorder=8)
    ax1.fill(horizon_ra * (np.pi/180) - np.pi, horizon_dec * (np.pi/180), 
             color='skyblue', alpha=0.3, zorder=8)

# Plot sun
ax1.scatter(sun_ra * (np.pi/180) - np.pi, sun_dec * (np.pi/180), 
            marker='o', s=100, color='gold', zorder=6)

# Plot milkyway
ax1.plot(milkyway_ra * (np.pi/180) - np.pi, milkyway_dec * (np.pi/180), 
         linewidth=1, color='silver', zorder=5)
ax1.scatter(milkyway_center_ra * (np.pi/180) - np.pi, milkyway_center_dec * (np.pi/180), 
            marker='o', s=100, color='silver', zorder=5)

# Plot distribution of location 
scatter = ax1.scatter(table_ra[plot_index] * (np.pi/180) - np.pi, table_dec[plot_index] * (np.pi/180), 
                      marker='o', s=10, c=chi_square[plot_index], edgecolors='none',
                      cmap=cmap, vmin=chi_min, vmax=chi_max, zorder=1)
cbar = plt.colorbar(scatter, ax=ax1, 
                    orientation='horizontal', aspect=70, pad=0.03,
                    boundaries=np.linspace(chi_min, chi_max, 100), 
                    ticks=[chi_min, chi_min+2.3, chi_min+4.6, chi_min+9.6],)
cbar.ax.tick_params(direction='in', length=10, width=2, color='black', labelsize=10)
ax1.tricontour(table_ra * (np.pi/180) - np.pi, table_dec * (np.pi/180), 
               np.array(chi_square, dtype='float'), levels=[chi_min+2.3, chi_min+4.6, chi_min+9.6], 
               linewidths=1, colors='black', zorder=2)

# Plot ground truth and bset fit 
ax1.scatter(real_grb_ra * (np.pi/180) - np.pi, real_grb_dec * (np.pi/180), 
            marker='x', s=100, linewidth=2, color='limegreen', zorder=3)
ax1.scatter(location_ra * (np.pi/180) - np.pi, location_dec * (np.pi/180), 
            marker='x', s=100, linewidth=2, color='lightcoral', zorder=4)

# Adjust ticks label
xticks = np.array([-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150]) * (np.pi/180.0)
xtick_labels = ['30°', '60°', '90°', '120°', '150°', '180°', '210°', '240°', '270°', '300°', '330°']
plt.xticks(xticks, xtick_labels, fontsize=10)
yticks = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]) * (np.pi/180.0)
ytick_labels = ['-75°', '-60°', '-45°', '-30°', '-15°', '0°', '15°', '30°', '45°', '60°', '75°']
plt.yticks(yticks, ytick_labels, fontsize=10)

# Save figure
ax1.grid(linewidth=0.3)
ax1.set_xlabel('R.A.', fontsize=10)
ax1.set_ylabel('Dec.', fontsize=10)
fig1.savefig(f'./3.location/sky_map_{test_fluence}_{grb_theta}_{grb_phi}.png', dpi=300)
plt.close(fig1)
#====================