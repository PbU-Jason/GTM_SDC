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
        # for i in range(1, 16+1, 1):
        #     self.axesList.append(fig.add_subplot(4, 4, i))
        for i in range(1, 2+1, 1):
            self.axesList.append(fig.add_subplot(1, 2, i))
        super(MplCanvas, self).__init__(fig)

### function ###
def Loader(Filename):
    df = pd.read_csv(Filename, sep=';')
    return df
#====================


