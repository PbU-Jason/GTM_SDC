#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 21:09:48 2023

@author: jasonpbu
"""

### package ###
import numpy as np
import pandas as pd 
#====================

### function ###
def all_grb_statistic():
    key_list = []
    grb_name_list = []
    grb_ra_list = []
    grb_dec_list = []
    grb_time_list = []
    with open('BrowseTargets-16746-1695890594.txt') as f:
        
        while True:
            line = f.readline()
            if not line:
                break
            
            if line[0] == '|':
                
                if line[1] != 'G':
                    for line_temp in line.split('|'):
                        if (line_temp.isspace()) or (len(line_temp) == 0):
                            pass
                        else:
                            key_list.append(line_temp.strip())
                else:
                    grb_temp = line.split('|')
                    grb = list(filter(None, grb_temp))
                    grb_name_list.append(grb[0])
                    grb_ra_temp = grb[1].split()
                    grb_ra = (float(grb_ra_temp[0]) + float(grb_ra_temp[1])/60 + float(grb_ra_temp[2])/3600) * (360/24)   
                    grb_ra_list.append(grb_ra)
                    grb_dec_temp = grb[2].split()
                    if float(grb_dec_temp[0]) >= 0:
                        grb_dec = float(grb_dec_temp[0]) + float(grb_dec_temp[1])/60 + float(grb_dec_temp[2])/3600
                    else:
                        grb_dec = float(grb_dec_temp[0]) - float(grb_dec_temp[1])/60 - float(grb_dec_temp[2])/3600
                    grb_dec_list.append(grb_dec)
                    grb_date = grb[3][:10]
                    grb_time_list.append(grb_date)
                
    grb_dict = {
        key_list[0]: grb_name_list,
        key_list[1]: grb_ra_list,
        key_list[2]: grb_dec_list,
        key_list[3]: grb_time_list,
    }
    
    df_grb = pd.DataFrame(grb_dict)
    
    df_grb_date = df_grb.groupby(['trigger_time'])['trigger_time'].count().to_frame('Count').reset_index()

    # Prepare all date range based on pd's datetime
    all_date_idx = pd.date_range(df_grb_date.trigger_time.head(1).item(), 
                        df_grb_date.trigger_time.tail(1).item())

    # Change old index into pd's datetime
    df_grb_date.index = pd.DatetimeIndex(df_grb_date.trigger_time)

    # Create a new df comparing all date range and old index
    df_grb_all_date = df_grb_date.reindex(all_date_idx, fill_value=0)

    return df_grb, df_grb_all_date
#====================
