#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 10:34:31 2023

@author: jillianwu
version: 9/29/2023
"""

### package ###
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from matplotlib.colors import ListedColormap
cmap = np.zeros([256, 4])
cmap[:, 0] = np.flip(np.linspace(0.0, 175/255, 256))
cmap[:, 1] = np.flip(np.linspace(0.0, 0.0, 256))
cmap[:, 2] = np.flip(np.linspace(0.0, 1.0, 256))
cmap[:, 3] = np.flip(np.linspace(0.8, 0.8, 256))
cmap = ListedColormap(cmap)
from datetime import datetime
from astropy import units
from astropy.time import Time
from astropy.coordinates import get_sun, SkyCoord
from pyquaternion import Quaternion
from skyfield.positionlib import Geocentric
from skyfield.api import Distance, load, wgs84
#====================

### function ###
def unit_vector(vector):
    # Returns the unit vector of the vector. 
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    # Returns the angle in radians between vectors 'v1' and 'v2'
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def V2AZ(x,y,z):
    theta = np.mod(np.arctan2(y,-x)/np.pi*180,360)-180
    phi = np.arctan2(np.sqrt(x**2 + y**2),-z)/np.pi*180-90
    return theta,phi

def xyz2RD(x,y,z):
    RA = np.mod(np.arctan2(y,x)/np.pi*180,360)
    Dec = np.arctan2(z,np.sqrt(x**2 + y**2))/np.pi*180
    return RA,Dec

def RD2xyz(Ra,Dec):
    x = np.cos(Dec)*np.cos(Ra)
    y = np.cos(Dec)*np.sin(Ra)
    z = np.sin(Dec)
    return np.array([x, y, z])
#====================

### main code ###
table_name = ['middle','hard','soft']
table1 = np.array(pd.read_csv("./1.table/" + "big_typical1_response.csv")) #file name of middle energy big table
table2 = np.array(pd.read_csv("./1.table/" + "big_typical2_response.csv")) #file name of hard energy big table
table3 = np.array(pd.read_csv("./1.table/" + "big_typical3_response.csv")) #file name of soft energy big table

filename = "trigger_output"
trigger_data = pd.read_pickle(filename + ".pkl")

bkg_count = np.array(trigger_data.loc[0, list(trigger_data.keys())[23 : 23 + 8]])
print(bkg_count)
source_count = np.array(trigger_data.loc[0, list(trigger_data.keys())[15 : 15 + 8]])
print(source_count)
total_count = bkg_count + source_count

#==================================== calculate chi square distribution =================================
# bkg_count_tmp,tmp = np.meshgrid(bkg_count,np.arange(0,len(table1)))
source_count_tmp,tmp = np.meshgrid(source_count,np.arange(0,len(table1)))
total_count_tmp,tmp = np.meshgrid(total_count,np.arange(0,len(table1)))

# Chi^2 = sum((Observe - Estimate)^2 / Poisson noise)
## Observe: source count ;Estimate: (normalization factor)*(effective area)
# Chi^2 = sum(S^2 / P) - sum((2 * S * EA) / P) * N^2 + sum(EA^2 / P) * N^2
N1 = np.sum(table1[:,3:11]*source_count_tmp/total_count_tmp,1) / np.sum( table1[:,3:11]**2 / total_count_tmp ,1)
Chi_square1 = np.sum(source_count_tmp**2/total_count_tmp,1) \
    - 2*np.sum(table1[:,3:11]*source_count_tmp/total_count_tmp,1)*N1 \
    + np.sum( table1[:,3:11]**2 / total_count_tmp ,1)*N1**2

N2 = np.sum(table2[:,3:11]*source_count_tmp/total_count_tmp,1) / np.sum( table2[:,3:11]**2 / total_count_tmp ,1)
Chi_square2 = np.sum(source_count_tmp**2/total_count_tmp,1) \
    - 2*np.sum(table2[:,3:11]*source_count_tmp/total_count_tmp,1)*N2 \
    + np.sum( table2[:,3:11]**2 / total_count_tmp ,1)*N2**2

N3 = np.sum(table3[:,3:11]*source_count_tmp/total_count_tmp,1) / np.sum( table3[:,3:11]**2 / total_count_tmp ,1)
Chi_square3 = np.sum(source_count_tmp**2/total_count_tmp,1) \
    - 2*np.sum(table3[:,3:11]*source_count_tmp/total_count_tmp,1)*N3 \
    + np.sum( table3[:,3:11]**2 / total_count_tmp ,1)*N3**2

print(np.array([np.min(Chi_square1),np.min(Chi_square2),np.min(Chi_square3)]))
which_table = np.argmin(np.array([np.min(Chi_square1),np.min(Chi_square2),np.min(Chi_square3)]))
if which_table==0:
    index_min_chi = np.argmin(Chi_square1)
    Chi_square = Chi_square1
    location_xyz_sc = table1[index_min_chi,0:3]
elif which_table==1:
    index_min_chi = np.argmin(Chi_square2)
    Chi_square = Chi_square2
    location_xyz_sc = table2[index_min_chi,0:3]
elif which_table==2:
    index_min_chi = np.argmin(Chi_square3)
    Chi_square = Chi_square3
    location_xyz_sc = table3[index_min_chi,0:3]

# location_theta, location_phi  =  V2AZ(location_xyz_sc[0],location_xyz_sc[1],location_xyz_sc[2])

# location_xyz_sc : the location of the source in the coordinate of the massmodel
print("location_xyz_sc: " + str(location_xyz_sc))
# print("location_theta_phi: " + str((location_theta,location_phi)))
print("which_table: " + str(which_table+1))


# (qw,qx,qy,qz) is the quaternions representing the rotation relative to ECI
# q_sc : quaternioins from trigger data
# q_location_sc : the location of the source in the coordinate of the satellite
# q_location_sky : q_location_sc corrected by the "inverse" rotation of the quaternions
q_sc = Quaternion(trigger_data['Qw'] * 2**-15,trigger_data['Qx'] * 2**-15,trigger_data['Qy'] * 2**-15,trigger_data['Qz'] * 2**-15)
q_location_sc = Quaternion(0, -1 * location_xyz_sc[0], location_xyz_sc[1], -1 * location_xyz_sc[2])    # Massmodel's x&z are the opposite of the satellite's ones
q_location_sky = (q_sc * q_location_sc * q_sc.inverse).conjugate

location_xyz_sky = [q_location_sky[1],q_location_sky[2],q_location_sky[3]]
print("location_xyz_sky: " + str(location_xyz_sky))

location_RA, location_Dec  =  xyz2RD(location_xyz_sky[0],location_xyz_sky[1],location_xyz_sky[2])
print("location_RA_Dec: " + str((location_RA,location_Dec)))

#================== position of earth and sun and milkyway =================
# earth horizon
print(trigger_data[list(trigger_data.keys())[0]][0])
start_time_obj = datetime.strptime(trigger_data[list(trigger_data.keys())[0]][0], '%Y-%m-%d %H:%M:%S')
UTC = [start_time_obj.year, start_time_obj.month, start_time_obj.day, start_time_obj.hour, start_time_obj.minute, start_time_obj.second]
print(UTC)
ts = load.timescale()
t = ts.utc(UTC[0],UTC[1],UTC[2],UTC[3],UTC[4],UTC[5])
d = Distance(m=[trigger_data['ECIx'] * 2**-4 * 1000,trigger_data['ECIy'] * 2**-4 * 1000,trigger_data['ECIz'] * 2**-4 * 1000]) # "*1000" for km to m
p = Geocentric(d.au, t=t)       # ECI -> ECEF
g = wgs84.subpoint(p)           # the projection of the satellite on Earth 
sc_height = g.elevation.m       # Altitude of the satellite
# earth_R = np.sqrt(np.sum([(trigger_data['ECIx']*1000)**2,(trigger_data['ECIy']*1000)**2,(trigger_data['ECIz']*1000)**2]))
earth_R = 6371 * 1000
# print('sc_height:' + str(sc_height))
print('earth_R= ' +str(earth_R))
# print('trigger_data:' + str((trigger_data['ECIx'],trigger_data['ECIy'],trigger_data['ECIz'])))
earth_V = np.array([-trigger_data['ECIx'] * 2**-4, -trigger_data['ECIy'] * 2**-4, -trigger_data['ECIz'] * 2**-4])
earth_V = earth_V / np.linalg.norm(earth_V)
earth_RA, earth_Dec = xyz2RD(earth_V[0],earth_V[1],earth_V[2])
print('earth ECI: '+str((earth_V[0],earth_V[1],earth_V[2])))
print('earth RA Dec: '+str((earth_RA, earth_Dec)))
earth_r = 90 - np.arccos(earth_R / (earth_R + sc_height)) / np.pi*180
t_angle = np.arange(0,np.pi*2,np.pi/100)

# horizon_x & horizon_y & horizon_z : the horizon block by the Earth
horizon_x =  (np.sin(earth_r)*np.cos(-earth_Dec/180*np.pi+np.pi*0.5)*np.cos(earth_RA/180*np.pi))*np.cos(t_angle)\
            -(np.sin(earth_r)*np.sin( earth_RA /180*np.pi))*np.sin(t_angle)\
            +(np.cos(earth_r)*np.sin(-earth_Dec/180*np.pi+np.pi*0.5)*np.cos(earth_RA/180*np.pi))
horizon_y =  (np.sin(earth_r)*np.cos(-earth_Dec/180*np.pi+np.pi*0.5)*np.sin(earth_RA/180*np.pi))*np.cos(t_angle)\
            -(np.sin(earth_r)*np.cos( earth_RA /180*np.pi))*np.sin(t_angle)\
            +(np.cos(earth_r)*np.sin(-earth_Dec/180*np.pi+np.pi*0.5)*np.sin(earth_RA/180*np.pi))
horizon_z = -(np.sin(earth_r)*np.sin(-earth_Dec/180*np.pi+np.pi*0.5))*np.cos(t_angle)\
            + np.cos(earth_r)*np.cos(-earth_Dec/180*np.pi+np.pi*0.5)
horizon_RA = np.array([])
horizon_Dec = np.array([])
# (x, y, z) -> RA, DEC
for ii in range(len(horizon_x)):
    horizon_RA_, horizon_Dec_ = xyz2RD(horizon_x[ii],horizon_y[ii],horizon_z[ii])
    horizon_RA = np.append(horizon_RA,horizon_RA_)
    horizon_Dec = np.append(horizon_Dec,horizon_Dec_)

# Correcting the value of RA & DEC
if np.count_nonzero(np.abs(np.diff(horizon_RA))>300)==1:
    is_horizon_split = False
    horizon_Dec = horizon_Dec[np.argsort(horizon_RA)]
    horizon_RA  = horizon_RA[np.argsort(horizon_RA)]
    horizon_RA = np.append(horizon_RA,np.ones(50)*359.99)
    horizon_RA = np.append(horizon_RA,np.ones(50)*0.01)
    if earth_Dec<0:
        horizon_Dec = np.append(horizon_Dec,np.linspace(horizon_Dec[-1],-90,num=50))
        horizon_Dec = np.append(horizon_Dec,np.linspace(-90,horizon_Dec[0],num=50))
    else:
        horizon_Dec = np.append(horizon_Dec,np.linspace(horizon_Dec[-1],90,num=50))
        horizon_Dec = np.append(horizon_Dec,np.linspace(90,horizon_Dec[0],num=50))
elif np.count_nonzero(np.abs(np.diff(horizon_RA))>300)==2:
    is_horizon_split = True
    print( np.where(np.abs(np.diff(horizon_RA))>300) )
    split_index_1 = np.where(np.abs(np.diff(horizon_RA))>300)[0][0]
    split_index_2 = np.where(np.abs(np.diff(horizon_RA))>300)[0][1]
    horizon_RA_1  = np.roll(horizon_RA,-split_index_1-1)[0:(split_index_2-split_index_1)]
    horizon_RA_2  = np.roll(horizon_RA,-split_index_2-1)[0:len(horizon_RA)-(split_index_2-split_index_1)]
    horizon_Dec_1 = np.roll(horizon_Dec,-split_index_1-1)[0:(split_index_2-split_index_1)]
    horizon_Dec_2 = np.roll(horizon_Dec,-split_index_2-1)[0:len(horizon_RA)-(split_index_2-split_index_1)]
    horizon_RA_1  = np.append(horizon_RA_1,np.ones(50)*359.99)
    horizon_RA_2  = np.append(horizon_RA_2,np.ones(50)*0.01)
    horizon_Dec_1 = np.append(horizon_Dec_1,np.linspace(horizon_Dec_1[-1],horizon_Dec_1[0],num=50))
    horizon_Dec_2 = np.append(horizon_Dec_2,np.linspace(horizon_Dec_2[-1],horizon_Dec_1[0],num=50))
else:
    is_horizon_split = False
    
# sun
trigger_time = Time(start_time_obj, scale='utc')
coords = get_sun(trigger_time)
sun_RA = coords.ra.degree
sun_Dec = coords.dec.degree
print("sun_RA_Dec " + str((sun_RA, sun_Dec)))

# milkyway
lon = np.linspace(0, 360, 100)
lat = np.zeros(100)
ecl = SkyCoord(lon, lat, unit=units.deg, frame='galactic')
ecl_gal = ecl.transform_to('icrs')
milkyway_RA, milkyway_Dec = ecl_gal.ra.degree, ecl_gal.dec.degree
milkyway_RA_C = milkyway_RA[0]
milkyway_Dec_C = milkyway_Dec[0]
milkyway_Dec = milkyway_Dec[np.argsort(milkyway_RA)]
milkyway_RA  = milkyway_RA[np.argsort(milkyway_RA)]

#======================init plot parameter===============
colormap_RGB = np.ones((256, 4))
colormap_RGB[:, 0] = np.linspace(138/256, 1, 256)
colormap_RGB[:, 1] = np.linspace(43/256, 1, 256)
colormap_RGB[:, 2] = np.linspace(226/256, 1, 256)
purple = ListedColormap(colormap_RGB)

RA = np.array([])
Dec = np.array([])
for ii in range(len(table1)):
    q_table = Quaternion(0, table1[ii,0], table1[ii,1], table1[ii,2])
    q_table_sky = q_sc*q_table*q_sc.inverse
    RA_, Dec_ = xyz2RD(q_table_sky[1],q_table_sky[2],q_table_sky[3])
    RA = np.append(RA,RA_)
    Dec = np.append(Dec,Dec_)

phi, theta = V2AZ(table1[:,0],table1[:,1],table1[:,2])

color_map_max = np.min(Chi_square)+9.6
color_map_min = np.min(Chi_square)

# plot all sky map
plt.figure(figsize=(16, 8))
ax1 = plt.subplot(111, projection='mollweide')
plot_index = Chi_square < color_map_max

# earth
plt.scatter(-earth_RA/180*np.pi+np.pi, earth_Dec/180*np.pi, marker='x', s=100, linewidths=3, c='#00ccff', label='Center of Earth', zorder=7)
if is_horizon_split==True:
    plt.plot(-horizon_RA_1/180*np.pi+np.pi, horizon_Dec_1/180*np.pi, c='#66e0ff', alpha = 0.3)
    plt.fill(-horizon_RA_1/180*np.pi+np.pi, horizon_Dec_1/180*np.pi, c='#66e0ff', alpha = 0.3)
    plt.plot(-horizon_RA_2/180*np.pi+np.pi, horizon_Dec_2/180*np.pi, c='#66e0ff', alpha = 0.3)
    plt.fill(-horizon_RA_2/180*np.pi+np.pi, horizon_Dec_2/180*np.pi, c='#66e0ff', alpha = 0.3)
    print('test')
else:
    plt.plot(-horizon_RA/180*np.pi+np.pi, horizon_Dec/180*np.pi, c='#66e0ff', alpha = 0.3, zorder=9)
    plt.fill(-horizon_RA/180*np.pi+np.pi, horizon_Dec/180*np.pi, c='#66e0ff', alpha = 0.3, label='Sky Covered by Earth', zorder=8)

# sun
plt.scatter(-sun_RA/180*np.pi+np.pi, sun_Dec/180*np.pi, marker='o', s=100, c='#ffcc66', label='Sun', zorder=6)

# milkyway
plt.plot(-milkyway_RA/180*np.pi+np.pi, milkyway_Dec/180*np.pi, c='#cccccc', lw=2, alpha=0.5, label='Disk of Milkyway', zorder=4)
plt.scatter(-milkyway_RA_C/180*np.pi+np.pi, milkyway_Dec_C/180*np.pi, c='#cccccc', marker='o', s=100, alpha=0.8, label='Center of Milkyway', zorder=5)

# location
plt.scatter(-RA[plot_index]/180*np.pi+np.pi, Dec[plot_index]/180*np.pi, marker='o', s=20, c=Chi_square[plot_index], cmap=cmap, vmin=color_map_min, vmax=color_map_max, edgecolors='none', zorder=1)
cb = plt.colorbar(fraction=0.05, orientation='horizontal', boundaries=np.linspace(color_map_min,color_map_max,100), ticks=[color_map_min+2.3, color_map_min+4.6, color_map_min+9.6], anchor=(0.1, 0), pad=0.1)
cb.set_label('Chi-Squared', fontsize=18, weight='bold')
cb.ax.tick_params(direction='in', length=23, width=3, color='white', labelsize=15)
plt.scatter(-location_RA/180*np.pi+np.pi, location_Dec/180*np.pi, marker='x', s=100, linewidths=3, c='white', label='Best Fit Location', zorder=3)
cs = ax1.tricontour(-RA/180*np.pi+np.pi, Dec/180*np.pi, np.array(Chi_square, dtype = 'float'), levels=[2.3, 4.6, 9.6]+color_map_min, colors='white', linewidths=1, zorder=2)

yticks = np.array([-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]) * (np.pi/180.0)
yticklabels = ['-75°', '-60°', '-45°', '-30°', '-15°', '0°', '15°', '30°', '45°', '60°', '75°']
plt.yticks(yticks, yticklabels, fontsize=18, weight='bold')
xticks = np.array([-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150]) * (np.pi/180.0)
xticklabels = ['330°', '300°', '270°', '240°', '210°', '180°', '150°', '120°', '90°', '60°', '30°']
plt.xticks(xticks, xticklabels, fontsize=18, weight='bold')

plt.xlabel('R.A. (J2000.0)', fontsize=18, weight='bold')
plt.ylabel('Dec. (J2000.0)', fontsize=18, weight='bold')
plt.title('All Sky Map', y=1.05, fontsize=25, weight='bold')
handles, labels = plt.gca().get_legend_handles_labels()
legend_order_list = [5, 0, 1, 2, 3, 4]
plt.legend([handles[i] for i in legend_order_list], [labels[i] for i in legend_order_list], loc='lower right', bbox_to_anchor=(1, -0.37), fontsize=15, prop={'size': 15, 'weight':'bold'})
plt.grid(True)
plt.savefig("./4.location/AllSykMap.png", dpi=500)

# #============================ plot zoom in sky map ======================
# plt.figure(figsize=(16,8))
# if location_Dec>70 or location_Dec<-70:
#     ax2 = plt.subplot(111, projection="polar")
# else:
#     ax2 = plt.subplot(111)
# cs2 = ax2.tricontour(RA, Dec, np.array(Chi_square, dtype = 'float'), levels = [2.3, 4.6, 9.6]+color_map_min, colors = 'gray', linewidths=1)
# plt.scatter(location_RA, location_Dec, marker='x', c = 'k')
# ax2.set_xlim((np.min((np.array(cs2.collections[2].get_paths()[0].to_polygons())[0][:,0]))), np.max(((cs2.collections[2].get_paths()[0].to_polygons())[0][:,0])))
# ax2.set_ylim((np.min(((cs2.collections[2].get_paths()[0].to_polygons())[0][:,1]))), np.max(((cs2.collections[2].get_paths()[0].to_polygons())[0][:,1])))
# plt.xlabel('RA(J2000.0) degrees')
# plt.ylabel('Dec(J2000.0) degrees')
# plt.title('zoom in sky map', y=1.05, size='large')
# plt.grid(True)
# plt.savefig("./4.location/zoominsykmap.png", dpi=300)

# #============================ result CSV ============================
# contour_RA  = -np.array(cs.collections[0].get_paths()[0].to_polygons())[0][:,0]+np.pi
# contour_Dec = np.array(cs.collections[0].get_paths()[0].to_polygons())[0][:,1]
# contour_x, contour_y, contour_z = RD2xyz(contour_RA, contour_Dec)
# coutour_dist = []
# for contour_x_, contour_y_, contour_z_ in zip(contour_x, contour_y, contour_z):
#     coutour_dist.append(angle_between(location_xyz_sky,[contour_x_, contour_y_, contour_z_])/np.pi*180)
# One_Sigma_Radius = np.mean(coutour_dist)

# best_fit_table = table_name[which_table]

# result = np.array([
#     location_RA,
#     location_Dec,
#     best_fit_table,
#     One_Sigma_Radius
# ])
# print(result)
# header_str = ['RA','Dec','Best_fit_table','One_sigma_radius']
# pd.DataFrame(result.reshape(-1, len(result))).to_csv("./4.location/result_"+ filename+ ".csv",index = False,header = header_str)
#====================