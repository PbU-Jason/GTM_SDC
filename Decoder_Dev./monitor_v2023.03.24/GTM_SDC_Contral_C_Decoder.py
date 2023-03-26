#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:45:06 2022

@author: jasonpbu
"""

import platform
from ctypes import *

def C_Decoder(FileName, DecodeMode, ExtractOnOff, ExportMode, InitailFilePointer):
    if platform.system() == 'Darwin': # MacOS
        so_file = "./GTM_Decoder_Main.dylib"
    elif platform.system() == 'Linux': # Linux
        so_file = "./GTM_Decoder_Main.so"
    elif platform.system() == 'Windows': # Windows
        so_file = "./GTM_Decoder_Main.dll"
    else:
        print('please check OS!')
    c_function = CDLL(so_file)
    
    c_int(new_file_pointer) = c_function.decoder(c_char_p(bytes(FileName, 'utf-8')), 
                                                 c_int(DecodeMode),
                                                 c_int(ExtractOnOff), 
                                                 c_int(ExportMode),
                                                 c_int(InitailFilePointer)
                                                 )
    
    return new_file_pointer