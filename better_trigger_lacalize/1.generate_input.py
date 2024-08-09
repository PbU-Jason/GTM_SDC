#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
import numpy as np
import pandas as pd 
from datetime import datetime
#====================

### variable ###

# Select np random seed
np.random.seed(234895)

# Filename
table_number = 1 # middle energy
# table_number = 2 # hard energy
# table_number = 3 # soft energy

# GRB properties
test_fluence = 4e-6 # erg/cm^2
# test_fluence = 4e-5 # erg/cm^2
grb_type = 'LGRB'
# grb_type = 'SGRB'
# grb_random_direction = True
grb_random_direction = False
grb_theta = 45 # deg, in mass-model coordinate
grb_phi   = 60 # deg, in mass-model coordinate

# Lightcurve properties
total_duration = 1000 # s
bkg_count_rate = 42.6 # #/s from 2021.06.09_CountRate_v3.pdf

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

def generate_data_poisson(data_type, ideal_data, start_time, time_interval, sensor, storage):
    if data_type == 'BKG' or data_type == 'LGRB':
        real_data = np.random.poisson(ideal_data, time_interval) # flucuate by Poisson distribution
        for each_real_data, time in zip(real_data, range(start_time, start_time+time_interval, 1)):
            sensor_id   = np.ones(each_real_data) * (sensor+1)
            real_time   = np.random.uniform(time, time+1, each_real_data) # randomly give time tag
            sensor_time = (np.vstack((sensor_id, real_time))).T # np.vstack (n,) + (n,) = (2, n)
            storage     = np.concatenate((storage, sensor_time), axis=0) # concatenate along row (axis 0)
    elif data_type == 'SGRB':
        real_data   = np.random.poisson(ideal_data * time_interval) # rescale 1 to 0.5 s
        sensor_id   = np.ones(real_data) * (sensor+1)
        real_time   = np.random.uniform(start_time, start_time+time_interval, real_data)
        sensor_time = (np.vstack((sensor_id, real_time))).T
        storage     = np.concatenate((storage, sensor_time), axis=0)
    else:
        print('please select data_type!')
    return storage
#====================

### main ###

# Load big table
table = np.array(pd.read_csv(f'./0.table/linear_big_typical{table_number}_response.csv'))

# Choose GRB starting time randomly
grb_start = np.random.randint(total_duration) # s

# GRB properties based on table and GRB type
if table_number == 1:
    if grb_type == 'SGRB':
        grb_duration = 0.5       # s
        ref_fluence  = 2e-5      # erg/cm^2
    elif grb_type == 'LGRB':
        grb_duration = 10        # s
        ref_fluence  = 4e-4      # erg/cm^2
    else:
        print('please select GRB type!')
elif table_number == 2:
    if grb_type == 'SGRB':
        grb_duration = 0.5       # s
        ref_fluence  = 4.0507e-5 # erg/cm^2
    elif grb_type == 'LGRB':
        grb_duration = 10        # s
        ref_fluence  = 8.1014e-4 # erg/cm^2
    else:
        print('please select GRB type!')
elif table_number == 3:
    if grb_type == 'SGRB':
        grb_duration = 0.5       # s
        ref_fluence  = 8.9764e-6 # erg/cm^2
    elif grb_type == 'LGRB':
        grb_duration = 10        # s
        ref_fluence  = 1.7952e-4 # erg/cm^2
    else:
        print('please select GRB type!')
else:
    print('please select filename!')

# Choose GRB direction
if grb_random_direction:
    grb_direction_idx = np.random.randint(len(table))
else:
    x, y, z = spherical2cartesian(grb_theta, grb_phi)
    x *= -1 # transfer GTM's x to TASA's x
    z *= -1 # transfer GTM's z to TASA's z
    table_xyz = table[:, 0:3]
    table_x_diff = table_xyz[:, 0] - x
    table_y_diff = table_xyz[:, 1] - y
    table_z_diff = table_xyz[:, 2] - z
    table_distance = np.array([])
    for direction_idx in range(len(table_xyz)):
        distance = (table_x_diff[direction_idx]**2 +\
                    table_y_diff[direction_idx]**2 +\
                    table_z_diff[direction_idx]**2)**0.5
        table_distance = np.append(table_distance, distance)
    grb_direction_idx = np.argmin(table_distance)
grb_xyz = table[grb_direction_idx, 0:3]
grb_theta_phi = cartesian2spherical(grb_xyz[0], grb_xyz[1], grb_xyz[2]) # deg, in satellite coordinate

# Decide bkg count rate, slightly change with time
bkg_count_rate_list = bkg_count_rate * (0.95 + 0.05 * np.square(np.arange(0, 1, 1/total_duration)))

# Decide src count rate
# (flux * A scale) * responce(area) = count rate
src_count_rate_list = (245.96 * (test_fluence/ref_fluence)) * table[grb_direction_idx, 3:11]

# Create empty array to store data
sensor_data = np.empty(shape=[0, 2])
for sensor in range(8):
    sensor_data = generate_data_poisson('BKG', bkg_count_rate_list, 
                                        0, total_duration, 
                                        sensor, sensor_data)
    sensor_data = generate_data_poisson(grb_type, src_count_rate_list[sensor], 
                                        grb_start, grb_duration, 
                                        sensor, sensor_data)
sensor_data = sensor_data[np.argsort(sensor_data[:, 1])] # arrange by time

# Save real GRB info.
real_grb_info = pd.DataFrame({
    'UTC': [datetime.now().strftime('%Y_%m_%d_%H_%M_%S.%f')], 'GRB Fluence': [test_fluence],
    'GRB Start': [grb_start], 'GRB End': [grb_start + grb_duration],
    'GRB Theta (GTM)': [grb_theta], 'GRB Phi (GTM)': [grb_phi],
    'GRB Theta (TASA)': [grb_theta_phi[0]], 'GRB Phi (TASA)': [grb_theta_phi[1]],
    'Table Number': [table_number],
    })
real_grb_info.to_csv(f'./1.input/real_grb_info_{test_fluence}_{grb_theta}_{grb_phi}.csv', index=False)

# Save lightcurve
lightcurve             = pd.DataFrame(data=sensor_data, columns=['Detector', 'Time'])
lightcurve['Detector'] = lightcurve['Detector'].astype(int)
lightcurve = lightcurve[['Time', 'Detector']]
lightcurve.to_csv(f'./1.input/lightcurve_{test_fluence}_{grb_theta}_{grb_phi}.csv', index=False)

# Save satellite attitude
satellite_attitude         = pd.DataFrame()
satellite_attitude['Time'] = np.linspace(0, total_duration, 100+1)
satellite_attitude['Qw']   = np.ones(100+1) * np.sqrt(0.5)
satellite_attitude['Qx']   = np.ones(100+1) * -np.sqrt(0.5)
satellite_attitude['Qy']   = np.zeros(100+1)
satellite_attitude['Qz']   = np.zeros(100+1)
satellite_attitude['ECIx'] = np.ones(100+1) * -12.32691165665816
satellite_attitude['ECIy'] = np.ones(100+1) * 4215.534296188868
satellite_attitude['ECIz'] = np.ones(100+1) * 5318.530945682411
satellite_attitude.to_csv(f'./1.input/satellite_attitude_{test_fluence}_{grb_theta}_{grb_phi}.csv', index=False)
#====================