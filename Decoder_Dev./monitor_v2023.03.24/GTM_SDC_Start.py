#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:03:15 2022

@author: jasonpbu
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory

from GTM_SDC_Contral import MainWindow_controller

print("Usable Style:",QStyleFactory.keys())

if __name__ == '__main__':
    import sys
    QtWidgets.QApplication.setStyle('Fusion')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())