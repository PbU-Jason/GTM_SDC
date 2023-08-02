#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:45:06 2022

@author: jasonpbu
"""

import platform
from ctypes import *

def c_decoder(file_name, in_space_flag, decode_mode, export_mode, initail_file_pointer):
    
    # Check system
    if platform.system() == 'Darwin': # MacOS
        so_file = "./GTM_Decoder_Main.dylib"
    elif platform.system() == 'Linux': # Linux
        so_file = "./GTM_Decoder_Main.so"
    elif platform.system() == 'Windows': # Windows
        so_file = "./GTM_Decoder_Main.dll"
    else:
        print('Please check OS!')
    
    # Create c dynamic-link library (CDLL) based on system
    c_function = CDLL(so_file)

    # Assign return type
    c_function.decoder.restype = c_int

    # Run decoder in c
    new_file_pointer = c_function.decoder(
        c_char_p(bytes(file_name, 'utf-8')),
        c_int(in_space_flag),
        c_int(decode_mode),
        c_int(export_mode),
        c_int(initail_file_pointer)
    )
    
    return new_file_pointer