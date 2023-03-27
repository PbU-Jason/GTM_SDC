#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 13:41:06 2022

@author: jasonpbu
"""

### package ###

import time
import numpy as np
import pandas as pd 
#====================

### selection ###
dt = 0.01 # s
file_in = '123352.477.bin'
#====================

### fixed variables ###
file_out = 'fake.bin'
#====================

### function ###
def DecomposeBinFile(File):    
    # read all data
    with open(File, 'rb') as f:
        data = f.read()
        
    i = 0
    flag_head = 0
    data_master_list = []
    data_slave_list = []
    while i < len(data):
        # check header
        if ('0x%02x' % data[i]) == '0x55' and ('0x%02x' % data[i+1]) == '0xaa' and ('0x%02x' % data[i+2]) == '0x02':
            flag_head = 1 # for master
        
        if ('0x%02x' % data[i]) == '0x55' and ('0x%02x' % data[i+1]) == '0xaa' and ('0x%02x' % data[i+2]) == '0x05':
            flag_head = 2 # for slave
        
        # record one packet data
        if flag_head == 1:
            data_master_list.append([data[j] for j in range(i, i+128)])
        elif flag_head == 2:
            data_slave_list.append([data[j] for j in range(i, i+128)])
        else:
            print('error!')
        
        i += 128 # skip recoraded data
    return pd.DataFrame(np.array(data_master_list)), pd.DataFrame(np.array(data_slave_list))

def RecordBinFile(MasterDF, SlaveDF):
    # initialize output file for master & slave
    with open(file_out, 'wb') as f:
        pass
    
    # record data according to dt
    size_list = [MasterDF.shape[0], SlaveDF.shape[0]]
    larger_df = max(size_list)
    larger_case = size_list.index(larger_df)
    smaller_df = min(size_list)
    for i in range(larger_df):
        if i < smaller_df:
            with open(file_out, 'ab') as f:
                f.write(bytes(MasterDF.iloc[i]))
                time.sleep(dt)
                f.write(bytes(SlaveDF.iloc[i]))
                time.sleep(dt)
        else:
            if larger_case == 0:
                with open(file_out, 'ab') as f:
                    f.write(bytes(MasterDF.iloc[i]))
                    time.sleep(dt)
            else:
                with open(file_out, 'ab') as f:
                    f.write(bytes(SlaveDF.iloc[i]))
                    time.sleep(dt)
    return
#====================

### main code ###
df_master, df_salve = DecomposeBinFile(file_in)
RecordBinFile(df_master, df_salve)
#====================
