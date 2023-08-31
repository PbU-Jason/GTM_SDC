# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:42:20 2023

@author: 2000
"""
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('classic')
import math  
from datetime import datetime
from datetime import timedelta
from scipy.stats import poisson
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

#====================


sensor_name_list =['M','M1','M2','M3','M4','S','S1','S2','S3','S4']
# bin_size_list = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
bin_size_list = [1]
# sensor_name_list =['M1']

sensor_name_list_2 = ['S']
bin_size_list_2 = [1]
#====================


def csv2df(csv):
    
    # Convert csv to data frame
    df = pd.read_csv(csv, sep=',')
    
    return df


def slice_GTI(df,t0,t1):
        
    # Flag good time interval , relative time from t0 to t1
    flags = (df['Relative Time'] > t0) == (df['Relative Time'] < t1 + 50)
    
    # Slice data frame
    sliced_df = df[flags]
    
    return sliced_df



def group_data(df,group):
    
    # define group by sensor name or GTM ID
    if len(group) == 2:
        
        #group by a specific sensor
        df = df.groupby('Sensor Name')
        
        grouped_df = df.get_group(group)
        
    else : 
        
        #group by Master or Slave
        df = df.groupby('GTM ID')
        
        if group == 'M':
            group = 0
        else :
            group = 1
        
        grouped_df = df.get_group(group)
        
    return grouped_df


def FitBKG(X, Y, TestX):
    
    # preprocessing data x & y to standard distribution
    ScalerX, ScalerY = StandardScaler(), StandardScaler()
    
    TrainX = ScalerX.fit_transform(X[..., None]) # X[..., None] = X.reshape(-1, 1) and giving TrainX with the similar shape

    TrainY = ScalerY.fit_transform(Y[..., None])
    
    # fit model
    Model = make_pipeline(LinearRegression())#PolynomialFeatures(2), 

    Model.fit(TrainX, TrainY.ravel())
    
    # do some predictions
    Predictions = ScalerY.inverse_transform(
        Model.predict(ScalerX.transform(TestX[..., None])).reshape(-1, 1)
    )
    
    return Predictions.flatten()


def plot_and_define_best_time_bin(df,t0,t1,group,bin_size):
    
    sensor_name_list = ['M1','M2','M3','M4','S1','S2','S3','S4','M','S']
    
    bin_size_list = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
    
    
    for bin_size in bin_size_list:
        for group in sensor_name_list:
    
            threshold = []
            
            # df = csv2df(csv)
            
            sliced_df = slice_GTI(df,t0,t1)
            
            group_df = group_data(sliced_df,group)
            
            time = group_df['Relative Time'] 
            
            tmin =  math.floor(min(time))
            
            duration = math.ceil(max(time)) - math.floor(min(time))
            
            
            
                 
            for shift in range(2):
                    
                shifter = bin_size * shift * (1/2)
                
                hist, bin_edges = np.histogram(time - tmin,bins=np.arange(shifter,duration + shifter + bin_size,bin_size))
                
                if np.mean(hist) > 3:
                    background = FitBKG(np.arange(shifter, duration + shifter, bin_size), hist, np.arange(shifter, duration + shifter, bin_size))
                    threshold_temp = np.nan_to_num(poisson.ppf(1 - 0.001/(duration/bin_size), background))
                else:
                    background = np.ones(len(hist)) * np.mean(hist)
                    threshold_temp = poisson.ppf(1 - 0.001/(duration/bin_size), background)
                    
                    
                trigger_time_index = np.nonzero(hist > threshold)
                
                hist2 = np.delete(hist,trigger_time_index)
                
                if np.mean(hist2) > 3:
                    background2 = FitBKG(np.arange(shifter, len(hist2)*bin_size + shifter, bin_size), hist2, np.arange(shifter,  len(hist2)*bin_size + shifter, bin_size))
                    threshold2 = np.nan_to_num(poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2))
                else:
                    background2 = np.ones(len(hist2)) * np.mean(hist2)
                    threshold2 = poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2)  
                
                
                
                
                threshold.append(threshold_temp)
        
   
    threshold = np.array(threshold).T
    
    trigger_time_index = np.nonzero(hist > threshold2)
    
    
    return   threshold
    



def plot_gtm_data(df,t0,t1,bin_size_list,sensor_name_list):
    
    trigger_time_list = []
    
    end_time_list = []
    

    for bin_size in bin_size_list:
        
        totalfig,totalaxe = [],[]
        
        for k in range(2):
            
            # figure = plt.figure()
            
            fig,axe = plt.subplots(2, 5, figsize=(15, 8), dpi=300, constrained_layout=True)
    
            totalfig.append(fig)
            
            totalaxe.append(axe)
            
            fig.supxlabel('Time [s]')
            fig.supylabel('Count Rate [#/s]')
            fig.suptitle(f'Light Curve (time bin = {bin_size} s, shift flag = {k})')
        
        for group_index,group in enumerate(sensor_name_list):
            
            threshold = []
            
            # trigger_time_temp_list = []
            
            # end_time_temp_list = []
            
            sliced_df = slice_GTI(df,t0,t1)
            
            # df = csv2df(csv)
            
            group_df = group_data(sliced_df,group)
            
            
        
            time = group_df['Relative Time']                                                                                                                                                                        
            
            tmin =  math.floor(min(time))
            
            duration = t1 - t0
                 
            
            for shift in range(2):       
                
                shifter = bin_size * shift * (1/2)
                
                time_temp = time[time < t1 + shifter]
                
                hist, bin_edges = np.histogram(time_temp - tmin,bins=np.arange(shifter,duration + shifter + bin_size,bin_size))
                
                if np.mean(hist) > 3:
                    background = FitBKG(np.arange(shifter, duration + shifter, bin_size), hist, np.arange(shifter, duration + shifter, bin_size))
                    threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(duration/bin_size), background))
                else:
                    background = np.ones(len(hist)) * np.mean(hist)
                    threshold = poisson.ppf(1 - 0.001/(duration/bin_size), background)   
                
                # threshold.append(threshold_temp)
                
           
                # threshold = np.array(threshold).T
                
                # threshold = np.ones(duration) * np.mean(threshold)
                
                # background = np.ones(duration) * np.mean(background)
                
                trigger_time_index = np.nonzero(hist > threshold)
                
                hist2 = np.delete(hist,trigger_time_index)
                
                if np.mean(hist2) > 3:
                    background2 = FitBKG(np.arange(shifter, len(hist2)*bin_size + shifter, bin_size), hist2, np.arange(shifter,  len(hist2)*bin_size + shifter, bin_size))
                    threshold2 = np.nan_to_num(poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2))
                else:
                    background2 = np.ones(len(hist2)) * np.mean(hist2)
                    threshold2 = poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2)  
                
                
                
                
                
                # trigger_time_index2 = np.nonzero(hist2 > threshold2)
                # trigger_time = (trigger_time_index2[0] + shift * (0.5)) * bin_size
                
                threshold2 = np.ones(int(duration/bin_size)) * np.mean(threshold2)
                
                background2 = np.ones(int(duration/bin_size)) * np.mean(background2)
                
                trigger_time_index =  np.argwhere(hist > threshold2)
                
                if len(trigger_time_index) != 0:
                    
                    trigger_time_temp = tmin + bin_size * trigger_time_index[0] + shifter
                    end_time_temp = tmin + bin_size * trigger_time_index[-1] + shifter+ bin_size
                    # trigger_time_temp_list.append(trigger_time_temp)
                    trigger_time_list.append(trigger_time_temp)
                    # end_time_temp_list.append(end_time_temp)
                    end_time_list.append(end_time_temp)
                    
                    
                    
                xtick_index = np.linspace(0,len(hist),7)    
                # totalaxe[shift][group_index//5][group_index-5].set_xlim([0, duration/bin_size])
                # totalaxe[shift][group_index//5][group_index-5].set_ylim([0, 3000*bin_size])
                totalaxe[shift][group_index//5][group_index-5].title.set_text(group)
                
                totalaxe[shift][group_index//5][group_index-5].plot(hist,linewidth='1.5')
                totalaxe[shift][group_index//5][group_index-5].plot(threshold2,linewidth='1.5')
                totalaxe[shift][group_index//5][group_index-5].plot(background2,linewidth='1.5')
                totalaxe[shift][group_index//5][group_index-5].set_xticks(xtick_index,list(map(str,np.int_(xtick_index*bin_size))))
                
                
    trigger_time = np.min(trigger_time_list)
    
    end_time = np.max(end_time_list)
                
                
    
    return   trigger_time, end_time

#===================================




df = csv2df('112120.617.bin_science_pipeline_calibrated_relative_time.csv')

t0 = 300
t1 = 600

trigger_time, end_time = plot_gtm_data(df,t0,t1,bin_size_list,sensor_name_list)
# a = slice_GTI(a,300,600)
# a = group_data(a,'S')
# for i in ['M','M1','M2','M3','M4','S','S1','S2','S3','S4']:
    

    
#     b.to_csv('112120.617.bin_science_pipeline_calibrated_relative_time_sliced_' + i + '_.csv', index=None)

###########################
# np.histogram(a)
# energy = a['ADC']
# time = a['Relative Time']
# tmax = math.ceil(max(time))
# tmin = math.floor(min(time))
# duration = tmax-tmin
# test_2 = []

# trigger_time_list = []
# end_time_list = []



# for bin_size in bin_size_list:
    
#     totalfig,totalaxe = [],[]
    
#     for k in range(2):
        
#         figure = plt.figure()
        
#         fig,axe = plt.subplots(2, 5, figsize=(15, 8), dpi=300, constrained_layout=True)

#         totalfig.append(fig)
        
#         totalaxe.append(axe)
        
#         fig.supxlabel('Time [s]')
#         fig.supylabel('Count Rate [#/s]')
#         fig.suptitle(f'Light Curve (time bin = {bin_size} s, shift flag = {k})')
        
        

    
    
#     for group_index,group in enumerate(sensor_name_list):
        
#         threshold = []
        
#         trigger_time_temp_list = []
        
#         end_time_temp_list = []
        
#         sliced_df = slice_GTI(df,t0,t1)
        
#         # df = csv2df(csv)
        
#         group_df = group_data(sliced_df,group)
        
        
    
#         time = group_df['Relative Time']                                                                                                                                                                        
        
#         tmin =  math.floor(min(time))
        
#         duration = t1 - t0
             
        
#         for shift in range(2):       
            
#             shifter = bin_size * shift * (1/2)
            
#             time_temp = time[time < t1 + shifter]
            
#             hist, bin_edges = np.histogram(time_temp - tmin,bins=np.arange(shifter,duration + shifter + bin_size,bin_size))
            
#             if np.mean(hist) > 3:
#                 background = FitBKG(np.arange(shifter, duration + shifter, bin_size), hist, np.arange(shifter, duration + shifter, bin_size))
#                 threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(duration/bin_size), background))
#             else:
#                 background = np.ones(len(hist)) * np.mean(hist)
#                 threshold = poisson.ppf(1 - 0.001/(duration/bin_size), background)   
            
#             # threshold.append(threshold_temp)
            
       
#             # threshold = np.array(threshold).T
            
#             # threshold = np.ones(duration) * np.mean(threshold)
            
#             # background = np.ones(duration) * np.mean(background)
            
#             trigger_time_index = np.nonzero(hist > threshold)
            
#             hist2 = np.delete(hist,trigger_time_index)
            
#             if np.mean(hist2) > 3:
#                 background2 = FitBKG(np.arange(shifter, len(hist2)*bin_size + shifter, bin_size), hist2, np.arange(shifter,  len(hist2)*bin_size + shifter, bin_size))
#                 threshold2 = np.nan_to_num(poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2))
#             else:
#                 background2 = np.ones(len(hist2)) * np.mean(hist2)
#                 threshold2 = poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2)  
            
            
            
            
            
#             # trigger_time_index2 = np.nonzero(hist2 > threshold2)
#             # trigger_time = (trigger_time_index2[0] + shift * (0.5)) * bin_size
            
#             threshold2 = np.ones(int(duration/bin_size)) * np.mean(threshold2)
            
#             background2 = np.ones(int(duration/bin_size)) * np.mean(background2)
            
#             trigger_time_index = np.argwhere(hist > threshold2)
            
#             if len(trigger_time_index) != 0:
                
#                 trigger_time_temp = tmin + bin_size * trigger_time_index[0] + shifter
#                 end_time_temp = tmin + bin_size * trigger_time_index[-1] + shifter + bin_size
#                 trigger_time_temp_list.append(trigger_time_temp)
#                 trigger_time_list.append(trigger_time_temp)
#                 end_time_temp_list.append(end_time_temp)
#                 end_time_list.append(end_time_temp)
                
                
            
#             xtick_index = np.linspace(0,len(hist),7)
            
            
#             # totalaxe[shift][group_index//5][group_index-5].set_xlim([0, duration/bin_size])
#             # totalaxe[shift][group_index//5][group_index-5].set_ylim([0, 3000*bin_size])
#             totalaxe[shift][group_index//5][group_index-5].title.set_text(group)
            
#             totalaxe[shift][group_index//5][group_index-5].plot(hist,linewidth='1.5')
#             totalaxe[shift][group_index//5][group_index-5].plot(threshold2,linewidth='2')
#             totalaxe[shift][group_index//5][group_index-5].plot(background2,linewidth='1.5')
#             totalaxe[shift][group_index//5][group_index-5].set_xticks(xtick_index,list(map(str,np.int_(xtick_index*bin_size))))
            
            
#             # plt.show()
            
#             # hist2 = np.delete(hist,trigger_time_index)
            
            
#             # hist = hist - background
            
#             # full = np.sum(hist)
            
#             # a=np.zeros(len(hist))
            
#             # for i in range(len (hist)):
                
#             #     a[i] = a[i]+ a[i-1]+hist[i]
            
            
        
# #         plt.figure(figsize=(9,6), dpi=300)
#         plt.plot(hist,linewidth='2'),plt.plot(threshold2,linewidth='2'),plt.plot(background2,linewidth='2')
# plt.title('background fitting and threshold ,Time bin = 1 (s)')
# plt.xlabel('Time (s)')
# plt.ylabel('Count rate (#/s)')
# plt.legend(['light curve','threshold','background'])
# plt.plot(a,linewidth='2')
# # plt.title('background fitting and threshold ,Time bin = 1 (s)')
# plt.xlabel('Time (s)')
# plt.ylabel('Accumulation Count (#/s)')
# # plt.legend(['light curve','threshold','background'])


###################################################=================================



sensor_name = ['S']

time_bin = 1
                
# trigger_time = np.min(trigger_time_list)
    
# end_time = np.max(end_time_list)
    

foward_time_bin_num = 70

backward_time_bin_num = 50         


sliced_df = slice_GTI(df,trigger_time - time_bin * foward_time_bin_num,end_time + time_bin * backward_time_bin_num)

# df = csv2df(csv)
group_df = group_data(sliced_df,sensor_name)


time = group_df['Relative Time']   

tmin =  math.floor(min(time)) 

tmax =  math.ceil(max(time))

duration = tmax - tmin

hist, bin_edges = np.histogram(time - tmin,bins=np.arange(0,duration + time_bin,time_bin))


head_bin_num_to_fit = 50

background = FitBKG(np.concatenate((bin_edges[:head_bin_num_to_fit],bin_edges[-head_bin_num_to_fit:])), np.concatenate((hist[:head_bin_num_to_fit],hist[-head_bin_num_to_fit:])), bin_edges[:-1])

src = hist - background

src_cumsum = np.cumsum(src)

zero_point = np.mean(src_cumsum[:head_bin_num_to_fit])

src_cumsum_correct = src_cumsum - zero_point

total_flux = np.mean(src_cumsum_correct[-head_bin_num_to_fit:])

t05 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.05)))[0][0]

t25 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.25)))[0][0]

t75 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.75)))[0][0]

t95 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.95)))[0][0]



plt.figure()
plt.plot(src_cumsum_correct)
plt.plot(background)
plt.plot(hist)
# plt.plot(src)
plt.axvline(t05)
plt.axvline(t25)
plt.axvline(t75)
plt.axvline(t95)
plt.axvline(end_time-trigger_time+foward_time_bin_num*time_bin,color='gray')
plt.axvline(foward_time_bin_num*time_bin,color='gray')