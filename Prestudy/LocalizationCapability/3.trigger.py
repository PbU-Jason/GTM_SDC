#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### package ###
from math import floor
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from datetime import datetime
from datetime import timedelta
from scipy.stats import poisson
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
#====================

### selection ###
# filename
filename_list = ['real_grb_info.csv', 'lightcurve.csv', 'satellite_attitude.csv']
#====================

### function ###
def FitBKG(X, Y, TestX):
    # preprocessing data x & y to standar distribution
    ScalerX, ScalerY = StandardScaler(), StandardScaler()
    TrainX = ScalerX.fit_transform(X[..., None]) # X[..., None] = X.reshape(-1, 1) and giving TrainX with the similar shape
    TrainY = ScalerY.fit_transform(Y[..., None])
    # fit model
    Model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    Model.fit(TrainX, TrainY.ravel())
    # do some predictions
    Predictions = ScalerY.inverse_transform(
        Model.predict(ScalerX.transform(TestX[..., None])).reshape(-1, 1)
    )
    return Predictions.flatten()

def FindExponent(Number):
    Exponent10 = np.log10(Number)
    return floor(Exponent10)

def FindCoefficient(Number, Exponent10):
    Coefficient = Number/(10**Exponent10)
    return Coefficient
#====================

### fixed variables ###
sensor_number     = 8
sensor_name_list  = ['NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB', 'N', 'P']
min_hits_intervel = 2e-6 
bin_size_list     = [0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
plot_order_list   = [0, 1, 2, 3, 8, # 'NN', 'NP', 'NT', 'NB', 'N'
                     4, 5, 6, 7, 9] # 'PN', 'PP', 'PT', 'PB', 'P'
trigger_plot_backward_time = 30
trigger_plot_forward_time  = 30
trigger_plot_forward_gap   = 10
#====================

### main code ###
# load real GRB info. data
real_grb_info = pd.read_csv('./2.input/' + filename_list[0])
fluence_exponent    = FindExponent(real_grb_info['GRB fluence'][0])
fluence_coefficient = FindCoefficient(real_grb_info['GRB fluence'][0], fluence_exponent)
UTC_lightcurve_start_time = datetime.strptime(real_grb_info['UTC'][0], '%m_%d_%Y_%H_%M_%S.%f')

# load lightcurve data
lightcurve = pd.read_csv('./2.input/' + filename_list[1]) # skiprows=[0] to remove starting UTC, but it doesn't work now

# combine hits within 2 ms and filter energy 50-300 keV
sensor_data = []
sector      = lightcurve.groupby('detector')
for i in range(1, sensor_number+1):
    raw_hit_time    = np.array(sector.get_group(i)['time'])
    hits_intervel   = np.diff(raw_hit_time)
    hits_intervel   = np.insert(hits_intervel, 0, 10)                               # 10 is just a number bigger than min_hits_intervel to make below hits_intervel > min_hits_intervel can work
    raw_hit_time    = np.where(hits_intervel > min_hits_intervel, raw_hit_time, -1) # if hits_intervel > min_hits_intervel, then changing hits_intervel to -1
    combined_energy = np.array(sector.get_group(i)['energy'])
    for j in range(len(combined_energy)):
        if raw_hit_time[j] != -1:
            # don't need to combine energy
            least_non_combined_bin = j
        else:
            # need to combine energy
            combined_energy[least_non_combined_bin] += combined_energy[j]
            combined_energy[j] = -1 # make this energy can make this time to be ruled out
    # kick out those hits with non-resolved time or non-detectable energy
    combined_filtered_hit_time = raw_hit_time[np.logical_and(np.logical_and((raw_hit_time != -1), (combined_energy <= 300)), (combined_energy >= 50))]
    
    # hits time list for each sensor
    sensor_data.append(combined_filtered_hit_time) # 'NN', 'NP', 'NT', 'NB', 'PN', 'PP', 'PT', 'PB'
    
# hits time list for sensor set
sensor_data.append(np.concatenate((sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3]))) # 'N' set
sensor_data.append(np.concatenate((sensor_data[4], sensor_data[5], sensor_data[6], sensor_data[7]))) # 'P' set

# creating empty trigger info. array
trigger_info = np.empty(shape=[0, 4])

# bin time and trigger
real_total_duration = np.max(lightcurve['time'])
for is_shift in range(2):
    for bin_size in bin_size_list:
        shifter = is_shift * bin_size * (1/2)
        for i in range(len(sensor_data)):
            R = np.array([])
            hist, bin_edges = np.histogram(sensor_data[i], bins=np.arange(shifter, real_total_duration + bin_size + shifter, bin_size) , density=False)
            if np.mean(hist) > 3:
                background = FitBKG(np.arange(shifter, real_total_duration + shifter, bin_size), hist, np.arange(shifter, real_total_duration + shifter, bin_size))
                threshold = np.nan_to_num(poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background))
            else:
                background = np.ones(len(hist)) * np.mean(hist)
                threshold = poisson.ppf(1 - 0.001/(real_total_duration/bin_size), background)
            trigger_time_index = np.nonzero(hist > threshold)
            trigger_time_hist = hist[trigger_time_index]
            for time_hist, time_index in zip(trigger_time_hist, trigger_time_index):
                R = np.append(R, poisson.sf(time_hist, background[time_index]))
            trigger_time = (trigger_time_index[0] + is_shift * (0.5)) * bin_size
            if len(trigger_time) != 0:
                print('T:', trigger_time)
                print('R:', R)
                trigger_info_temp = (np.vstack((trigger_time, bin_size * np.ones(len(trigger_time)), (i+1) * np.ones(len(trigger_time)).astype(int), R))).T
                trigger_info = np.concatenate((trigger_info, trigger_info_temp), axis=0) 

# plot some figures depending on trigger
## without tirgger
if len(trigger_info) == 0: 
    # plot 0.1 & 2 s case
    for bin_size in [0.1, 2]: # s
        fig, ax = plt.subplots()
        for i in range(len(plot_order_list)):
            hist, bin_edges = np.histogram(sensor_data[plot_order_list[i]], bins=np.arange(0, real_total_duration + bin_size, bin_size) , density=False)
            plt.subplot(2, 5, i+1)
            plt.plot(np.arange(0, real_total_duration, bin_size), hist) # here use # per time bin due to low count rate!
            plt.title(sensor_name_list[plot_order_list[i]])
            plt.xlabel('Time [s]')
            plt.ylabel('Count [#]') 
        fig.suptitle('Lightcurve (bin size = ' + str(bin_size) + ' s)')
## with tirgger
else:                
    # plot min trigger time bin and 0.1 s case
    min_trigger_time_bin = np.min(trigger_info[:,1])
    check_min_count = 0
    for bin_size in [min_trigger_time_bin, 0.1]: # s
        # define time range base on time bin
        first_trigger_time   = np.min([trigger_info[i][0] for i in np.argwhere(trigger_info[:, 1] == bin_size).flatten()])
        last_trigger_time    = np.max([trigger_info[i][0] for i in np.argwhere(trigger_info[:, 1] == bin_size).flatten()]) + bin_size
        plot_window_front    = first_trigger_time - trigger_plot_backward_time
        plot_window_back     = last_trigger_time + trigger_plot_forward_time
        plot_window_duration = plot_window_back - plot_window_front
        sensor_data_for_plot = [sensor_data[i][np.logical_and(sensor_data[i] >= plot_window_front, sensor_data[i] <= (plot_window_front + bin_size * (int(plot_window_duration/bin_size) + 1)))] for i in range(10)]
        
        # find proper plot range
        count_rate_range_list = []
        for i in range(len(plot_order_list)):
            hist, bin_edges = np.histogram(sensor_data_for_plot[plot_order_list[i]], bins=np.linspace(plot_window_front, plot_window_front + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), density=False)
            count_rate_range_list.append([np.min(hist/bin_size), np.max(hist/bin_size)])
        plot_min_single_sensor = np.min([count_rate_range_list[i][0] for i in [0, 1, 2, 3, 5, 6, 7, 8]])
        plot_max_single_sensor = np.max([count_rate_range_list[i][1] for i in [0, 1, 2, 3, 5, 6, 7, 8]])
        plot_min_sensor_set    = np.min([count_rate_range_list[i][0] for i in [4, 9]])
        plot_max_sensor_set    = np.max([count_rate_range_list[i][1] for i in [4, 9]])
        
        # plot lightcurve
        fig, ax = plt.subplots(figsize=(16, 8))
        for i in range(len(plot_order_list)):
            plt.subplot(2, 5, i+1)
            plt.axvspan(real_grb_info['GRB start'][0] - first_trigger_time, real_grb_info['GRB end'][0] - first_trigger_time, facecolor='#ffffff', alpha=0.3, zorder=0) # fill real GRB region
            hist, bin_edges = np.histogram(sensor_data_for_plot[plot_order_list[i]], bins=np.linspace(plot_window_front, plot_window_front + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), density=False)
            hist = np.append(hist, hist[-1])
            if i in [0, 1, 2, 3]:
                plt.step(np.linspace(-trigger_plot_backward_time, -trigger_plot_backward_time + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), hist/bin_size, 
                         where='post', color='#ff9999', linewidth=1.7, zorder=5) # hist/bin_size = #/s per time bin
            elif i == 4:
                plt.step(np.linspace(-trigger_plot_backward_time, -trigger_plot_backward_time + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), hist/bin_size, 
                         where='post', color='#ff6666', linewidth=1.7, zorder=5) 
            elif i in [5, 6, 7, 8]:
                plt.step(np.linspace(-trigger_plot_backward_time, -trigger_plot_backward_time + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), hist/bin_size, 
                         where='post', color='#99ccff', linewidth=1.7, zorder=5)
            elif i == 9:
                plt.step(np.linspace(-trigger_plot_backward_time, -trigger_plot_backward_time + bin_size * (int(plot_window_duration/bin_size) + 1), (int(plot_window_duration/bin_size) + 1) + 1, endpoint=True), hist/bin_size, 
                         where='post', color='#6699ff', linewidth=1.7, zorder=5) 
            else:
                print('check plot!')
            if i != 4 and i != 9:
                # plt.vlines(x=0, ymin=(10 * int(plot_min_single_sensor/10)), ymax=(10 * int(plot_max_single_sensor/10) + 50), color='#ffffff', linestyles='dashed', linewidth=1.7, zorder=10)
                # plt.vlines(x=last_trigger_time-first_trigger_time, ymin=(10 * int(plot_min_single_sensor/10)), ymax=(10 * int(plot_max_single_sensor/10) + 50), color='#ffffff', linestyles='dashed', linewidth=1.7, zorder=10)
                plt.ylim([(10 * int(plot_min_single_sensor/10)), (10 * int(plot_max_single_sensor/10) + 10)])
            else:
                # plt.vlines(x=0, ymin=(10 * int(plot_min_sensor_set/10)), ymax=(10 * int(plot_max_sensor_set/10) + 50), color='#ffffff', linestyles='dashed', linewidth=1.7, zorder=10)
                # plt.vlines(x=last_trigger_time-first_trigger_time, ymin=(10 * int(plot_min_sensor_set/10)), ymax=(10 * int(plot_max_sensor_set/10) + 50), color='#ffffff', linestyles='dashed', linewidth=1.7, zorder=10)
                plt.ylim([(10 * int(plot_min_sensor_set/10)), (10 * int(plot_max_sensor_set/10) + 10)])
            plt.annotate(sensor_name_list[plot_order_list[i]], xy=(0.07, 0.95), xycoords='axes fraction', fontsize=18, weight='bold', horizontalalignment='left', verticalalignment='top')
            if i in range(5):
                plt.title(' ', fontsize=17)
            plt.xlabel('Time [s]', fontsize=15, weight='bold')
            plt.ylabel('Count Rate [#/s]', fontsize=15, weight='bold')
            plt.xlim([-trigger_plot_backward_time,  -trigger_plot_backward_time + bin_size * (int(plot_window_duration/bin_size) + 1)])
            plt.xticks(fontsize=15, weight='bold')
            plt.yticks(fontsize=15, weight='bold')
        # fig.legend([plt.axvspan(-100, -90, facecolor='#ffffff', alpha=0.3), 
        #             plt.vlines(x=0, ymin=(10 * int(plot_min_single_sensor/10)), ymax=(10 * int(plot_max_single_sensor/10) + 50), color='#ffffff', linestyles='dashed', linewidth=1.7)], 
        #            ['Real GRB Duration', 'First & Last Trigger Time'], loc='upper right', fontsize=18, prop={'size': 18, 'weight': 'bold'})
        fig.legend([plt.axvspan(-100, -90, facecolor='#ffffff', alpha=0.3)], 
                   ['Input GRB Duration'], loc='upper right', fontsize=18, prop={'size': 18, 'weight': 'bold'})
        if check_min_count == 0:
            fig.suptitle('Lightcurve with Min Time Bin = ' + str(bin_size) + ' s\nGRB: Theta ~ ' + '{:.2f}'.format(real_grb_info['GRB theta'][0]) + '°, Phi ~ ' + '{:.2f}'.format(real_grb_info['GRB phi'][0]) + '°, Fluence = ' + '{:.1f} x 10^{:d}'.format(fluence_coefficient, fluence_exponent) + ' erg/cm^2', 
                         fontsize=20, weight='bold', x=0.03, y=0.97, horizontalalignment='left', verticalalignment='top')
            fig.tight_layout()
            fig.savefig('./3.trigger/' + 'min_time_bin_' + str(bin_size) + 's_lightcurve.png', dpi=500)
        else:
            # fig.suptitle('Lightcurve with Trigger Time Bin = ' + str(bin_size) + ' s', fontsize=20, weight='bold', loc='left')
            fig.suptitle('Lightcurve with Time Bin = ' + str(bin_size) + ' s\nGRB: Theta ~ ' + '{:.2f}'.format(real_grb_info['GRB theta'][0]) + '°, Phi ~ ' + '{:.2f}'.format(real_grb_info['GRB phi'][0]) + '°, Fluence = ' + '{:.1f} x 10^{:d}'.format(fluence_coefficient, fluence_exponent) + ' erg/cm^2', 
                         fontsize=20, weight='bold', x=0.03, y=0.97, horizontalalignment='left', verticalalignment='top')
            fig.tight_layout()
            fig.savefig('./3.trigger/' + 'time_bin_' + str(bin_size) + 's_lightcurve.png', dpi=500)
        check_min_count += 1
        
    #####
    # label T50 & T90 on accumulative figure
    ## redefine time range for hole range
    first_trigger_time   = np.min(trigger_info[:, 0])
    last_trigger_time    = np.max(trigger_info[:, 0]) + trigger_info[np.argmax(trigger_info[:, 0]), 1]
    plot_window_front    = first_trigger_time - trigger_plot_backward_time
    plot_window_back     = last_trigger_time + trigger_plot_forward_time
    plot_window_duration = plot_window_back - plot_window_front
    
    ## find most confident case
    min_R_detector = int(trigger_info[np.argmin(trigger_info[:, 3]), 2]) - 1
    
    ## extract useful data
    hist, bin_edges = np.histogram(sensor_data[min_R_detector], bins=np.arange(0, real_total_duration + min_trigger_time_bin, min_trigger_time_bin) , density=False)
    hist_for_FitBKG      = np.concatenate((hist[int(plot_window_front/min_trigger_time_bin): int(first_trigger_time/min_trigger_time_bin)], hist[int(last_trigger_time/min_trigger_time_bin): int(plot_window_back/min_trigger_time_bin)]))
    hist_for_plot_window = hist[int(plot_window_front/min_trigger_time_bin): int(plot_window_back/min_trigger_time_bin)]
    time_for_FitBKG      = np.concatenate((np.arange(plot_window_front, first_trigger_time, min_trigger_time_bin), np.arange(last_trigger_time, plot_window_back, min_trigger_time_bin)))
    time_for_plot_window = np.arange(plot_window_front, plot_window_front + plot_window_duration, min_trigger_time_bin)[:len(hist_for_plot_window)]
    
    # fit bkg & define zero point and total flux
    bkg             = FitBKG(time_for_FitBKG, hist_for_FitBKG, time_for_plot_window)
    hist_src        = hist_for_plot_window - bkg
    hist_src_cumsum = np.cumsum(hist_src)
    zero_point      = np.mean(hist_src_cumsum[:int(trigger_plot_backward_time/min_trigger_time_bin)])
    hist_src_cumsum = hist_src_cumsum - zero_point
    total_flux      = np.mean(hist_src_cumsum[int(len(hist_src_cumsum) - (trigger_plot_forward_time - trigger_plot_forward_gap)/min_trigger_time_bin):])

    ## plot 
    fig = plt.figure()
    plt.step(np.arange(-trigger_plot_backward_time, plot_window_duration, min_trigger_time_bin)[0: len(hist_src_cumsum)], hist_src_cumsum, where='post')
    T25 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.25)))[0][-1]+1) * min_trigger_time_bin + plot_window_front
    T75 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.75)))[0][0] +1) * min_trigger_time_bin + plot_window_front
    T50 = T75 - T25
    T05 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.05)))[0][-1]+1) * min_trigger_time_bin + plot_window_front
    T95 = (np.where(np.diff(np.sign(hist_src_cumsum - total_flux * 0.95)))[0][0] +1) * min_trigger_time_bin + plot_window_front
    T90 = T95 - T05
    
    T05_to_trigger = T05 - first_trigger_time
    T25_to_trigger = T25 - first_trigger_time
    T75_to_trigger = T75 - first_trigger_time
    T95_to_trigger = T95 - first_trigger_time
    
    plt.vlines(x=T05_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='r', linestyles = 'dashed')
    plt.vlines(x=T25_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='b', linestyles = 'dashed')
    plt.vlines(x=T75_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='b', linestyles = 'dashed')
    plt.vlines(x=T95_to_trigger, ymin=0, ymax=np.max(hist_src_cumsum), color='r', linestyles = 'dashed')

    plt.xlabel('Time [s]')
    plt.ylabel('Count [#]')
    fig.suptitle('Accumulative Lightcruve with Min Time Bin = ' + str(min_trigger_time_bin) + ' s & Detector = ' + sensor_name_list[min_R_detector])
    fig.savefig('./3.trigger/'+'accumulative_lightcurve_min_time_bin_' + str(min_trigger_time_bin) + 's_detector_' + sensor_name_list[min_R_detector] + '.png', dpi=500)
    #####
    
    #####
    # save trigger output
    UTC_GRB_trigger_time = UTC_lightcurve_start_time + timedelta(seconds=np.floor(first_trigger_time), microseconds=np.mod(first_trigger_time, 1))
    
    bkg_for_each_sensor = []
    hist_src_for_each_sensor = []
    for i in range(8):
        hist, bin_edges = np.histogram(sensor_data[i], bins=np.arange(0, real_total_duration + min_trigger_time_bin, min_trigger_time_bin) , density=False)
        hist_for_FitBKG      = np.concatenate((hist[int(plot_window_front/min_trigger_time_bin): int(first_trigger_time/min_trigger_time_bin)], hist[int(last_trigger_time/min_trigger_time_bin): int(plot_window_back/min_trigger_time_bin)]))
        hist_for_plot_window = hist[int(plot_window_front/min_trigger_time_bin): int(plot_window_back/min_trigger_time_bin)]
        time_for_FitBKG      = np.concatenate((np.arange(plot_window_front, first_trigger_time, min_trigger_time_bin), np.arange(last_trigger_time, plot_window_back, min_trigger_time_bin)))
        time_for_plot_window = np.arange(plot_window_front, plot_window_front + plot_window_duration, min_trigger_time_bin)[:len(hist_for_plot_window)]

        bkg = FitBKG(time_for_FitBKG, hist_for_FitBKG, time_for_plot_window)
        bkg_for_each_sensor.append(bkg)
        hist_src_for_each_sensor.append(hist_for_plot_window - bkg)
    
    sensor_src_count_list = []
    sensor_bkg_count_list = [] # in T90
    if T90 < 10:
        for i in range(8):
            sensor_src_count_list.append(np.sum(hist_src_for_each_sensor[i][int((trigger_plot_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_plot_backward_time + T95_to_trigger)/min_trigger_time_bin) + 1]))
            sensor_bkg_count_list.append(np.sum(bkg_for_each_sensor[i][int((trigger_plot_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_plot_backward_time + T95_to_trigger)/min_trigger_time_bin) + 1]))
    else:
        for i in range(8):
            sensor_src_count_list.append(np.sum(hist_src_for_each_sensor[i][int((trigger_plot_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_plot_backward_time + T95_to_trigger + 10)/min_trigger_time_bin) + 1]))
            sensor_bkg_count_list.append(np.sum(bkg_for_each_sensor[i][int((trigger_plot_backward_time + T05_to_trigger)/min_trigger_time_bin): int((trigger_plot_backward_time + T95_to_trigger + 10)/min_trigger_time_bin) + 1]))
    
    satellite_attitude = pd.read_csv('./2.input/' + filename_list[2])
    trigger_mid_time       = (T25 + T75)/2
    trigger_mid_time_index = (np.abs(satellite_attitude['time'] - trigger_mid_time)).argmin()
    qx   = satellite_attitude['qx'][trigger_mid_time_index]
    qy   = satellite_attitude['qy'][trigger_mid_time_index]
    qz   = satellite_attitude['qz'][trigger_mid_time_index]
    qw   = satellite_attitude['qw'][trigger_mid_time_index]
    ECIx = satellite_attitude['ECIx'][trigger_mid_time_index]
    ECIy = satellite_attitude['ECIy'][trigger_mid_time_index]
    ECIz = satellite_attitude['ECIz'][trigger_mid_time_index]

    trigger_output = np.array([datetime.strftime(UTC_GRB_trigger_time, '%m_%d_%Y_%H_%M_%S.%f'), min_trigger_time_bin,
                               round(T50,3), round(T90,3), round(T05_to_trigger,3), round(T25_to_trigger,3), round(T75_to_trigger,3), round(T95_to_trigger,3),
                               sensor_src_count_list[0], sensor_src_count_list[1], sensor_src_count_list[2], sensor_src_count_list[3],
                               sensor_src_count_list[4], sensor_src_count_list[5], sensor_src_count_list[6], sensor_src_count_list[7],
                               sensor_bkg_count_list[0], sensor_bkg_count_list[1], sensor_bkg_count_list[2], sensor_bkg_count_list[3], 
                               sensor_bkg_count_list[4], sensor_bkg_count_list[5], sensor_bkg_count_list[6], sensor_bkg_count_list[7], 
                               qw, qx, qy, qz, ECIx, ECIy, ECIz])
    trigger_output_header = ['Trigger Time UTC','Min Trigger Time Bin','T50','T90','T05 to Trigger','T25 to Trigger','T75 to Trigger','T95 to Trigger',
                             'NN SRC Count','NP SRC Count','NT SRC Count','NB SRC Count','PN SRC Count','PP SRC Count','PT SRC Count','PB SRC Count',
                             'NN BKG Count','NP BKG Count','NT BKG Count','NB BKG Count','PN BKG Count','PP BKG Count','PT BKG Count','PB BKG Count',
                             'qw','qx','qy','qz','ECIx','ECIy','ECIz']
    pd.DataFrame(trigger_output.reshape(-1, len(trigger_output))).to_csv('./3.trigger/' + 'trigger_output.csv', index=False, header=trigger_output_header)
    #####
#====================