#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
import numpy as np
import pandas as pd 
from datetime import datetime
#====================

### selection ###
# filename
filename = 'big_typical1_response' # middle energy
# filename = 'big_typical2_response' # hard energy
# filename = 'big_typical3_response' # soft energy

# GRB properties
testing_fluence    = 4e-6   # erg/cm^2
GRB_type_selection = 'LGRB'
# GRB_type_selection = 'SGRB'
# GRB_random_direction = True
GRB_random_direction = False
GRB_theta = 144
GRB_phi   = 52
#====================

### function ###
def Polar2Cartesian(ThetaDegree, PhiDegree):
    ThetaRadian = ThetaDegree * np.pi/180
    PhiRadian   = PhiDegree * np.pi/180
    X = -np.sin(ThetaRadian) * np.cos(PhiRadian) # NSPO define +x to -x
    Y = np.sin(ThetaRadian) * np.sin(PhiRadian)
    Z = -np.cos(ThetaRadian)                     # NSPO define +z to -z
    return np.array([X, Y, Z])

def Cartesian2Polar(X, Y, Z):
    Theta = np.arctan2(np.sqrt(X**2 + Y**2), -Z) * (180/np.pi) # NSPO define +z to -z
    Phi   = np.arctan2(Y, -X) * (180/np.pi)                    # NSPO define +x to -x
    return Theta, Phi

def Generate_Data_Poisson(DataType, IdealData, StartTime, TimeInterval, Sensor, StorageSpace):
    if DataType == 'BKG' or DataType == 'LGRB':
        # base on the ideal data, using the poisson distribution to get the real data
        RealData = np.random.poisson(IdealData, len(range(StartTime, StartTime + TimeInterval)))
        for DataNumber, Time in zip(RealData, range(StartTime, StartTime + TimeInterval)):
            # give real data their random time
            RealTime        = np.random.uniform(Time, Time + 1, DataNumber)
            SensorID        = np.ones(DataNumber) * (Sensor + 1)
            RealSensorData  = (np.vstack((RealTime, SensorID))).T
            StorageSpace    = np.concatenate((StorageSpace, RealSensorData), axis=0)
    elif DataType == 'SGRB':
        RealData        = np.random.poisson(IdealData * TimeInterval)                      # counts in 0.5 s
        RealTime        = np.random.uniform(StartTime, StartTime + TimeInterval, RealData) # randomlize time of above counts in 0.5 s
        SensorID        = np.ones(RealData) * (Sensor + 1)
        RealSensorData  = (np.vstack((RealTime, SensorID))).T
        StorageSpace    = np.concatenate((StorageSpace, RealSensorData), axis=0)
    else:
        print('please select DataType!')
    return StorageSpace
#====================

### fixed variables ###
total_duration = 1000 # s
bkg_count_rate = 42.6 # #/s from 2021.06.09_CountRate_v3.pdf
#====================

### variable base on selection ###
if filename == 'big_typical1_response':
    if GRB_type_selection == 'SGRB':
        GRB_duration = 0.5            # s
        reference_fluence = 2e-5      # erg/cm^2
    elif GRB_type_selection == 'LGRB':
        GRB_duration = 10             # s
        reference_fluence = 4e-4      # erg/cm^2
    else:
        print('please select GRB type!')
elif filename == 'big_typical2_response':
    if GRB_type_selection == 'SGRB':
        GRB_duration = 0.5            # s
        reference_fluence = 4.0507e-5 # erg/cm^2
    elif GRB_type_selection == 'LGRB':
        GRB_duration = 10             # s
        reference_fluence = 8.1014e-4 # erg/cm^2
    else:
        print('please select GRB type!')
elif filename == 'big_typical3_response':
    if GRB_type_selection == 'SGRB':
        GRB_duration = 0.5            # s
        reference_fluence = 8.9764e-6 # erg/cm^2
    elif GRB_type_selection == 'LGRB':
        GRB_duration = 10             # s
        reference_fluence = 1.7952e-4 # erg/cm^2
    else:
        print('please select GRB type!')
else:
    print('please select filename!')
#====================

### main code ###
# load big table
table = np.array(pd.read_csv('./1.table/' + 'big_typical1_response.csv'))

# randomly choose src starting time
GRB_start = np.random.randint(total_duration) # s

if GRB_random_direction:
    # randomly choose src direction
    GRB_direction_index = np.random.randint(len(table))
else:
    x, y, z = Polar2Cartesian(GRB_theta, GRB_phi)
    table_xyz = table[:, 0: 3].copy()
    table_x_diff = table_xyz[:, 0] - x
    table_y_diff = table_xyz[:, 1] - y
    table_z_diff = table_xyz[:, 2] - z
    table_distance = np.array([])
    for i in range(len(table_x_diff)):
        table_distance = np.append(table_distance, table_x_diff[i]**2 + table_y_diff[i]**2 + table_z_diff[i]**2)
    GRB_direction_index = np.argmin(table_distance)
src_direction = table[GRB_direction_index, 0: 3]
src_theta_phi = Cartesian2Polar(src_direction[0], src_direction[1], src_direction[2])

# preparing src count rate
src_count_rate_list = (testing_fluence/reference_fluence) * table[GRB_direction_index, 3: 11] * 245.96 # fluence scaling * responce(area) * flux = count rate, flux refer to Ian

# preparing bkg count rate
bkg_count_rate_with_time = bkg_count_rate * (0.95 + 0.05 * np.square(np.arange(0, 1, 1/total_duration)))

# creating empty sensor data array
sensor_data = np.empty(shape=[0, 2])

# generate src & bkg signal for each sensor
for sensor in range(8):
    sensor_data = Generate_Data_Poisson('BKG'             , bkg_count_rate_with_time   , 0        , total_duration, sensor, sensor_data)
    sensor_data = Generate_Data_Poisson(GRB_type_selection, src_count_rate_list[sensor], GRB_start, GRB_duration  , sensor, sensor_data)

# rearranging by time
sensor_data = sensor_data[np.argsort(sensor_data[:, 0])]

# real GRB info. dataframe
# now = datetime.now()
# date_time = now.strftime('%m_%d_%Y_%H_%M_%S.%f')
date_time = '01_26_2022_02_01_54.583301'

real_grb_info = pd.DataFrame()
real_grb_info['GRB start']   = [GRB_start]
real_grb_info['GRB end']     = [GRB_start + GRB_duration]
real_grb_info['GRB theta']   = [src_theta_phi[0]]
real_grb_info['GRB phi']     = [src_theta_phi[1]]
real_grb_info['GRB fluence'] = [testing_fluence]
real_grb_info['UTC']         = [date_time]

# save real GRB info. .csv
real_grb_info_header = ['GRB start', 'GRB end', 'GRB theta', 'GRB phi', 'GRB fluence', 'UTC']
real_grb_info.to_csv('./2.input/' + 'real_grb_info.csv', index=False, header=real_grb_info_header)

# create lightcurve dataframe
lightcurve             = pd.DataFrame(data=sensor_data, columns=['time', 'detector'])
lightcurve['detector'] = lightcurve['detector'].astype(int)
lightcurve["pixel"]    = np.random.uniform(0, 15, len(sensor_data)).astype(int)
lightcurve["energy"]   = np.random.uniform(50, 300, len(sensor_data))

# save lightcurve .csv
lightcurve_header = ['time', 'detector', 'pixel', 'energy']
lightcurve.to_csv('./2.input/' + 'lightcurve.csv', index=False, header=lightcurve_header)

# create satellite attitude dataframe
satellite_attitude         = pd.DataFrame()
satellite_attitude['time'] = np.linspace(0, total_duration, 300)
satellite_attitude['qw']   = np.ones(300) * np.sqrt(0.5)
satellite_attitude['qx']   = np.ones(300) * np.sqrt(0.5)
satellite_attitude['qy']   = np.zeros(300)
satellite_attitude['qz']   = np.zeros(300)
satellite_attitude['ECIx'] = np.ones(300) * -12.32691165665816
satellite_attitude['ECIy'] = np.ones(300) * 4215.534296188868
satellite_attitude['ECIz'] = np.ones(300) * 5318.530945682411

# save satellite attitude .csv
satellite_attitude_header = ['time', 'qw', 'qx', 'qy', 'qz', 'ECIx', 'ECIy', 'ECIz']
satellite_attitude.to_csv('./2.input/' + 'satellite_attitude.csv', index=False, header=satellite_attitude_header)
#====================