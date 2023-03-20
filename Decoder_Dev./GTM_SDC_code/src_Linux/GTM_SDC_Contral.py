#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2

from GTM_SDC_UI import Ui_MainWindow
from GTM_SDC_Contral_C_Decoder import C_Decoder

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
        
        # Input File
        self.ui.InputFile_Decoder_Button.clicked.connect(self.Open_File)
        self.Input_Decoder_Filename = ""
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
        
        ### Plotting ###
        self.ui.Plotting_Button.clicked.connect(self.ButtonClicked_Plotting)
        self.Clicked_Counter_Plotting = 0
        
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
    
    def Open_File(self):
        self.Input_Decoder_Filename, self.Input_Decoder_Filetype = QFileDialog.getOpenFileName(self, "Open file", "./")
        self.ui.InputFile_Decoder_Text.setText(self.Input_Decoder_Filename)
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
        if self.Input_Decoder_Filename != "":
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
        print("Running!")
        C_Decoder(self.Input_Decoder_Filename, self.Decode_Modes, self.Extract_Selection, self.Export_Modes, self.Hit_Selection)
            
    def ButtonClicked_Plotting(self):
        self.Clicked_Counter_Plotting += 1
        if (self.Clicked_Counter_Plotting%2) != 0:
            self.ui.Plotting_Button.setStyleSheet("background-color: #2B5DD1;"
                                                  "color: #FFFFFF;"
                                                  "border-style: outset;"
                                                  "padding: 2px;"
                                                  "font: bold 20px;"
                                                  "border-width: 3px;"
                                                  "border-radius: 10px;"
                                                  "border-color: #2752B8;")
            self.ui.Plotting_Button_Status.setText("Plotting Selected!")
        else:
            self.ui.Plotting_Button.setStyleSheet("")
            self.ui.Plotting_Button_Status.setText("     ")
                
                








