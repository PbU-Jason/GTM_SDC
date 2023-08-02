#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:03:15 2022

@author: jasonpbu
"""

# Ref: https://www.wongwonggoods.com/all-posts/python/pyqt5/pyqt5-5/

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory

from GTM_SDC_UI_Contraller import MainWindowController

if __name__ == '__main__':

    # Check usable style and assign 'Fusion'
    print("Usable Style:", QStyleFactory.keys())
    QtWidgets.QApplication.setStyle('Fusion')

    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindowController()
    window.show()

    # Above 2 lines == Below 4 lines

    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()

    sys.exit(app.exec_())