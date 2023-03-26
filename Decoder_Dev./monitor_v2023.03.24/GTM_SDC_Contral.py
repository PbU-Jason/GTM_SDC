#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

import re
import time
import numpy as np
import pandas as pd

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2

from GTM_SDC_UI import Ui_MainWindow
from GTM_SDC_Contral_C_Decoder import C_Decoder
from GTM_SDC_PlottingWindow import Ui_PlottingWindow
from GTM_SDC_PlottingFunction import MplCanvas, Loader

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        ### GTM icon ###
        self.img_path = 'GTM_icon.png'
        self.display_img()
        
        ### Decoder ###
        self.ui.Decoder_Button.clicked.connect(self.ButtonClicked_Decoder)
        self.Clicked_Counter_Decoder = 0
        
        # Decoder On or Off
        self.Decoder_OnOff()
        
        # Decoder Input File
        self.ui.InputFile_Decoder_Button.clicked.connect(self.Decoder_Open_File)
        self.Input_Decoder_Filename = []
        self.Input_Decoder_Filetype = ""
        
        # Decode Modes
        self.ui.Decode_Modes_CheckBox_Sci.clicked.connect(self.Sci_CheckBoxClick)
        self.ui.Decode_Modes_CheckBox_TMTC.clicked.connect(self.TMTC_CheckBoxClick)
        self.Decode_Modes = 0
        
        # Extract Selection for Sci Export Modes
        self.ui.Extract_NSPO_CheckBox.clicked.connect(self.Extract_CheckBoxClick)
        self.Extract_Selection = 0
        
        # Sci Export Modes
        self.ui.Export_Modes_CheckBox_Sci_Raw.clicked.connect(self.Sci_Raw_CheckBoxClick)
        self.ui.Export_Modes_CheckBox_Sci_Pipeline.clicked.connect(self.Sci_Pipeline_CheckBoxClick)
        self.ui.Export_Modes_CheckBox_Sci_Both.clicked.connect(self.Sci_Both_CheckBoxClick)
        self.Export_Modes = 0
        
        # Hit Selection for Sci Export Modes
        self.ui.Hit_Selection_CheckBox_Hit.clicked.connect(self.Hit_CheckBoxClick)
        self.ui.Hit_Selection_CheckBox_NoHit.clicked.connect(self.NoHit_CheckBoxClick)
        self.Hit_Selection = 0
        
        # Start Decoding
        self.ui.Start_Button.clicked.connect(self.ButtonClicked_Start)
        
        ### Calibrator ###
        self.ui.Calibrator_Button.clicked.connect(self.ButtonClicked_Calibrator)
        self.Clicked_Counter_Calibrator = 0

        # Calibrator On or Off
        self.Calibrator_OnOff()

        # Calibrator Input File
        self.ui.InputFile_Calibrator_Button.clicked.connect(self.Calibrator_Open_File)
        self.Input_Calibrator_Filename = []
        self.Input_Calibrator_Filetype = ""

        # Visualization Modes
        self.ui.Visualization_RadioButton_Counts_ADC.clicked.connect(self.Counts_ADC_RadioButtonClick)
        self.ui.Visualization_RadioButton_Counts_ADC_fitting.clicked.connect(self.Counts_ADC_fitting_RadioButtonClick)

        # Module and Sensor Selection
        self.ui.Calibrator_GroupBox_Master.clicked.connect(self.Plot_OnOff)
        self.ui.Calibrator_GroupBox_Slave.clicked.connect(self.Plot_OnOff)

        self.ui.Master_CheckBox_Sensor1.clicked.connect(self.Plot_OnOff)
        self.ui.Master_CheckBox_Sensor2.clicked.connect(self.Plot_OnOff)
        self.ui.Master_CheckBox_Sensor3.clicked.connect(self.Plot_OnOff)
        self.ui.Master_CheckBox_Sensor4.clicked.connect(self.Plot_OnOff)

        self.ui.Slave_CheckBox_Sensor1.clicked.connect(self.Plot_OnOff)
        self.ui.Slave_CheckBox_Sensor2.clicked.connect(self.Plot_OnOff)
        self.ui.Slave_CheckBox_Sensor3.clicked.connect(self.Plot_OnOff)
        self.ui.Slave_CheckBox_Sensor4.clicked.connect(self.Plot_OnOff)

        # Start Plotting
        self.ui.Plot_Button.clicked.connect(self.ButtonClicked_Plot)

        # Define Plotting Variables
        self.low_gain  = 4
        self.high_gain = 40
        self.dic = {'PPS'       : [],
                    'Finetime'  : [],
                    'GTM_Module': [],
                    'Citiroc_ID': [],
                    'Channel_ID': [],
                    'Gain'      : [],
                    'ADC'       : []}
        
    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.qpixmap_height = self.qpixmap.height()
        self.qpixmap_height -= 210
        scaled_pixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)
        self.ui.GTM_ICON.setPixmap(scaled_pixmap)
    
    def ButtonClicked_Decoder(self):
        self.Clicked_Counter_Decoder += 1
        if (self.Clicked_Counter_Decoder%2) != 0:
            self.ui.Decoder_Button.setStyleSheet("background-color: #2B5DD1;"
                                                 "color: #FFFFFF;"
                                                 "border-style: outset;"
                                                 "padding: 2px;"
                                                 "font: bold 20px;"
                                                 "border-width: 3px;"
                                                 "border-radius: 10px;"
                                                 "border-color: #2752B8;")
            self.ui.Decoder_Button_Status.setText("Decoder Selected!")
        else:
            self.ui.Decoder_Button.setStyleSheet("")
            self.ui.Decoder_Button_Status.setText("     ")
        self.Decoder_OnOff()
        
    def Decoder_OnOff(self):
        if (self.Clicked_Counter_Decoder%2) != 0:
            self.ui.InputFile_Decoder_Button.setEnabled(True)
            self.ui.InputFile_Decoder_Text.setEnabled(True)
            
            self.ui.Decode_Modes_Text.setEnabled(True)
            self.ui.Decode_Modes_CheckBox_Sci.setEnabled(True)
            self.ui.Extract_NSPO_CheckBox.setEnabled(True)
            self.ui.Decode_Modes_CheckBox_TMTC.setEnabled(True)
            
            self.Sci_OnOff()
            self.Start_OnOff()
        else:
            self.ui.InputFile_Decoder_Button.setEnabled(False)
            self.ui.InputFile_Decoder_Text.setEnabled(False)
            
            self.ui.Decode_Modes_Text.setEnabled(False)
            self.ui.Decode_Modes_CheckBox_Sci.setEnabled(False)
            self.ui.Extract_NSPO_CheckBox.setEnabled(False)
            self.ui.Decode_Modes_CheckBox_TMTC.setEnabled(False)
            
            self.ui.Export_Modes_CheckBox_Sci_Raw.setEnabled(False)
            self.ui.Export_Modes_CheckBox_Sci_Pipeline.setEnabled(False)
            self.ui.Export_Modes_CheckBox_Sci_Both.setEnabled(False)
            
            self.ui.Hit_Selection_Text.setEnabled(False)
            self.ui.Hit_Selection_CheckBox_Hit.setEnabled(False)
            self.ui.Hit_Selection_CheckBox_NoHit.setEnabled(False)
            
            self.ui.Start_Button.setEnabled(False)
            self.ui.Start_progressBar.setEnabled(False)
            self.ui.Start_Status.setEnabled(False)
    
    def Decoder_Open_File(self):
        self.Input_Decoder_Filename, self.Input_Decoder_Filetype = QFileDialog.getOpenFileNames(self, "Open file", "./")

        if len(self.Input_Decoder_Filename) == 1:
            self.ui.InputFile_Decoder_Text.setText(self.Input_Decoder_Filename[0])
        
        if len(self.Input_Decoder_Filename) > 1:
            Input_Decoder_Filename_print = ""
            for Input_Decoder_Filename_print_temp in self.Input_Decoder_Filename:
                Input_Decoder_Filename_print += Input_Decoder_Filename_print_temp + ";"
            self.ui.InputFile_Decoder_Text.setText(Input_Decoder_Filename_print)

        self.Start_OnOff()
    
    def Sci_CheckBoxClick(self):
        if self.ui.Decode_Modes_CheckBox_Sci.isChecked():
            self.ui.Decode_Modes_CheckBox_TMTC.setChecked(False)
            self.Decode_Modes = 1
        else:
            self.Decode_Modes = 0
        self.Sci_OnOff()
        self.Start_OnOff()
        
    def TMTC_CheckBoxClick(self):
        if self.ui.Decode_Modes_CheckBox_TMTC.isChecked():
            self.ui.Decode_Modes_CheckBox_Sci.setChecked(False)
            self.Decode_Modes = 2
        else:
            self.Decode_Modes = 0
        self.Sci_OnOff()
        self.Start_OnOff()
        
    def Sci_OnOff(self):
        if self.ui.Decode_Modes_CheckBox_Sci.isChecked():
            self.ui.Extract_NSPO_CheckBox.setEnabled(True)
            
            self.ui.Export_Modes_CheckBox_Sci_Raw.setEnabled(True)
            self.ui.Export_Modes_CheckBox_Sci_Pipeline.setEnabled(True)
            self.ui.Export_Modes_CheckBox_Sci_Both.setEnabled(True)
            
            self.ui.Hit_Selection_Text.setEnabled(True)
            self.ui.Hit_Selection_CheckBox_Hit.setEnabled(True)
            self.ui.Hit_Selection_CheckBox_NoHit.setEnabled(True)
        else:
            self.ui.Extract_NSPO_CheckBox.setEnabled(False)
            
            self.ui.Export_Modes_CheckBox_Sci_Raw.setEnabled(False)
            self.ui.Export_Modes_CheckBox_Sci_Pipeline.setEnabled(False)
            self.ui.Export_Modes_CheckBox_Sci_Both.setEnabled(False)
            
            self.ui.Hit_Selection_Text.setEnabled(False)
            self.ui.Hit_Selection_CheckBox_Hit.setEnabled(False)
            self.ui.Hit_Selection_CheckBox_NoHit.setEnabled(False)
        
    def Extract_CheckBoxClick(self):
        if self.ui.Extract_NSPO_CheckBox.isChecked():
            self.Extract_Selection = 1
        else:
            self.Extract_Selection = 0
        self.Start_OnOff()
    
    def Sci_Raw_CheckBoxClick(self):
        if self.ui.Export_Modes_CheckBox_Sci_Raw.isChecked():
            self.ui.Export_Modes_CheckBox_Sci_Pipeline.setChecked(False)
            self.ui.Export_Modes_CheckBox_Sci_Both.setChecked(False)
            self.Export_Modes = 1
        else:
            self.Export_Modes = 0
        self.Start_OnOff()
    
    def Sci_Pipeline_CheckBoxClick(self):
        if self.ui.Export_Modes_CheckBox_Sci_Pipeline.isChecked():
            self.ui.Export_Modes_CheckBox_Sci_Raw.setChecked(False)
            self.ui.Export_Modes_CheckBox_Sci_Both.setChecked(False)
            self.Export_Modes = 2
        else:
            self.Export_Modes = 0
        self.Start_OnOff()
    
    def Sci_Both_CheckBoxClick(self):
        if self.ui.Export_Modes_CheckBox_Sci_Both.isChecked():
            self.ui.Export_Modes_CheckBox_Sci_Raw.setChecked(False)
            self.ui.Export_Modes_CheckBox_Sci_Pipeline.setChecked(False)
            self.Export_Modes = 3
        else:
            self.Export_Modes = 0
        self.Start_OnOff()
        
    def Hit_CheckBoxClick(self):
        if self.ui.Hit_Selection_CheckBox_Hit.isChecked():
            self.ui.Hit_Selection_CheckBox_NoHit.setChecked(False)
            self.Hit_Selection = 1
        else:
            self.Hit_Selection = 0
        self.Start_OnOff()
    
    def NoHit_CheckBoxClick(self):
        if self.ui.Hit_Selection_CheckBox_NoHit.isChecked():
            self.ui.Hit_Selection_CheckBox_Hit.setChecked(False)
            self.Hit_Selection = 2
        else:
            self.Hit_Selection = 0
        self.Start_OnOff()
    
    def Start_OnOff(self):
        if self.Input_Decoder_Filename != []:
            if self.ui.Decode_Modes_CheckBox_TMTC.isChecked():
                self.ui.Start_Button.setEnabled(True)
                self.ui.Start_progressBar.setEnabled(True)
                self.ui.Start_Status.setEnabled(True)
            elif self.ui.Decode_Modes_CheckBox_Sci.isChecked():
                if self.ui.Export_Modes_CheckBox_Sci_Raw.isChecked():
                    if self.ui.Hit_Selection_CheckBox_Hit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    elif self.ui.Hit_Selection_CheckBox_NoHit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    else:
                        self.ui.Start_Button.setEnabled(False)
                        self.ui.Start_progressBar.setEnabled(False)
                        self.ui.Start_Status.setEnabled(False)
                elif self.ui.Export_Modes_CheckBox_Sci_Pipeline.isChecked():
                    if self.ui.Hit_Selection_CheckBox_Hit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    elif self.ui.Hit_Selection_CheckBox_NoHit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    else:
                        self.ui.Start_Button.setEnabled(False)
                        self.ui.Start_progressBar.setEnabled(False)
                        self.ui.Start_Status.setEnabled(False)
                elif self.ui.Export_Modes_CheckBox_Sci_Both.isChecked():
                    if self.ui.Hit_Selection_CheckBox_Hit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    elif self.ui.Hit_Selection_CheckBox_NoHit.isChecked():
                        self.ui.Start_Button.setEnabled(True)
                        self.ui.Start_progressBar.setEnabled(True)
                        self.ui.Start_Status.setEnabled(True)
                    else:
                        self.ui.Start_Button.setEnabled(False)
                        self.ui.Start_progressBar.setEnabled(False)
                        self.ui.Start_Status.setEnabled(False)
                else:
                    self.ui.Start_Button.setEnabled(False)
                    self.ui.Start_progressBar.setEnabled(False)
                    self.ui.Start_Status.setEnabled(False)
            else:
                self.ui.Start_Button.setEnabled(False)
                self.ui.Start_progressBar.setEnabled(False)
                self.ui.Start_Status.setEnabled(False)
        else:
            self.ui.Start_Button.setEnabled(False)
            self.ui.Start_progressBar.setEnabled(False)
            self.ui.Start_Status.setEnabled(False)
            
    
    def ButtonClicked_Start(self):
        print("Decoding!")

        # for pure TMTC and SD decoding (only need one file pointer)
        if ((self.Decode_Modes == 1) and (self.Extract_Selection == 0)) or (self.Decode_Modes == 2):
            for Input_Decoder_Filename in self.Input_Decoder_Filename:
                new_file_pointer = C_Decoder(Input_Decoder_Filename, self.Decode_Modes, self.Extract_Selection, self.Export_Modes, InitailFilePointer=0) 
                print(new_file_pointer)
                new_file_pointer_cache = new_file_pointer

                time.sleep(1)

                continue_decode = True
                while continue_decode:
                    new_file_pointer = C_Decoder(Input_Decoder_Filename, self.Decode_Modes, self.Extract_Selection, self.Export_Modes, InitailFilePointer=new_file_pointer_cache) 
                    print(new_file_pointer)

                    if new_file_pointer == new_file_pointer_cache:
                        break
                    else:
                        new_file_pointer_cache = new_file_pointer
                        time.sleep(10)
        
        # for SD (with header and tail) decoding ( need two file pointers)
        if (self.Decode_Modes == 1) and (self.Extract_Selection == 1):
            for Input_Decoder_Filename in self.Input_Decoder_Filename:
                new_file_pointer_extract = C_Decoder(Input_Decoder_Filename, self.Decode_Modes, self.Extract_Selection, self.Export_Modes, InitailFilePointer=0) 
                print(new_file_pointer_extract)
                new_file_pointer_extract_cache = new_file_pointer_extract

                Input_Decoder_Filename_extracted = Input_Decoder_Filename.replace('.bin','_extracted.bin')
                new_file_pointer_decode = C_Decoder(Input_Decoder_Filename_extracted, self.Decode_Modes, 0, self.Export_Modes, InitailFilePointer=0) 
                print(new_file_pointer_decode)
                new_file_pointer_decode_cache = new_file_pointer_decode

                time.sleep(1)


                continue_decode = True
                while continue_decode:
                    new_file_pointer_extract = C_Decoder(Input_Decoder_Filename, self.Decode_Modes, self.Extract_Selection, self.Export_Modes, InitailFilePointer=new_file_pointer_extract_cache) 
                    print(new_file_pointer_extract)
                    new_file_pointer_decode = C_Decoder(Input_Decoder_Filename_extracted, self.Decode_Modes, 0, self.Export_Modes, InitailFilePointer=new_file_pointer_decode_cache) 
                    print(new_file_pointer_decode)

                    if (new_file_pointer_extract == new_file_pointer_extract_cache) and (new_file_pointer_decode == new_file_pointer_decode_cache):
                        break
                    else:
                        new_file_pointer_extract_cache = new_file_pointer_extract
                        new_file_pointer_decode_cache = new_file_pointer_decode
                        time.sleep(10)

    def ButtonClicked_Calibrator(self):
        self.Clicked_Counter_Calibrator += 1
        if (self.Clicked_Counter_Calibrator%2) != 0:
            self.ui.Calibrator_Button.setStyleSheet("background-color: #2B5DD1;"
                                                  "color: #FFFFFF;"
                                                  "border-style: outset;"
                                                  "padding: 2px;"
                                                  "font: bold 20px;"
                                                  "border-width: 3px;"
                                                  "border-radius: 10px;"
                                                  "border-color: #2752B8;")
            self.ui.Calibrator_Button_Status.setText("Calibrator Selected!")
        else:
            self.ui.Calibrator_Button.setStyleSheet("")
            self.ui.Calibrator_Button_Status.setText("     ")
        self.Calibrator_OnOff()
        
    def Calibrator_OnOff(self):
        if (self.Clicked_Counter_Calibrator%2) != 0:
            self.ui.InputFile_Calibrator_Button.setEnabled(True)
            self.ui.InputFile_Calibrator_Text.setEnabled(True)
            
            self.ui.Calibrator_GroupBox_Visualization.setEnabled(True)

            self.Visualization_OnOff()
        else:
            self.ui.InputFile_Calibrator_Button.setEnabled(False)
            self.ui.InputFile_Calibrator_Text.setEnabled(False)
            
            self.ui.Calibrator_GroupBox_Visualization.setEnabled(False)
            self.ui.Calibrator_GroupBox_Module_Sensor.setEnabled(False)
            self.ui.Calibrator_GroupBox_PlottingSetup.setEnabled(False)
            self.ui.Calibrator_GroupBox_FittingSetup.setEnabled(False)

            self.ui.Plotting_Widget.setEnabled(False)
    
    def Calibrator_Open_File(self):
        self.Input_Calibrator_Filename, self.Input_Calibrator_Filetype = QFileDialog.getOpenFileNames(self, "Open file", "./")

        if len(self.Input_Calibrator_Filename) == 1:
            self.ui.InputFile_Calibrator_Text.setText(self.Input_Calibrator_Filename[0])
        
        if len(self.Input_Calibrator_Filename) > 1:
            Input_Calibrator_Filename_print = ""
            for Input_Calibrator_Filename_print_temp in self.Input_Calibrator_Filename:
                Input_Calibrator_Filename_print += Input_Calibrator_Filename_print_temp + ";"
            self.ui.InputFile_Calibrator_Text.setText(Input_Calibrator_Filename_print)

        self.Plot_OnOff()
     
    def Counts_ADC_RadioButtonClick(self):
        self.ui.Calibrator_GroupBox_Module_Sensor.setEnabled(True)
        self.ui.Calibrator_GroupBox_PlottingSetup.setEnabled(True)
        self.ui.Calibrator_GroupBox_FittingSetup.setEnabled(False)

        self.Plot_OnOff()
    
    def Counts_ADC_fitting_RadioButtonClick(self):
        self.ui.Calibrator_GroupBox_Module_Sensor.setEnabled(True)
        self.ui.Calibrator_GroupBox_PlottingSetup.setEnabled(True)
        self.ui.Calibrator_GroupBox_FittingSetup.setEnabled(True)

        self.Plot_OnOff()

    def Visualization_OnOff(self):
        if self.ui.Visualization_RadioButton_Counts_ADC.isChecked():
            self.Counts_ADC_RadioButtonClick()
        if self.ui.Visualization_RadioButton_Counts_ADC_fitting.isChecked():
            self.Counts_ADC_fitting_RadioButtonClick()
    
    def Plot_OnOff(self):
        if self.Input_Calibrator_Filename != []:
            if self.ui.Visualization_RadioButton_Counts_ADC.isChecked() or self.ui.Visualization_RadioButton_Counts_ADC_fitting.isChecked():
                if self.ui.Calibrator_GroupBox_Master.isChecked():
                    if self.ui.Master_CheckBox_Sensor1.isChecked() or self.ui.Master_CheckBox_Sensor2.isChecked() or self.ui.Master_CheckBox_Sensor3.isChecked() or self.ui.Master_CheckBox_Sensor4.isChecked():
                        self.ui.Plotting_Widget.setEnabled(True)
                    else:
                        self.ui.Plotting_Widget.setEnabled(False)
                elif self.ui.Calibrator_GroupBox_Slave.isChecked():
                    if self.ui.Slave_CheckBox_Sensor1.isChecked() or self.ui.Slave_CheckBox_Sensor2.isChecked() or self.ui.Slave_CheckBox_Sensor3.isChecked() or self.ui.Slave_CheckBox_Sensor4.isChecked():
                        self.ui.Plotting_Widget.setEnabled(True)
                    else:
                        self.ui.Plotting_Widget.setEnabled(False)
                else:
                    self.ui.Plotting_Widget.setEnabled(False)
            else:
                self.ui.Plotting_Widget.setEnabled(False)
        else:
            self.ui.Plotting_Widget.setEnabled(False)
                    
    def ButtonClicked_Plot(self):
        print("Plotting!")
        
        # basic window setup
        self.window = QtWidgets.QMainWindow()
        self.uiPlotting = Ui_PlottingWindow()
        self.uiPlotting.setupUi(self.window)
        
        # # loading data
        # for Input_Calibrator_Filename in self.Input_Calibrator_Filename:
        #     Loader(Input_Calibrator_Filename, self.dic, 1)

        # creat figure
        sc = MplCanvas(self.window)

        # plotting
        for i in range(16):
            sc.axesList[i].plot([0,1,2,3,4], [10,1,20,3,40])

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self.window)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.window.setCentralWidget(widget)

        self.window.show()
            