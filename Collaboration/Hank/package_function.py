# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:11:55 2023

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







def csv2df(csv):
    
    # Convert csv to data frame
    df = pd.read_csv(csv, sep=',')
    
    return df


def slice_GTI(df,t0,t1):
        
    # Flag good time interval , relative time from t0 to t1 ,+5 sec for shift time bin
    flags = (df['Relative Time'] > t0) == (df['Relative Time'] < t1 + 5)
    
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

def plot_gtm_data(df,t0,t1,bin_size_list,sensor_name_list):
    
    trigger_time_list = []
    
    end_time_list = []
    

    for bin_size in bin_size_list:
        
        
        totalfig,totalaxe = [],[]
        
        
        for fig_number in range(2):# creat all figure we are going to use for different shift flag = 0 , 1 
            
            
            fig,axe = plt.subplots(2, 5, figsize=(15, 8), dpi=300, constrained_layout=True)
    
            totalfig.append(fig)                
            
            totalaxe.append(axe)
            
            fig.supxlabel('Time [s]')
            fig.supylabel('Count Rate [#/s]')
            fig.suptitle(f'Light Curve (time bin = {bin_size} s, shift flag = {fig_number})')
        
        for group_index,group in enumerate(sensor_name_list):
            
            threshold = []
            

            
            sliced_df = slice_GTI(df,t0,t1)

            group_df = group_data(sliced_df,group)
            
            time = group_df['Relative Time'] 
                                                                                                                                                                       
            diff = np.diff(time)
                        
            flag = (diff != 0)   
            
            flag = np.concatenate((flag ,[True]))
            
            time_correct = time[flag]
            
            tmin =  math.floor(min(time_correct))
            
            duration = t1 - t0
                 
            
            for shift in range(2):       
                
                shifter = bin_size * shift * (1/2)
                
                time_temp = time_correct[time_correct < t1 + shifter]
                
                hist, bin_edges = np.histogram(time_temp - tmin,bins=np.arange(shifter,duration + shifter + bin_size,bin_size))
                
                if np.mean(hist) > 3:
                    background = FitBKG(np.arange(shifter, duration + shifter, bin_size), hist, np.arange(shifter, duration + shifter, bin_size))
                    threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(duration/bin_size), background))
                else:
                    background = np.ones(len(hist)) * np.mean(hist)
                    threshold = poisson.ppf(1 - 0.001/(duration/bin_size), background)   
                
                trigger_time_index = np.nonzero(hist >= threshold)
                
                hist2 = np.delete(hist,trigger_time_index)
                
                if np.mean(hist2) > 3:
                    fitting_range=[]
                    for i in range(len(hist2)): 
                        fitting_range.append(i)
                    fitting_range=bin_size*np.array(fitting_range)
                    background2 = FitBKG(fitting_range, hist2, np.arange(shifter,  len(hist2)*bin_size + shifter, bin_size))
                    threshold2 = np.nan_to_num(poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2))
                else:
                    background2 = np.ones(len(hist2)) * np.mean(hist2)
                    threshold2 = poisson.ppf(1 - 0.001/( len(hist2)*bin_size/bin_size), background2)  
                
                      
                threshold2 = np.ones(len(hist)) * np.mean(threshold2)
                
                background2 = np.ones(len(hist)) * np.mean(background2)
                
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
                totalaxe[shift][group_index//5][group_index-5].set_xticks(xtick_index,list(map(str,t0+np.int_(xtick_index*bin_size))))
                # totalaxe[shift][group_index//5][group_index-5].set_ylim([0, 1600])
    
                
    if trigger_time_list == []:
        
        trigger_time, end_time = None , None
    
    else:
            
        trigger_time = np.min(trigger_time_list)
        
        end_time = np.max(end_time_list)
                
                
    
    return   trigger_time, end_time



            
def find_time_info(df,trigger_time,end_time,time_bin,sensor_name):
    
    if trigger_time != None:
        
        foward_time = 50
    
        backward_time = 50        
    
        sliced_df = slice_GTI(df,trigger_time -  foward_time , end_time +  backward_time)

        group_df = group_data(sliced_df,sensor_name)
    
    
        time = group_df['Relative Time']   
    
        diff = np.diff(time)
                    
        flag = (diff != 0)   
    
        flag = np.concatenate((flag ,[True]))
    
        time_correct = time[flag]
    
        tmin =  math.floor(min(time_correct)) 
    
        tmax =  math.ceil(max(time_correct))
    
        duration = tmax - tmin
    
        hist, bin_edges = np.histogram(time_correct - tmin,bins=np.arange(0,duration + time_bin,time_bin))
    
        head_time_to_fit = int(50/time_bin)
        
        background = FitBKG(np.concatenate((bin_edges[:head_time_to_fit],bin_edges[-head_time_to_fit:])), np.concatenate((hist[:head_time_to_fit],hist[-head_time_to_fit:])), bin_edges[:-1])
    
        src = hist - background
    
        src_cumsum = np.cumsum(src)
    
        zero_point = np.mean(src_cumsum[:head_time_to_fit])
    
        src_cumsum_correct = src_cumsum - zero_point
    
        total_flux = np.mean(src_cumsum_correct[-head_time_to_fit:])
    
        t05 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.05)))[0][0]-50
    
        t25 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.25)))[0][0]-50
    
        t75 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.75)))[0][0]-50
    
        t95 = np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.95)))[0][0]-50
    
    
        t50 = t75 - t25
        
        t90 = t95 - t05
    
        plt.figure(dpi=300)
        plt.plot(bin_edges[:-1]-50,src_cumsum_correct)
        # plt.plot(background)
        # plt.plot(hist)
        # plt.plot(src)
        plt.axvline((t05)*time_bin,color='green')
        plt.axvline((t25)*time_bin,color='red')
        plt.axvline((t75)*time_bin,color='red')
        plt.axvline((t95)*time_bin,color='green')
        plt.axvline(end_time-trigger_time+foward_time-50,color='gray')
        plt.axvline(foward_time-50,color='gray')
        plt.axhline(total_flux*0.05, color='green', linestyle='dashed')
        plt.axhline(total_flux*0.25, color='blue', linestyle='dashed')
        plt.axhline(total_flux*0.75, color='blue', linestyle='dashed')
        plt.axhline(total_flux*0.95, color='green', linestyle='dashed')
        
    else :
        group_df = group_data(df,sensor_name)
        time = group_df['Relative Time']
        
        diff = np.diff(time)
                    
        flag = (diff != 0)   
    
        flag = np.concatenate((flag ,[True]))
    
        time_correct = time[flag]
    
        tmin =  math.floor(min(time_correct)) 
    
        tmax =  math.ceil(max(time_correct))
    
        duration = tmax - tmin
        
        hist, bin_edges = np.histogram(time_correct - tmin,bins=np.arange(0,duration + time_bin,time_bin))
        
        if np.mean(hist) > 3:
            background = FitBKG(np.arange(0, duration, time_bin), hist, np.arange(0, duration, time_bin))
            threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(duration/time_bin), background))
        else:
            background = np.ones(len(hist)) * np.mean(hist)
            threshold = poisson.ppf(1 - 0.001/(duration/time_bin), background)   

        
        plt.figure(dpi=300)
        plt.plot(hist)
        plt.plot(background,color = 'red')
        plt.plot(threshold,color = 'green')
        
        
        t05, t25, t75, t95, t50, t90, src_cumsum_correct= None,None,None,None,None,None,None   
    
    return t05, t25, t75, t95, t50, t90, src_cumsum_correct

def report_info(df,sensor_name_list,trigger_time,end_time,best_bin_size,alt_info,t05, t25, t75, t95, t50, t90):
    
    dict_count = {
        'M1 SRC Count': [],'M2 SRC Count': [],'M3 SRC Count': [],'M4 SRC Count': [], 
        'S1 SRC Count': [],'S2 SRC Count': [],'S3 SRC Count': [],'S4 SRC Count': [],
        'M1 BKG Count': [],'M2 BKG Count': [],'M3 BKG Count': [],'M4 BKG Count': [],
        'S1 BKG Count': [],'S2 BKG Count': [],'S3 BKG Count': [],'S4 BKG Count': []
    
        }
    
    for sensor_name in sensor_name_list:
        
        if sensor_name != 'M' and sensor_name != 'S':
            
            foward_time_bin_num = 50
        
            backward_time_bin_num = 50        
        
            sliced_df = slice_GTI(df,trigger_time -  foward_time_bin_num , end_time +  backward_time_bin_num)
    
            group_df = group_data(sliced_df,sensor_name)
            
            time = group_df['Relative Time'] 
                                                                                                                                                                       
            diff = np.diff(time)
                        
            flag = (diff != 0)   
            
            flag = np.concatenate((flag ,[True]))
            
            time_correct = time[flag]
            
            tmin =  math.floor(min(time_correct)) 
        
            tmax =  math.ceil(max(time_correct))
        
            duration = tmax - tmin
        
            hist, bin_edges = np.histogram(time_correct - tmin,bins=np.arange(0,duration + best_bin_size,best_bin_size))
        
            head_bin_num_to_fit = int(50/best_bin_size)
            
            background = FitBKG(np.concatenate((bin_edges[:head_bin_num_to_fit],bin_edges[-head_bin_num_to_fit:])), np.concatenate((hist[:head_bin_num_to_fit],hist[-head_bin_num_to_fit:])), bin_edges[:-1])
        
            src = hist - background
            
            t05_arg = int((t05+best_bin_size*foward_time_bin_num)/best_bin_size)
            
            t95_arg = int((t95+best_bin_size*foward_time_bin_num)/best_bin_size)
            
            dict_count[f'{sensor_name} SRC Count'].append(
                np.sum(src[t05_arg:t95_arg+1])
                )
            dict_count[f'{sensor_name} BKG Count'].append(
                np.sum(background[t05_arg:t95_arg+1])
                )
            
    df_count = pd.DataFrame.from_dict(dict_count)
    
    df_alt=pd.read_csv(alt_info,sep=',')

    
    trigger_index = np.where(np.diff(np.sign(df_alt['Relative Time']-trigger_time)))[0][np.where(df_alt.loc[np.where(np.diff(np.sign(df_alt['Relative Time']-trigger_time)))]['Relative Time']!=max(df_alt['Relative Time']))[0][0]]
    
    time = recover_time(
                int(df_alt.iloc[trigger_index]['Day of Year']), 
                int(df_alt.iloc[trigger_index]['Hour']), 
                int(df_alt.iloc[trigger_index]['Minute']), 
                int(df_alt.iloc[trigger_index]['Second'])
            )
    
    df_count = pd.DataFrame.from_dict(dict_count)
    
    
    df_output = pd.concat([df_alt[['X', 'Y', 'Z', 'Q1', 'Q2', 'Q3', 'Q4']].iloc[[0]], df_count], axis=1)
    df_output.insert(0, 'T90', [t90])
    df_output.insert(0, 'T50', [t50])
    df_output.insert(0, 'Trigger2T95', [t95])
    df_output.insert(0, 'Trigger2T75', [t75])
    df_output.insert(0, 'Trigger2T25', [t25])
    df_output.insert(0, 'Trigger2T05', [t05])
    df_output.insert(0, 'Min Trigger Time Bin', [best_bin_size])
    df_output.insert(0, 'Trigger UTC', [time])
    df_output.rename(columns = {'X':'ECIx', 'Y':'ECIy', 'Z':'ECIz',
                                'Q1':'Qw', 'Q2':'Qx', 'Q3':'Qy', 'Q4':'Qz'}, inplace = True)

    df_output.to_pickle('trigger_output_test.pkl')
    
    
    return df_output


def recover_time(day_of_year, hour, minute, second): # subsecond???
    
    # Initialize year
    year = datetime.now().year
     
    # Make up 0 for strptime
    day_of_year = str(day_of_year).rjust(3, '0')
    hour = str(hour).rjust(2, '0')
    minute = str(minute).rjust(2, '0')
    second = str(second).rjust(2, '0')
     
    # Convert to date
    time = \
    datetime.strptime(f'{year}-{day_of_year} {hour}:{minute}:{second}', '%Y-%j %H:%M:%S')\
    .strftime('%Y-%m-%d %H:%M:%S')
     
    return time


           
sensor_name_list =['M','M1','M2','M3','M4','S','S1','S2','S3','S4']
# bin_size_list = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
bin_size_list = [1]
     

df = csv2df('112120.617.bin_science_pipeline_calibrated_relative_time.csv')

t0 = 300
t1 = 600
   
trigger_time,end_time = plot_gtm_data(df,t0,t1,bin_size_list,sensor_name_list)        


t05, t25, t75, t95, t50, t90, src_cumsum_correct= find_time_info(df,trigger_time,end_time,1,'S')
    

df_output_test = report_info(df,sensor_name_list,trigger_time,end_time,best_bin_size=0.01,alt_info='2023_209_010338_t0.NEET.FS8A.vc3_science_pipeline_relative_time.csv',t05=t05, t25=t25, t75=t75, t95=t95, t50=t50, t90=t90)
        



                                                                                                                                                                                                                                                              