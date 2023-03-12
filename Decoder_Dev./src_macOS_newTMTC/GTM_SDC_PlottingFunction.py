#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:47:55 2022

@author: jasonpbu
"""

import re
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=16, height=9, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)
        self.axesList = []
        for i in range(1, 16+1, 1):
            self.axesList.append(fig.add_subplot(4, 4, i))
        super(MplCanvas, self).__init__(fig)

### function ###
def Loader(Filename, Dictionary, HitSelection):
    with open(Filename) as file:
        line = file.readline()
        while line:
            if HitSelection == 1:
                # if hit, [pps count], [fine count], [gtm module], [citiroc id], [channel id], [gain] & [adc value]
                regex = re.compile(r'event adc:\s{0,}1;\s{0,}(\d+);\s{0,}(\d+);\s{0,}(\d);\s{0,}(\d);\s{0,}(\d{1,2});\s{0,}(\d);\s{0,}(-?\d+)')
            elif HitSelection == 2:
                regex = re.compile(r'event adc:\s{0,}0;\s{0,}(\d+);\s{0,}(\d+);\s{0,}(\d);\s{0,}(\d);\s{0,}(\d{1,2});\s{0,}(\d);\s{0,}(-?\d+)')
            else:
                print("unknow hit selection!")
            match = regex.search(line)
            if match:
                Dictionary['PPS'].append(int(match.group(1)))
                Dictionary['Finetime'].append(int(match.group(2)))
                Dictionary['GTM_Module'].append(int(match.group(3)))
                Dictionary['Citiroc_ID'].append(int(match.group(4)))
                Dictionary['Channel_ID'].append(int(match.group(5)))
                Dictionary['Gain'].append(int(match.group(6)))
                Dictionary['ADC'].append(int(match.group(7)))
            line = file.readline()
    return
#====================


