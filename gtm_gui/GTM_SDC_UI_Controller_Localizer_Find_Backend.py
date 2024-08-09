#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 18:00:25 2023

@author: jasonpbu & hank
"""

### package ###
import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product
import matplotlib.pyplot as plt
plt.style.use('default')
from scipy.stats import poisson
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
#====================

### function ###
def csv2df(csv):
    
    # Convert csv to data frame
    df = pd.read_csv(csv, sep=',')
    
    return df

def slice_GTI(df, t0, t1):
        
    # Flag good time interval, relative time from t0 to t1
    flags = (df['Relative Time'] >= t0) == (df['Relative Time'] <= t1)
    
    # Slice data frame
    sliced_df = df[flags]
    
    return sliced_df

def split_df(df):

    # Create empty list to store different case
    df_list = []
    df_name_list = []
    
    # Group by GTM ID
    df_grouped_gtm_id = df.groupby(['GTM ID'])
    
    # Extract grouped data
    for gtm_id in df_grouped_gtm_id.groups.keys():
        df_gtm_id_temp = df_grouped_gtm_id.get_group((gtm_id))
        
        # Cache grouped data
        df_list.append(df_gtm_id_temp)
        if gtm_id == 0: # master
            df_name_list.append('Master')
        else: # salve
            df_name_list.append('Slave')
        
        # Group by Sensor Name
        df_grouped_sensor_name = df_gtm_id_temp.groupby(['Sensor Name'])
        
        # Extract grouped data
        for sensor_name in df_grouped_sensor_name.groups.keys():
            df_sensor_name_temp = df_grouped_sensor_name.get_group((sensor_name))
            
            # Cache grouped data
            df_list.append(df_sensor_name_temp)
            df_name_list.append(sensor_name)
    
    return df_list, df_name_list

def find_trigger(file_name, df, df_list, df_name_list, bin_size_list):

    # Define data start & end time
    data_start_time = np.min(df['Relative Time'])
    data_end_time = np.max(df['Relative Time'])

    # Create empty list to store all possible trigger & end time
    trigger_time_list = []
    end_time_list = []

    for shift_flag in range(2): # with or without shift
        
        for bin_size in bin_size_list: # run all bin size
            
            # Calculate shift
            shift = bin_size * (shift_flag * 0.5)
            
            # Calculate number of bin
            bin_number = int(np.floor( (data_end_time - data_start_time - shift) / bin_size ))
            
            # Calculate bin edge
            bin_edges = np.linspace(data_start_time+shift, data_start_time+shift+(bin_number*bin_size), num=bin_number, endpoint=True)
            
            # Create empty list to store trigger & end time in certain bin size
            trigger_time_temp_list = []
            end_time_temp_list = []
            
            # Create figure
            fig, axs = plt.subplots(2, 5, figsize=(15, 8), dpi=300, constrained_layout=True)
            
            print('==============================')
            print(f'bin size  : {bin_size}')
            print(f'shift flag: {shift_flag}')
            
            for data_idx, data in enumerate(df_list): # run M, M1~4, S & S1~4
                
                data = data.groupby('Relative Time')['ADC'].sum().reset_index()
                
                # Bin data
                hist, bin_edges = \
                np.histogram(data['Relative Time'], bins=bin_edges, density=False)
                
                if np.mean(hist) > 3:
                    background = fit_bkg(bin_edges[:-1], hist, bin_edges[:-1])
                    threshold = np.nan_to_num(poisson.ppf(1 - 0.001/bin_number, background))
                    
                    hist2 = np.delete(hist, np.argwhere(hist > threshold))
                    bin_edges2 = np.delete(bin_edges[:-1], np.argwhere(hist > threshold))
                    
                    background = fit_bkg(bin_edges2, hist2, bin_edges[:-1])
                    threshold = np.nan_to_num(poisson.ppf(1 - 0.001/bin_number, background))
                else:
                    background = np.ones(len(hist)) * np.mean(hist)
                    threshold = poisson.ppf(1 - 0.001/bin_number, background)
                
                # Pick up triggered bin
                pass_threshold_arg = np.argwhere(hist > threshold)
                
                # Calculate trigger & end time in certain case
                if len(pass_threshold_arg) != 0:
                    trigger_time_temp = data_start_time + bin_size * (pass_threshold_arg[0] + (shift_flag * 0.5))
                    end_time_temp = data_start_time + bin_size * (pass_threshold_arg[-1] + (shift_flag * 0.5)) + bin_size
                    
                    print(f'{df_name_list[data_idx]}: {trigger_time_temp[0]} to {end_time_temp[0]}')
                    
                    # Cache trigger & end time in certain case
                    trigger_time_temp_list.append(trigger_time_temp)
                    trigger_time_list.append(trigger_time_temp)
                    end_time_temp_list.append(end_time_temp)
                    end_time_list.append(end_time_temp)
                    
                # Plot light curve, bkg & threshold
                ax = list(product('01', '01234'))[data_idx]
                axs[int(ax[0]), int(ax[1])].set_title(df_name_list[data_idx])
                axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], hist/bin_size, color='black')
                if np.mean(hist) > 3:
                    axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], background/bin_size, color='green')
                else:
                    axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], background/bin_size, color='blue')
                axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], threshold/bin_size, color='red')
                # axs[int(ax[0]), int(ax[1])].set_ylim([0, 1600])
            
            # # Plot min trigger & max end time in certain case
            # for ax in list(product('01', '01234')): # run all ax
            #     axs[int(ax[0]), int(ax[1])].axvline(np.min(trigger_time_temp_list), color='gray')
            #     axs[int(ax[0]), int(ax[1])].axvline(np.max(end_time_temp_list), color='gray')
            
            fig.supxlabel('Time [s]')
            fig.supylabel('Count Rate [#/s]')
            fig.suptitle(f'Light Curve (time bin = {bin_size} s, shift flag = {shift_flag})')
            fig.savefig(f'../level_2/{file_name}_lc_shift={shift_flag}_{bin_size}s.png')
            plt.close()
            
    # Calculate trigger & end time
    if trigger_time_list != []:
        trigger_time = np.min(trigger_time_list)
        end_time = np.max(end_time_list)
        print('==============================')
        print(f'Trigger time: {trigger_time}')
        print(f'End time: {end_time}')
    else:
        trigger_time = None
        end_time = None
        print('==============================')
        print('No any trigger was detected!')
    
    return trigger_time, end_time

def fit_bkg(x, y, text_x):
    
    # Preprocess data x & y to standar distribution
    scaler_x, scaler_y = StandardScaler(), StandardScaler()
    train_x = scaler_x.fit_transform(x[..., None]) # X[..., None] = X.reshape(-1, 1) and giving train_x with the similar shape
    train_y = scaler_y.fit_transform(y[..., None])
    
    # Fit model
    model = make_pipeline(LinearRegression()) # PolynomialFeatures(2)?
    model.fit(train_x, train_y.ravel())
    
    # Do some prediction
    prediction = scaler_y.inverse_transform(
        model.predict(scaler_x.transform(text_x[..., None])).reshape(-1, 1)
    )
    
    return prediction.flatten()

def find_time_info(file_name, df_list, df_name_list, trigger_time, end_time, best_bin_size, best_case_name):

    # Decide forward & backward time bin number
    forward_time_bin_number = 50
    backward_time_bin_number = 50

    # Define data with grb start & end time (trigger_time as 0)
    data_with_grb_start_time = - best_bin_size * forward_time_bin_number
    data_with_grb_end_time = end_time + best_bin_size * backward_time_bin_number - trigger_time

    # Calculate number of bin
    bin_number = int(np.floor( (data_with_grb_end_time - data_with_grb_start_time) / best_bin_size ))

    # Calculate bin edge
    bin_edges = np.linspace(data_with_grb_start_time, data_with_grb_start_time+(bin_number*best_bin_size), num=bin_number, endpoint=True)

    # Create figure
    fig, axs = plt.subplots(2, 5, figsize=(15, 8), dpi=300, constrained_layout=True)

    for data_idx, data in enumerate(df_list): # run M, M1~4, S & S1~4

        data = data.groupby('Relative Time')['ADC'].sum().reset_index()
        
        # Bin data
        hist, bin_edges = \
        np.histogram(data['Relative Time']-trigger_time, bins=bin_edges, density=False)
            
        # Fit bkg
        used_head_tail_bin = 50
        bkg = fit_bkg(x=np.concatenate((bin_edges[:used_head_tail_bin], bin_edges[-used_head_tail_bin:])), 
                      y=np.concatenate((hist[:used_head_tail_bin], hist[-used_head_tail_bin:])), 
                      text_x=bin_edges[:-1])
            
        # Plot light curve, bkg & threshold
        ax = list(product('01', '01234'))[data_idx]
        axs[int(ax[0]), int(ax[1])].set_title(df_name_list[data_idx])
        axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], hist/best_bin_size, color='black')
        axs[int(ax[0]), int(ax[1])].plot(bin_edges[:-1], bkg/best_bin_size, color='blue')
        axs[int(ax[0]), int(ax[1])].axvline(0, color='gray')
        axs[int(ax[0]), int(ax[1])].axvline(end_time-trigger_time, color='gray')
        axs[int(ax[0]), int(ax[1])].set_ylim([0, 1600])
        
        if df_name_list[data_idx] == best_case_name: # use it to decide T50 & T90
            
            # Total data - bkg = src
            src = hist - bkg
            
            # Accumulate src
            src_cumsum = np.cumsum(src)
            
            # Average accumulated src in forward time bin to get zero point
            zero_point = np.mean(src_cumsum[:forward_time_bin_number])
            
            # Correct accumulated src by zero point
            src_cumsum_correct = src_cumsum - zero_point
            
            # Average accumulated correct src in backward time bin to get total flux
            total_flux = np.mean(src_cumsum_correct[-backward_time_bin_number:])
            
            # Get t05 ~ t95
            t05 = data_with_grb_start_time + best_bin_size * (np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.05)))[0][-1]+1) # -1 for last one    
            t25 = data_with_grb_start_time + best_bin_size * (np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.25)))[0][-1]+1)
            t75 = data_with_grb_start_time + best_bin_size * (np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.75)))[0][0] +1) # 0 for first one 
            t95 = data_with_grb_start_time + best_bin_size * (np.where(np.diff(np.sign(src_cumsum_correct - total_flux * 0.95)))[0][0] +1)
            
            # Get t50 & t90
            t50 = t75 - t25
            t90 = t95 - t05

    fig.supxlabel('Time [s]')
    fig.supylabel('Count Rate [#/s]')
    fig.suptitle(f'Light Curve for Accumulation (best time bin = {best_bin_size} s)')
    fig.savefig(f'../level_2/{file_name}_lc_accumulation_{best_bin_size}s.png')
    plt.close()

    # Plot
    fig = plt.figure(dpi=300)
    plt.plot(bin_edges[:-1], src_cumsum_correct, color='black')

    plt.axvline(0, color='gray')
    plt.axvline(end_time-trigger_time, color='gray')

    plt.axhline(0, color='gray', linestyle='dashed')
    plt.axhline(total_flux, color='gray', linestyle='dashed')

    plt.axvline(t05, color='green')
    plt.axvline(t25, color='blue')
    plt.axvline(t75, color='blue')
    plt.axvline(t95, color='green')

    plt.axhline(total_flux*0.05, color='green', linestyle='dashed')
    plt.axhline(total_flux*0.25, color='blue', linestyle='dashed')
    plt.axhline(total_flux*0.75, color='blue', linestyle='dashed')
    plt.axhline(total_flux*0.95, color='green', linestyle='dashed')

    plt.xlabel('Time [s]')
    plt.ylabel('Accumulated Count [#]')
    fig.savefig(f'../level_2/{file_name}_accumulation.png')
    plt.close()
    
    return data_with_grb_start_time, data_with_grb_end_time, bin_edges, t05, t25, t75, t95, t50, t90
    
def report_trigger_info(file_name, df_list, df_name_list, trigger_time, data_with_grb_start_time, data_with_grb_end_time,\
                        t05, t25, t75, t95, t50, t90, best_bin_edges, best_bin_size): # , attitude_csv
    
    # Create dictionary to store count in t90
    dict_count = {
        'M1 SRC Count': [], 'M2 SRC Count': [], 'M3 SRC Count': [], 'M4 SRC Count': [],
        'S1 SRC Count': [], 'S2 SRC Count': [], 'S3 SRC Count': [], 'S4 SRC Count': [],
        'M1 BKG Count': [], 'M2 BKG Count': [], 'M3 BKG Count': [], 'M4 BKG Count': [],
        'S1 BKG Count': [], 'S2 BKG Count': [], 'S3 BKG Count': [], 'S4 BKG Count': [],
    }

    for data_idx, data in enumerate(df_list): # run M, M1~4, S & S1~4
        
        if (df_name_list[data_idx] != 'Master') and (df_name_list[data_idx] != 'Slave'): # only run M1~4 & S1~4
        
            # Bin data
            hist, bin_edges = \
            np.histogram(data['Relative Time']-trigger_time, bins=best_bin_edges, density=False)
                
            # Fit bkg
            used_head_tail_bin = 50
            bkg = fit_bkg(x=np.concatenate((bin_edges[:used_head_tail_bin], bin_edges[-used_head_tail_bin:])), 
                          y=np.concatenate((hist[:used_head_tail_bin], hist[-used_head_tail_bin:])), 
                          text_x=bin_edges[:-1])
            
            # Total data - bkg = src
            src = hist - bkg
            
            # Calculate arg of t05 & t95
            t05_arg = int((t05-data_with_grb_start_time)/best_bin_size)
            t95_arg = int((t95-data_with_grb_start_time)/best_bin_size)
            
            # Save count info.
            dict_count[f'{df_name_list[data_idx]} SRC Count'].append(
                np.sum(src[t05_arg:t95_arg+1])
                )
            dict_count[f'{df_name_list[data_idx]} BKG Count'].append(
                np.sum(bkg[t05_arg:t95_arg+1])
                )
            
    # Convert dictionary to df
    df_count = pd.DataFrame.from_dict(dict_count)

    # Collect time info.
    time = recover_time(
                day_of_year=158, 
                hour=2, 
                minute=0, 
                second=12, 
                # subsecond=df_attitude.iloc[0]['Subsecond']
            )
    
    dict_attitude = {
        'ECIx': [12326.91165665816], 'ECIy': [4215534.296188868], 'ECIz': [5318530.945682411], 
        'Qw': [5442], 'Qx': [24750], 'Qy': [60255], 'Qz': [20090],
        }
    df_attitude = pd.DataFrame.from_dict(dict_attitude)

    # Collect all used data to output
    df_output = pd.concat([df_attitude, df_count], axis=1)
    df_output.insert(0, 'T90', [t90])
    df_output.insert(0, 'T50', [t50])
    df_output.insert(0, 'Trigger2T95', [t95])
    df_output.insert(0, 'Trigger2T75', [t75])
    df_output.insert(0, 'Trigger2T25', [t25])
    df_output.insert(0, 'Trigger2T05', [t05])
    df_output.insert(0, 'Min Trigger Time Bin', [best_bin_size])
    df_output.insert(0, 'Trigger UTC', [time])

    # Save output df as pkl
    df_output.to_pickle(f'../level_2/{file_name}_trigger_output.pkl')
    
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
#====================

