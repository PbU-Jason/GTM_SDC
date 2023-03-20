#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:44:11 2022

@author: jasonpbu
"""

### package ###
# import sys
# if 'little' == sys.byteorder:
#      print(666)
# else:
#      print(777)
import time
import struct
import numpy as np
import pandas as pd 
#====================

### selection ###
dt = 1 # s
file_in = 'fake.bin'
#====================

### fixed variables ###
csv_out_master = 'master.csv'
csv_out_slave = 'slave.csv'
csv_header_list_part_1 = ['Header', 'GTM ID', 'Packet Counter', 'Data Length (MSB)', 'Data Length', 
                          'UTC Year', 'UTC Day', 'UTC Hour', 'UTC Minute', 'UTC Second', 'UTC Subsecond', 
                          'GTM ID in Lastest PPS Counter', 'Lastest PPS Counter', 'Lastest Fine Time Counter Value Between 2 PPSs', 
                          'Board Temperature#1', 'Board Temperature#2', 
                          'CITIROC1 Temperature#1', 'CITIROC1 Temperature#2', 'CITIROC2 Temperature#1', 'CITIROC2 Temperature#2', 
                          'CITIROC1 Live Time (Busy)', 'CITIROC2 Live Time (Busy)']
csv_header_list_part_2 = ['CITIROC1 Hit Counter#' + str(i) for i in range(32)]
csv_header_list_part_3 = ['CITIROC2 Hit Counter#' + str(i) for i in range(32)]
csv_header_list_part_4 = ['CITIROC1 Trigger Counter', 'CITIROC2 Trigger Counter', 'Counter Period Setting', 'HV DAC1', 'HV DAC2', 
                          'SPW#A Error Count', 'SPW#A Last Recv Byte', 'SPW#B Error Count', 'SPW#B Last Recv Byte', 'SPW#A Status', 'SPW#B Status', 
                          'Recv Checksum of Last CMD', 'Calc Checksum of Last CMD', 'Number of Recv CMDs', 
                          'Bytes 114', 'Bytes 115', 'Bytes 116', 'Bytes 117', 'Bytes 118', 
                          'CITIROC1 Live Time (Buffer+Busy)', 'CITIROC2 Live Time (Buffer+Busy)', 'Checksum', 'Tail']
csv_header_list = [*csv_header_list_part_1, *csv_header_list_part_2, *csv_header_list_part_3, *csv_header_list_part_4]
#====================

### function ###
def WriteCSV(File):
    # create empty csv files for master & slave
    df_master = pd.DataFrame(columns=csv_header_list)
    df_slave = pd.DataFrame(columns=csv_header_list)
    df_master.to_csv(csv_out_master, index=False)
    df_slave.to_csv(csv_out_slave, index=False)

    # decoding & writing
    file_pointer = 0
    idle_counter = 0
    while True:
        with open(File, 'rb') as f:
            f.seek(file_pointer, 1) # move pointer to read new info
            data = f.read()
        file_pointer += len(data) # update the number for pointer to move
        
        if len(data) != 0:
            idle_counter = 0 # refresh idle counter
            
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
                
                # preprocessing
                if bin(struct.unpack('B', bytes([data[i+15]]))[0])[2] == '1':
                    gtm_id_in_pps = 1 # for slave
                else:
                    gtm_id_in_pps = 0 # for master
                
                pps = bytes([struct.unpack('B', bytes([data[i+15]]))[0] & 127]) + bytes([data[i+16]]) # 127 = 0x7f = 0111 1111
                fine_time = b'\x00' + bytes([data[i+17]]) + bytes([data[i+18]]) + bytes([data[i+19]])
                
                citiroc1_livetime_busy = b'\x00' + bytes([data[i+26]]) + bytes([data[i+27]]) + bytes([data[i+28]])
                citiroc2_livetime_busy = b'\x00' + bytes([data[i+29]]) + bytes([data[i+30]]) + bytes([data[i+31]])
                
                citiroc1_livetime_buffer_busy = b'\x00' + bytes([data[i+119]]) + bytes([data[i+120]]) + bytes([data[i+121]])
                citiroc2_livetime_buffer_busy = b'\x00' + bytes([data[i+122]]) + bytes([data[i+123]]) + bytes([data[i+124]])
                
                # decode
                data_decoded_part_1 = ['%02X%02X' % (data[i], data[i+1]),                              # head
                                       struct.unpack('B', bytes([data[i+2]]))[0],                      # gtm id
                                       struct.unpack('>H', bytes([data[i+3]])+bytes([data[i+4]]))[0],  # packet counter
                                       struct.unpack('B', bytes([data[i+5]]))[0],                      # data length msb
                                       struct.unpack('B', bytes([data[i+6]]))[0],                      # data length
                                       struct.unpack('>H', bytes([data[i+7]])+bytes([data[i+8]]))[0],  # utc year
                                       struct.unpack('>H', bytes([data[i+9]])+bytes([data[i+10]]))[0], # utc day
                                       struct.unpack('B', bytes([data[i+11]]))[0],                     # utc hour
                                       struct.unpack('B', bytes([data[i+12]]))[0],                     # utc minute
                                       struct.unpack('B', bytes([data[i+13]]))[0],                     # utc second
                                       struct.unpack('B', bytes([data[i+14]]))[0],                     # utc subsecond
                                       gtm_id_in_pps,                                                  # gtm id in pps
                                       struct.unpack('>H', pps)[0],                                    # pps counter
                                       struct.unpack('>I', fine_time)[0],                              # fine time
                                       struct.unpack('b', bytes([data[i+20]]))[0],                     # board temp 1
                                       struct.unpack('b', bytes([data[i+21]]))[0],                     # board temp 1
                                       struct.unpack('b', bytes([data[i+22]]))[0],                     # citiroc1 temp 1
                                       struct.unpack('b', bytes([data[i+23]]))[0],                     # citiroc1 temp 2
                                       struct.unpack('b', bytes([data[i+24]]))[0],                     # citiroc2 temp 1
                                       struct.unpack('b', bytes([data[i+25]]))[0],                     # citiroc2 temp 2
                                       struct.unpack('>I', citiroc1_livetime_busy)[0],                 # citiroc1 livetime (busy)
                                       struct.unpack('>I', citiroc2_livetime_busy)[0],                 # citiroc1 livetime (busy)
                                       ]
                data_decoded_part_2 = [struct.unpack('B', bytes([data[i+j]]))[0] for j in range(32, 32+32)]
                data_decoded_part_3 = [struct.unpack('B', bytes([data[i+j]]))[0] for j in range(64, 64+32)]
                data_decoded_part_4 = [struct.unpack('>H', bytes([data[i+96]])+bytes([data[i+97]]))[0],  # citiroc1 trigger
                                       struct.unpack('>H', bytes([data[i+98]])+bytes([data[i+99]]))[0],  # citiroc2 trigger
                                       struct.unpack('B', bytes([data[i+100]]))[0],                      # counter period
                                       struct.unpack('B', bytes([data[i+101]]))[0],                      # hv dac 1
                                       struct.unpack('B', bytes([data[i+102]]))[0],                      # hv dac 2
                                       '%02X' % (data[i+103]),                                           # spw a error_count
                                       '%02X' % (data[i+104]),                                           # spw a last_receive
                                       '%02X' % (data[i+105]),                                           # spw b error_count
                                       '%02X' % (data[i+106]),                                           # spw_b last_receive
                                       '%02X%02X' % (data[i+107], data[i+108]),                          # spw a status
                                       '%02X%02X' % (data[i+109], data[i+110]),                          # spw b status
                                       struct.unpack('B', bytes([data[i+111]]))[0],                      # recv checksum
                                       struct.unpack('B', bytes([data[i+112]]))[0],                      # calc checksum
                                       struct.unpack('B', bytes([data[i+113]]))[0],                      # number of recv
                                       struct.unpack('B', bytes([data[i+114]]))[0],                      # byte 114
                                       struct.unpack('B', bytes([data[i+115]]))[0],                      # byte 115
                                       struct.unpack('B', bytes([data[i+116]]))[0],                      # byte 116
                                       struct.unpack('B', bytes([data[i+117]]))[0],                      # byte 117
                                       struct.unpack('B', bytes([data[i+118]]))[0],                      # byte 118
                                       struct.unpack('>I', citiroc1_livetime_buffer_busy)[0],            # citiroc1 livetime (buffer busy)
                                       struct.unpack('>I', citiroc2_livetime_buffer_busy)[0],            # citiroc2 livetime (buffer busy)
                                       struct.unpack('B', bytes([data[i+125]]))[0],                      # recv checksum
                                       '%02X%02X' % (data[i+126], data[i+127]),                          # tail
                                       ]
                data_decoded = [*data_decoded_part_1, *data_decoded_part_2, *data_decoded_part_3, *data_decoded_part_4]
                
                # record one packet data
                if flag_head == 1:
                    data_master_list.append(data_decoded)
                elif flag_head == 2:
                    data_slave_list.append(data_decoded)
                else:
                    print('error!')
                
                i += 128 # skip recoraded data

            # append new data to csv files
            df_master_temp = pd.DataFrame(np.array(data_master_list))
            df_master_temp.to_csv(csv_out_master, mode='a', index=False, header=False)
            df_slave_temp = pd.DataFrame(np.array(data_slave_list))
            df_slave_temp.to_csv(csv_out_slave, mode='a', index=False, header=False)
        else:
            idle_counter += 1
            if idle_counter == 5:
                break
        
        time.sleep(dt)
    return
#====================

### main code ###s
WriteCSV(file_in)
#====================