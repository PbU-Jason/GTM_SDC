#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:22:20 2024

@author: jasonpbu
"""

import os
import numpy as np

from gui.GTM_SDC_UI_Controller_Decoder_Thread_C import c_decoder

for sub_folder in os.listdir('../pickup'):
    if os.path.isdir(f'../pickup/{sub_folder}/'):
        for file in os.listdir(f'../pickup/{sub_folder}/'):
            if file.endswith('.bin'):
                print(f'../pickup/{sub_folder}/{file}')
                _ = c_decoder(f'../pickup/{sub_folder}/{file}',
                              in_space_flag=2, 
                              decode_mode=2, 
                              export_mode=3, 
                              initail_file_pointer=0)
