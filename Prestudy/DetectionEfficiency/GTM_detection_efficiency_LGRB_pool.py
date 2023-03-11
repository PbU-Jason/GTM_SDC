#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 13:49:30 2022

@author: jasonpbu
"""

# package
import sys
import time
import numpy as np
import pandas as pd 
from scipy.stats import poisson
from functools import partial
from multiprocessing import set_start_method
set_start_method('fork', force=True)
from multiprocessing import Pool, Manager
#==========

# define changeable variable
used_cpu           = 40
test_number        = 10000
# check_point        = 5
GRB_type_selection = 'LGRB'
# GRB_type_selection = 'SGRB'
#==========

# function
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

## not work in paper version
# from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# from sklearn.pipeline import make_pipeline

# def BKG_Fitting(X, Y, Test_X):
#     # preprocessing data x & y to standar distribution
#     X_Scaler, Y_Scaler = StandardScaler(), StandardScaler()
#     X_Train = X_Scaler.fit_transform(X[..., None]) # X[..., None] = X.reshape(-1, 1) and giving X_Train with the similar shape
#     Y_Train = Y_Scaler.fit_transform(Y[..., None])
    
#     # fitting model
#     Model = make_pipeline(PolynomialFeatures(2), LinearRegression())
#     Model.fit(X_Train, Y_Train.ravel())
    
#     # doing some predictions
#     Predictions = Y_Scaler.inverse_transform(
#         Model.predict(X_Scaler.transform(Test_X[..., None])).reshape(-1, 1)
#     )
#     return Predictions.flatten()
## end

#==========

# define variable
## period & direction
total_duration           = 1000                                         # s
theta_phi_list           = [(45, 60), (45, -60), (45, 120), (45, -120)] # degree
##end

## bkg & src count rate
bkg_count_rate_avg       = 42.6            # #/s
LGRB_src_count_rate_list = np.array([[55, 63, 91, 73, 1520, 745, 1690, 539],
                                     [1540, 789, 1730, 595, 55, 63, 71, 72],
                                     [44, 41, 72, 46, 723, 1530, 1710, 534],
                                     [737, 1530, 1730, 595, 23, 19, 25, 24]]) # #/s
SGRB_src_count_rate_list = np.array([[33, 34, 50, 42, 576, 319, 651, 241],
                                     [612, 342, 680, 272, 33, 32, 41, 46],
                                     [24, 27, 45, 25, 299, 591, 675, 242],
                                     [217, 621, 666, 250, 12, 11, 14, 12]])   # #/s
##end

## variable base on selection
if GRB_type_selection == 'LGRB':
    GRB_duration             = 10                       # s
    src_count_rate_list_temp = LGRB_src_count_rate_list
    reference_fluence        = 4e-4                     # erg/cm^2
    fluence_array            = np.array([2, 5, 8, 9, 10, 15, 18, 21, 25, 30, 40]) * 1e-7 # erg/cm^2
elif GRB_type_selection == 'SGRB':
    GRB_duration             = 0.5                      # s
    src_count_rate_list_temp = SGRB_src_count_rate_list
    reference_fluence        = 1e-5                     # erg/cm^2
    fluence_array            = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 40]) * 1e-7 # erg/cm^2
else:
    print('please select GRB type!')
##end

## find GRB trigger
sensor_number     = 8
sensor_name       = ['NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB', 'N', 'P']
bin_size_list     = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10] # s
##end

### not work in paper version
# min_hits_intervel = 2e-6                                                              # s
### end

# ## save output info
# output_direction_case_list = []
# output_fluence_list        = []
# output_find_GRB_list       = []
# output_real_GRB_list       = []
# ##end

## save output info
manager = Manager()
output_direction_case_list = manager.list()
output_fluence_list        = manager.list()
output_find_GRB_list       = manager.list()
output_real_GRB_list       = manager.list()
##end
#==========

# function of parallelism loop
def Repeat_Find_Trigger(i, DirectionCase, Fluence, OutputDirectionCaseList, OutputFluenceList, OutputFindGRBList, OutputRealGRBList):
# def Repeat_Find_Trigger(i, UsedCpu, TestNumber, DirectionCase, Fluence, OutputDirectionCaseList, OutputFluenceList, OutputFindGRBList, OutputRealGRBList):
# for times in range(int(TestNumber/UsedCpu)):
    # # check point
    # if times % check_point == 0:
    #     print('current times:', times)
    #     print('current time :', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    
    # refresh random seed !!!
    np.random.seed()
    
    # refresh find_GRB & real_GRB
    find_GRB = 0
    real_GRB = 0
    
    # preparing src count rate
    GRB_start           = np.random.randint(total_duration)                                     # s
    src_count_rate_list = (Fluence/reference_fluence) * src_count_rate_list_temp[DirectionCase] # fluence scaling * src count rate

    # preparing bkg count rate
    # bkg_count_rate_with_time = bkg_count_rate_avg * (0.95 + 0.05 * np.square(np.arange(0, 1, 1/total_duration)))
    bkg_count_rate_with_time = bkg_count_rate_avg * np.ones(total_duration)

    # creating empty sensor data array
    sensor_data = np.empty(shape=[0, 2])

    # generate src & bkg signal for each sensor
    for sensor in range(sensor_number):
        sensor_data = Generate_Data_Poisson('BKG'             , bkg_count_rate_with_time   , 0        , total_duration, sensor, sensor_data)
        sensor_data = Generate_Data_Poisson(GRB_type_selection, src_count_rate_list[sensor], GRB_start, GRB_duration  , sensor, sensor_data)
    
    # rearranging by time
    sensor_data = sensor_data[np.argsort(sensor_data[:, 0])]
    
    # transfer to pandas format
    result             = pd.DataFrame(data=sensor_data, columns=['time', 'detector'])
    result['detector'] = result['detector'].astype(int)
    
    ## not work in paper version
    
    # result["pixel"]    = np.random.uniform(0, 15, len(sensor_data)).astype(int)
    # result["energy"]   = np.random.uniform(50, 300, len(sensor_data))
    
    # # combine hits within 2 mirco sec and filter energy 50-300 keV
    ## end
    
    sensor_data = []
    sector      = result.groupby('detector')
    for sensor_number_index in range(1, sensor_number + 1):
        raw_hit_time    = np.array(sector.get_group(sensor_number_index)['time'])
        
        ## not work in paper version
        # hits_intervel   = np.diff(raw_hit_time)
        # hits_intervel   = np.insert(hits_intervel, 0, 10)                               # 10 is just a number bigger than min_hits_intervel to make below hits_intervel > min_hits_intervel can work
        # raw_hit_time    = np.where(hits_intervel > min_hits_intervel, raw_hit_time, -1) # if hits_intervel > min_hits_intervel, then changing hits_intervel to -1
        # combined_energy = np.array(sector.get_group(sensor_number_index)['energy'])
        # for j in range(len(combined_energy)):
        #     if raw_hit_time[j] != -1:
        #         # don't need to combine energy
        #         least_non_combined_bin = j
        #     else:
        #         # need to combine energy
        #         combined_energy[least_non_combined_bin] += combined_energy[j]
        #         combined_energy[j] = -1 # make this energy can make this time to be ruled out
        # # kick out those hits with non-resolved time or non-detectable energy
        # combined_filtered_hit_time = raw_hit_time[np.logical_and(np.logical_and((raw_hit_time != -1), (combined_energy <= 300)), (combined_energy >= 50))]
        
        # # hits time list for each sensor
        # sensor_data.append(combined_filtered_hit_time) # 'NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB'
        ## end
        
        sensor_data.append(raw_hit_time) # 'NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB'
    # hits time list for sensor set
    sensor_data.append(np.concatenate((sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3]))) # 'N' set
    sensor_data.append(np.concatenate((sensor_data[4], sensor_data[5], sensor_data[6], sensor_data[7]))) # 'P' set
    
    # bin time and trigger
    real_total_duration = np.max(result['time'])
    for is_shift in range(2):
        for bin_size in bin_size_list:
            shifter = is_shift * bin_size * (1/2)
            for sensor_data_index in range(len(sensor_data)):
                hist, bin_edges = np.histogram(sensor_data[sensor_data_index], bins=np.arange(shifter, real_total_duration + bin_size + shifter, bin_size) , density=False)
                
                ## not work in paper version
                # if np.mean(hist)>3:
                #     background = BKG_Fitting(np.arange(shifter, real_total_duration + shifter, bin_size), hist, np.arange(shifter, real_total_duration + shifter, bin_size))
                #     threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background))
                # else:
                #     background = np.ones(len(hist)) * np.mean(hist)
                #     threshold = poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background)
                ## end
                
                avg = np.mean(hist)
                threshold = poisson.ppf(1-0.0001/(real_total_duration/bin_size), avg) + 1 # !!! 0.001 is good? here, I just follow previous. actually 0.0001 ~ +1
                # threshold = poisson.ppf(1-0.001/(real_total_duration/bin_size), avg)
                trigger_index = np.nonzero(hist > threshold)
                trigger = (trigger_index[0] + is_shift * (0.5)) * bin_size
                if len(trigger) != 0:
                    if all(trigger >= GRB_start - (bin_size + shifter)) and all(trigger <= GRB_start + GRB_duration + (bin_size + shifter)):
                        find_GRB = 1
                        real_GRB = 1
                    else:
                        find_GRB = 1
                        real_GRB = 0
                    break # if this break happens
            else:         # ↓
                continue  # ↓
            break         # ↓
        else:             # ↓
            continue      # ↓
        break             # break out for is_shift in range(2):
    
    # save direction_case, fluence & find_GRB
    OutputDirectionCaseList.append(DirectionCase)
    OutputFluenceList.append(Fluence)
    OutputFindGRBList.append(find_GRB)
    OutputRealGRBList.append(real_GRB)
    return
#==========
    
# main code
if __name__ == '__main__':
    # start time
    print('start time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    
    for direction_case, theta_phi in enumerate(theta_phi_list):
        for fluence in fluence_array:
            # checking
            print('GRB theta  :', theta_phi[0])
            print('GRB phi    :', theta_phi[1])
            print('GRB fluence: {:.3e}'.format(fluence))
            print('current time :', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            
            # parallelism loop
            with Pool(used_cpu) as p:
                # p.map(partial(Repeat_Find_Trigger, UsedCpu=used_cpu, TestNumber=test_number, DirectionCase=direction_case, Fluence=fluence,
                #               OutputDirectionCaseList=output_direction_case_list,
                #               OutputFluenceList=output_fluence_list,
                #               OutputFindGRBList=output_find_GRB_list,
                #               OutputRealGRBList=output_real_GRB_list), 
                #       range(used_cpu), chunksize=1) # chunksize=int(test_number/used_cpu)
                
                p.map(partial(Repeat_Find_Trigger, DirectionCase=direction_case, Fluence=fluence,
                              OutputDirectionCaseList=output_direction_case_list,
                              OutputFluenceList=output_fluence_list,
                              OutputFindGRBList=output_find_GRB_list,
                              OutputRealGRBList=output_real_GRB_list), 
                      range(test_number), chunksize=int(test_number/used_cpu))
    
    # save output info
    np.savez('GTM_' + GRB_type_selection + '_detection_efficiency_' + 'cpu_' + str(used_cpu) + '_test_' + str(test_number) + '.npz', # sys.argv[1]
             direction_case = list(output_direction_case_list), 
             fluence        = list(output_fluence_list), 
             find_GRB       = list(output_find_GRB_list),
             real_GRB       = list(output_real_GRB_list))
    
    
    # end time
    print('end time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#==========
