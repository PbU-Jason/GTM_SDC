#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 00:05:29 2022

@author: jasonpbu
"""

import re

setPointSize = re.compile(r"setPointSize")

### define file path ###

input_file_path = 'GTM_SDC_UI_temp.py'
output_file_path = 'GTM_SDC_UI.py'

### read and write file ###

with open(output_file_path, 'w') as f_out:
    with open(input_file_path, 'r') as f_in:
        
        line_in = f_in.readline()
        while line_in:
        
            if re.search(setPointSize, line_in):
                f_out.write(line_in.replace('setPointSize', 'setPixelSize'))
            else:
                f_out.write(line_in)
    
            line_in = f_in.readline()
            