#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

# Ref: https://www.wongwonggoods.com/all-posts/python/pyqt5/pyqt5-5/

from PyQt5 import QtWidgets

from GTM_SDC_UI import Ui_MainWindow # ouput from pyuic5 -x xxx.ui -o xxx.py
from GTM_SDC_UI_Controller_Decoder import UiDecoder

class MainWindowController(QtWidgets.QMainWindow, UiDecoder):
    def __init__(self):

        # Run __init__() in parent class
        # Here is for QtWidgets.QMainWindow due to further self.ui.setupUi(self)
        super().__init__() # in python3, super(Class, self).xxx = super().xxx

        # Import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Run Backend
        self.setup_controller()

    def setup_controller(self):
        
        ### decoder ###

        # Input file
        self.ui.decoder_input_file_button.clicked.connect(self.decoder_input_file)

        #-----
        
        # Data type
        self.ui.decoder_data_type_group.setEnabled(False)
        self.ui.decoder_data_type_in_space_radio_button.clicked.connect(self.decoder_data_type)
        self.ui.decoder_data_type_on_ground_radio_button.clicked.connect(self.decoder_data_type)

        # Data import
        self.ui.decoder_data_import_group.setEnabled(False)
        self.ui.decoder_data_import_tmtc_radio_button.clicked.connect(self.decoder_data_import)
        self.ui.decoder_data_import_science_radio_button.clicked.connect(self.decoder_data_import)

        # Science export
        self.ui.decoder_science_export_group.setEnabled(False)
        self.ui.decoder_science_export_raw_radio_button.clicked.connect(self.decoder_science_export)
        self.ui.decoder_science_export_pipeline_radio_button.clicked.connect(self.decoder_science_export)
        self.ui.decoder_science_export_both_radio_button.clicked.connect(self.decoder_science_export)
        
        #-----

        # Real-time display
        self.ui.decoder_real_time_display_group.setEnabled(False)
        self.ui.decoder_real_time_display_on_check_box.clicked.connect(self.decoder_real_time_display)

        # Auto-save figure
        self.ui.decoder_auto_save_figure_group.setEnabled(False)

        # Update time
        self.ui.decoder_update_time_group.setEnabled(False)

        # Display selection
        self.ui.decoder_display_selection_group.setEnabled(False)
        self.ui.decoder_display_selection_master_group.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_slave_group.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_master_s1_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_master_s2_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_master_s3_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_master_s4_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_slave_s1_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_slave_s2_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_slave_s3_check_box.clicked.connect(self.decoder_display_selection)
        self.ui.decoder_display_selection_slave_s4_check_box.clicked.connect(self.decoder_display_selection)
        
        #-----

        # Start & terminate
        self.ui.decoder_run_group.setStyleSheet("QGroupBox{border:none}")
        self.ui.decoder_run_group.setEnabled(False)
        self.ui.decoder_close_all_figure_button.setEnabled(False)
        self.ui.decoder_start_button.clicked.connect(self.decoder_start)
        self.ui.decoder_close_all_figure_button.clicked.connect(self.decoder_close_all_figure)
        self.ui.decoder_terminate_button.clicked.connect(self.decoder_terminate)

        ### decoder_end ###

        ### calibrator ###
        ### calibrator_end ###

        ### localizor ###
        ### localizor_end ###