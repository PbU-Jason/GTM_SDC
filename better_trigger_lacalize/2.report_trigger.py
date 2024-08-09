#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
import numpy as np
import pandas as pd
from itertools import product
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('default')

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

from scipy.stats import poisson
#====================

### variable ###

# GRB properties
# test_fluence = 4e-6 # erg/cm^2
test_fluence = 4e-5 # erg/cm^2
grb_theta = 45 # deg, in mass-model coordinate
grb_phi   = 60 # deg, in mass-model coordinate

# Time properties
bin_size_list = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10] # s
trigger_backward_time = 30 # s
trigger_forward_time  = 30 # s
trigger_forward_gap   = 10 # s

# Setup for plot
plot_order_list = [6, 7, 5, 4, 9, # 'PT', 'PB', 'PP', 'PN', 'P'
                   2, 3, 1, 0, 8] # 'NT', 'NB', 'NP', 'NN', 'N'   
plot_axs = list(product([0, 1], [0, 1, 2, 3, 4]))   
plot_color_list = ['#ff9999', '#ff9999', '#ff9999', '#ff9999', '#ff6666',
                   '#99ccff', '#99ccff', '#99ccff', '#99ccff', '#6699ff',]  
sensor_list = ['NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB', 'N', 'P']

#====================

### function ###
def fit_gkb(input_x, input_y, output_x):
    # Preprocess data x & y to standar distribution
    scaler_x, scaler_y = StandardScaler(), StandardScaler()
    train_x = scaler_x.fit_transform(input_x[..., None]) # [..., None] = .reshape(-1, 1) to match shape
    train_y = scaler_y.fit_transform(input_y[..., None])
    # Fit model
    model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model.fit(train_x, train_y.ravel())
    # Predict
    Predictions = scaler_y.inverse_transform(
        model.predict(scaler_x.transform(output_x[..., None])).reshape(-1, 1)
    )
    return Predictions.flatten()
#====================

### main code ###

# Load data
real_grb_info = pd.read_csv(f'./1.input/real_grb_info_{test_fluence}_{grb_theta}_{grb_phi}.csv')
lightcurve = pd.read_csv(f'./1.input/lightcurve_{test_fluence}_{grb_theta}_{grb_phi}.csv')
satellite_attitude = pd.read_csv(f'./1.input/satellite_attitude_{test_fluence}_{grb_theta}_{grb_phi}.csv')

# Derive info from data
utc = datetime.strptime(real_grb_info['UTC'][0], '%Y_%m_%d_%H_%M_%S.%f')
real_total_duration = np.max(lightcurve['Time'])

# Extract data and combine module
sensor_data = []
lightcurve_grouped = lightcurve.groupby('Detector')
for sensor in range(8):
    raw_time = np.array(lightcurve_grouped.get_group(sensor+1)['Time'])
    sensor_data.append(raw_time) # 'NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB'
sensor_data.append(np.concatenate((sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3]))) # 'N' set
sensor_data.append(np.concatenate((sensor_data[4], sensor_data[5], sensor_data[6], sensor_data[7]))) # 'P' set

# Create empty array to store trigger
print('Finding trigger...')
trigger_info = np.empty(shape=[0, 4])
for is_shift in range(2):
    for bin_size in bin_size_list:
        shifter = is_shift * 0.5 * bin_size
        for data_idx in range(len(sensor_data)):
            R = np.array([]) # empty array to store significance
            hist, bin_edges = np.histogram(sensor_data[data_idx], 
                                           bins=np.arange(shifter, real_total_duration+bin_size, bin_size), 
                                           density=False)
            if np.mean(hist) > 3: # bigger time bin, can fit bkg
                background = fit_gkb(np.arange(shifter, real_total_duration, bin_size), hist,
                                     np.arange(shifter, real_total_duration, bin_size))
            else: # smaller time bin, can't fit bkg
                background = np.ones(len(hist)) * np.mean(hist)
            threshold = poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background)
            trigger_time_idx = np.nonzero(hist > threshold)[0]
            trigger_time_hist = hist[trigger_time_idx]
            for time_hist, time_idx in zip(trigger_time_hist, trigger_time_idx):
                R = np.append(R, poisson.sf(time_hist, background[time_idx])) # significance
            trigger_time = (trigger_time_idx + is_shift * 0.5) * bin_size
            if len(trigger_time) != 0:
                print('T:', trigger_time)
                print('R:', R)
                trigger_info_temp = (np.vstack((trigger_time, 
                                                bin_size * np.ones(len(trigger_time)), 
                                                (data_idx) * np.ones(len(trigger_time)).astype(int), 
                                                R))).T
                trigger_info = np.concatenate((trigger_info, trigger_info_temp), axis=0) 
#%%

# Plot min time bin, min R's time bin, and maybe 0.1 s (if bright enough)
min_trigger_time_bin = np.min(trigger_info[:, 1])
min_R_time_bin = trigger_info[np.argmin(trigger_info[:, 3]), 1]
if min_trigger_time_bin >= 0.1:
    plot_bin_list = [min_trigger_time_bin, min_R_time_bin]
else:
    plot_bin_list = [min_trigger_time_bin, min_R_time_bin, 0.1]
for bin_size in plot_bin_list:
    
    # Define time range
    trigger_time_list  = [trigger_info[i][0] for i in np.argwhere(trigger_info[:, 1] == bin_size).flatten()]
    first_trigger_time = np.min(trigger_time_list)
    last_trigger_time  = np.max(trigger_time_list) + bin_size
    window_front       = first_trigger_time - trigger_backward_time
    window_back        = last_trigger_time + trigger_forward_time
    window_duration    = window_back - window_front
    sensor_data_for_plot = [
        sensor_data[i][
            np.logical_and(sensor_data[i] >= window_front, 
                           sensor_data[i] <= window_back)
            ] for i in range(10)
        ]
    
    # Derive uniform plot y range
    count_rate_range_list = []
    for plot_idx, plot_order in enumerate(plot_order_list):
        hist, bin_edges = np.histogram(
            sensor_data_for_plot[plot_order], 
            bins=np.linspace(window_front, 
                             window_back, 
                             int(window_duration/bin_size)+1, 
                             endpoint=True), 
            density=False)
        count_rate_range_list.append([np.min(hist/bin_size), np.max(hist/bin_size)])
    plot_min_single_sensor = np.min([count_rate_range_list[i][0] for i in [0, 1, 2, 3, 5, 6, 7, 8]])
    plot_max_single_sensor = np.max([count_rate_range_list[i][1] for i in [0, 1, 2, 3, 5, 6, 7, 8]])
    plot_min_sensor_set    = np.min([count_rate_range_list[i][0] for i in [4, 9]])
    plot_max_sensor_set    = np.max([count_rate_range_list[i][1] for i in [4, 9]])
    
    # Plot figure
    fig1, ax1 = plt.subplots(2, 5, figsize=(10, 5))
    for plot_idx, plot_order in enumerate(plot_order_list):
        
        # Select axis
        ax = plot_axs[plot_idx]
        
        # Fill real GRB region
        ax1[ax[0], ax[1]].axvspan(real_grb_info['GRB Start'][0] - first_trigger_time, 
                                  real_grb_info['GRB End'][0] - first_trigger_time, 
                                  facecolor='gray', alpha=0.1, zorder=0)
        
        # Plot lightcurve
        hist, bin_edges = np.histogram(
            sensor_data_for_plot[plot_order], 
            bins=np.linspace(window_front, 
                             window_back, 
                             int(window_duration/bin_size)+1,
                             endpoint=True), 
            density=False)
        hist = np.append(hist, hist[-1]) # match bin_edges size
        ax1[ax[0], ax[1]].step(bin_edges - first_trigger_time, hist/bin_size, where='post', 
                               color=plot_color_list[plot_idx], linewidth=1, zorder=1) # hist/bin_size = #/s per time bin
        
        # Check bkg and threshold
        hist, bin_edges = np.histogram(sensor_data[plot_order], 
                                       bins=np.arange(0, real_total_duration+bin_size, bin_size), 
                                       density=False)
        if np.mean(hist) > 3: # bigger time bin, can fit bkg
            background = fit_gkb(np.arange(0, real_total_duration, bin_size), hist,
                                 np.arange(0, real_total_duration, bin_size))
        else: # smaller time bin, can't fit bkg
            background = np.ones(len(hist)) * np.mean(hist)
        threshold = poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background)
        ax1[ax[0], ax[1]].plot(bin_edges[:-1] - first_trigger_time, background/bin_size,
                               linestyle='--', color='black', linewidth=1, zorder=2)
        ax1[ax[0], ax[1]].plot(bin_edges[:-1] - first_trigger_time, threshold/bin_size,
                               linestyle=':', color='black', linewidth=1, zorder=2)
        
        # Adjust plot range
        ax1[ax[0], ax[1]].set_xlim([window_front - first_trigger_time, window_back - first_trigger_time])
        if plot_idx != 4 and plot_idx != 9:
            ax1[ax[0], ax[1]].set_ylim([(10 * int(plot_min_single_sensor/10)), (10 * int(plot_max_single_sensor/10) + 10)])
        else:
            ax1[ax[0], ax[1]].set_ylim([(10 * int(plot_min_sensor_set/10)), (10 * int(plot_max_sensor_set/10) + 10)])
        
        # Adjust tick label
        ax1[ax[0], ax[1]].tick_params(axis='both', which='major', labelsize=10)
        if ax[0] == 0 and (ax[1] == 0 or ax[1] == 1 or ax[1] == 2 or ax[1] == 3 or ax[1] == 4):
            ax1[ax[0], ax[1]].set_xticklabels([])
        
        # Add detector name
        ax1[ax[0], ax[1]].text(0.2, 0.9, 
                               f'{sensor_list[plot_order]}', color='black', fontweight='bold', fontsize=10,
                               horizontalalignment='center', verticalalignment='center',
                               transform=ax1[ax[0], ax[1]].transAxes, zorder=3)
    
    # Save figure
    fig1.supxlabel('Time [s]', fontsize=10)
    fig1.supylabel('Count Rate [#/s]', fontsize=10)
    fig1.tight_layout()
    fig1.savefig(f'./2.trigger/lightcurve_{test_fluence}_bin_{bin_size}s_{grb_theta}_{grb_phi}.png', dpi=300)
    plt.close(fig1)
    
#%%

# Redefine time range for hole range
first_trigger_time   = np.min(trigger_info[:, 0])
last_trigger_time    = np.max(trigger_info[:, 0]) + trigger_info[np.argmax(trigger_info[:, 0]), 1]
window_front    = first_trigger_time - trigger_backward_time
window_back     = last_trigger_time + trigger_forward_time

# Find most significant data
min_R_data = int(trigger_info[np.argmin(trigger_info[:, 3]), 2])

# Extract useful data from most significance
hist, bin_edges = np.histogram(sensor_data[min_R_data], 
                               bins=np.arange(0, real_total_duration+min_trigger_time_bin, min_trigger_time_bin), 
                               density=False)
# # See possible uncertainty of real data (only pre and post window to fit bkg)
# hist_pre_post = np.concatenate((hist[int(window_front/min_trigger_time_bin): int(first_trigger_time/min_trigger_time_bin)], 
#                                 hist[int(last_trigger_time/min_trigger_time_bin)+1: int(window_back/min_trigger_time_bin)+1]))
# time_pre_post = np.concatenate((np.arange(window_front, first_trigger_time, min_trigger_time_bin), 
#                                 np.arange(last_trigger_time+min_trigger_time_bin, 
#                                           window_back+min_trigger_time_bin, 
#                                           min_trigger_time_bin)))
hist_for_plot = hist[int(window_front/min_trigger_time_bin): int(window_back/min_trigger_time_bin)+1]
time_for_plot = np.arange(window_front, window_back+min_trigger_time_bin, min_trigger_time_bin)[:len(hist_for_plot)] # np.arange bug

# Fit bkg to define zero and total level
# # See possible uncertainty of real data (only pre and post window to fit bkg)
# bkg             = fit_gkb(time_pre_post, hist_pre_post, time_for_plot)
bkg = fit_gkb(np.arange(0, real_total_duration, min_trigger_time_bin), hist, time_for_plot)
hist_src        = hist_for_plot - bkg
hist_src_cumsum = np.cumsum(hist_src)
zero_point      = np.mean(hist_src_cumsum[:int(trigger_backward_time/min_trigger_time_bin)])
hist_src_cumsum = hist_src_cumsum - zero_point
total_flux      = np.mean(hist_src_cumsum[int(len(hist_src_cumsum) - (trigger_forward_time - trigger_forward_gap)/min_trigger_time_bin):])

# Plot accumulative lightcruve
fig = plt.figure()
plt.step(time_for_plot - first_trigger_time, hist_src_cumsum, where='post', zorder=1)

# Calculate GRB duration
T25 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.25)))[0][-1]+1) * min_trigger_time_bin + window_front
T75 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.75)))[0][0] +1) * min_trigger_time_bin + window_front
T50 = T75 - T25
T05 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.05)))[0][-1]+1) * min_trigger_time_bin + window_front
T95 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.95)))[0][0] +1) * min_trigger_time_bin + window_front
T90 = T95 - T05

# Label GRB duration on accumulative lightcruve
T05_to_trigger = T05 - first_trigger_time
T25_to_trigger = T25 - first_trigger_time
T75_to_trigger = T75 - first_trigger_time
T95_to_trigger = T95 - first_trigger_time
plt.hlines(y=zero_point, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.hlines(y=total_flux * 0.05, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.hlines(y=total_flux * 0.25, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.hlines(y=total_flux * 0.75, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.hlines(y=total_flux * 0.95, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.hlines(y=total_flux, xmin=window_front-first_trigger_time, xmax=window_back-first_trigger_time, color='gray', linestyles=':', zorder=2)
plt.vlines(x=T05_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='r', linestyles='--', zorder=4)
plt.vlines(x=T25_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='b', linestyles='--', zorder=3)
plt.vlines(x=T75_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='b', linestyles='--', zorder=3)
plt.vlines(x=T95_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='r', linestyles='--', zorder=4)

# Check real GRB
plt.axvspan(real_grb_info['GRB Start'][0] - first_trigger_time, 
            real_grb_info['GRB End'][0] - first_trigger_time, 
            facecolor='gray', alpha=0.1, zorder=0)

plt.xlabel('Time [s]')
plt.ylabel('Accumulative Count [#]')
fig.tight_layout()
fig.savefig(f'./2.trigger/accumulative_{test_fluence}_minBin_{min_trigger_time_bin}s_minR_{sensor_list[min_R_data]}_{grb_theta}_{grb_phi}.png', dpi=300)

#%%

# Extract bkg and src to as output
bkg_for_each_sensor = []
src_for_each_sensor = []
for sensor_idx in range(8):
    hist, bin_edges = np.histogram(sensor_data[sensor_idx], 
                                   bins=np.arange(0, real_total_duration+min_trigger_time_bin, min_trigger_time_bin), 
                                   density=False)
    hist_for_plot = hist[int(window_front/min_trigger_time_bin): int(window_back/min_trigger_time_bin)+1]
    time_for_plot = np.arange(window_front, window_back+min_trigger_time_bin, min_trigger_time_bin)[:len(hist_for_plot)]
    bkg = fit_gkb(np.arange(0, real_total_duration, min_trigger_time_bin), hist, time_for_plot)
    hist_src = hist_for_plot - bkg
    bkg_for_each_sensor.append(bkg)
    src_for_each_sensor.append(hist_src)
    
# Sum over bkg and src counts in T90
sensor_bkg_count_list = []
sensor_src_count_list = []
for sensor_idx in range(8):
    sensor_bkg_count_list.append(np.sum(bkg_for_each_sensor[sensor_idx][
        int((trigger_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_backward_time + T95_to_trigger)/min_trigger_time_bin)+1
        ]))
    sensor_src_count_list.append(np.sum(src_for_each_sensor[sensor_idx][
        int((trigger_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_backward_time + T95_to_trigger)/min_trigger_time_bin)+1
        ]))

# Mimic to deal with attitude data
satellite_attitude = pd.read_csv(f'./1.input/satellite_attitude_{test_fluence}_{grb_theta}_{grb_phi}.csv')
trigger_mid_time       = (T25 + T75)/2
trigger_mid_time_idx = (np.abs(satellite_attitude['Time'] - trigger_mid_time)).argmin()
Qw   = satellite_attitude['Qw'][trigger_mid_time_idx]
Qx   = satellite_attitude['Qx'][trigger_mid_time_idx]
Qy   = satellite_attitude['Qy'][trigger_mid_time_idx]
Qz   = satellite_attitude['Qz'][trigger_mid_time_idx]
ECIx = satellite_attitude['ECIx'][trigger_mid_time_idx]
ECIy = satellite_attitude['ECIy'][trigger_mid_time_idx]
ECIz = satellite_attitude['ECIz'][trigger_mid_time_idx]

# Save trigger output
trigger_output = pd.DataFrame({
    'Trigger UTC': [real_grb_info['UTC'][0]], 
    'Trigger Min Time Bin': [min_trigger_time_bin],
    'T50': [round(T50, 3)],
    'T90': [round(T90, 3)],
    'NN SRC Count': [sensor_src_count_list[0]], 
    'NP SRC Count': [sensor_src_count_list[1]], 
    'NT SRC Count': [sensor_src_count_list[2]], 
    'NB SRC Count': [sensor_src_count_list[3]], 
    'PN SRC Count': [sensor_src_count_list[4]], 
    'PP SRC Count': [sensor_src_count_list[5]], 
    'PT SRC Count': [sensor_src_count_list[6]], 
    'PB SRC Count': [sensor_src_count_list[7]], 
    'NN BKG Count': [sensor_bkg_count_list[0]], 
    'NP BKG Count': [sensor_bkg_count_list[1]], 
    'NT BKG Count': [sensor_bkg_count_list[2]], 
    'NB BKG Count': [sensor_bkg_count_list[3]], 
    'PN BKG Count': [sensor_bkg_count_list[4]], 
    'PP BKG Count': [sensor_bkg_count_list[5]], 
    'PT BKG Count': [sensor_bkg_count_list[6]], 
    'PB BKG Count': [sensor_bkg_count_list[7]], 
    'Qw': [Qw], 'Qx': [Qx], 'Qy': [Qy], 'Qz': [Qz], 
    'ECIx': [ECIx], 'ECIy': [ECIy], 'ECIz': [ECIz], 
    })
trigger_output.to_csv(f'./2.trigger/trigger_output_{test_fluence}_{grb_theta}_{grb_phi}.csv', index=False)
#====================