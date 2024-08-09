#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

# Ref: https://www.wongwonggoods.com/all-posts/python/pyqt5/pyqt5-5/

from PyQt5 import QtWidgets

from GTM_SDC_UI import Ui_MainWindow # ouput from pyuic5 -x xxx.ui -o xxx.py

from GTM_SDC_UI_Controller_Flow import UiFlow
from GTM_SDC_UI_Controller_Mtl_Cmd import UiMtlCmd
from GTM_SDC_UI_Controller_Decoder import UiDecoder
from GTM_SDC_UI_Controller_Localizer import UiLocalizer

class MainWindowController(QtWidgets.QMainWindow, UiFlow, UiMtlCmd, UiDecoder, UiLocalizer):
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

        ### flow ###

        # Operation server login credentials
        self.ui.flow_operation_user_line.textChanged.connect(self.flow_operation_user)
        self.ui.flow_operation_host_line.textChanged.connect(self.flow_operation_host)
        self.ui.flow_operation_password_line.textChanged.connect(self.flow_operation_password)

        # SOCC ↔︎ operation server
        self.ui.flow_socc_operation_group.setEnabled(False)
        self.ui.flow_socc_operation_update_socc_button.clicked.connect(self.flow_socc_operation_update_socc)
        self.ui.flow_socc_operation_update_operation_button.clicked.connect(self.flow_socc_operation_update_operation)
        self.ui.flow_socc_operation_clone_button.clicked.connect(self.flow_socc_operation_clone)
        self.ui.flow_socc_operation_push_button.clicked.connect(self.flow_socc_operation_push)

        # Operation ↔︎ processing server
        self.ui.flow_operation_processing_group.setEnabled(False)
        self.ui.flow_operation_processing_update_operation_button.clicked.connect(self.flow_operation_processing_update_operation)
        self.ui.flow_operation_processing_update_processing_button.clicked.connect(self.flow_operation_processing_update_processing)
        self.ui.flow_operation_processing_clone_button.clicked.connect(self.flow_operation_processing_clone)
        self.ui.flow_operation_processing_push_button.clicked.connect(self.flow_operation_processing_push)

        #-----

        # Archiving server login credentials
        self.ui.flow_archiving_user_line.textChanged.connect(self.flow_archiving_user)
        self.ui.flow_archiving_host_line.textChanged.connect(self.flow_archiving_host)
        self.ui.flow_archiving_password_line.textChanged.connect(self.flow_archiving_password)

        # Processing → archiving server
        self.ui.flow_processing_archiving_group.setEnabled(False)
        self.ui.flow_processing_archiving_update_processing_button.clicked.connect(self.flow_processing_archiving_update_processing)
        self.ui.flow_processing_archiving_update_archiving_button.clicked.connect(self.flow_processing_archiving_update_archiving)
        self.ui.flow_processing_archiving_push_button.clicked.connect(self.flow_processing_archiving_push)

        ### flow_end ###

        ### mtl_cmd ###

        # Input file
        self.ui.mtl_input_2le_button.clicked.connect(self.mtl_input_2le)

        #---

        # Conditions
        self.ui.mtl_conditions_group.setEnabled(False)

        # Start time
        self.ui.mtl_current_utc_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_assign_utc_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_assign_utc_line.textChanged.connect(self.mtl_conditions)

        # Period
        self.ui.mtl_orbits_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_orbits_line.textChanged.connect(self.mtl_conditions)
        self.ui.mtl_days_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_days_line.textChanged.connect(self.mtl_conditions)
        self.ui.mtl_hours_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_hours_line.textChanged.connect(self.mtl_conditions)
        self.ui.mtl_minutes_radio_button.clicked.connect(self.mtl_conditions)
        self.ui.mtl_minutes_line.textChanged.connect(self.mtl_conditions)

        # SAA threshold
        self.ui.mtl_saa_check_box.clicked.connect(self.mtl_conditions)
        self.ui.mtl_saa_line.textChanged.connect(self.mtl_conditions)

        #---

        # Generate MTL
        self.ui.mtl_generate_button.setEnabled(False)
        self.ui.mtl_generate_button.clicked.connect(self.mtl_generate)

        #-----

        # Generate CMD
        self.ui.cmd_generate_button.setEnabled(False)
        self.ui.cmd_generate_button.clicked.connect(self.cmd_generate)

        ### mtl_cmd_end ###
        
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

        ### localizer ###

        # Input decoded and calibrated .vc3 file
        self.ui.find_input_file_button.clicked.connect(self.find_input_file)

        #---

        # Slice time
        self.ui.find_slice_time_group.setEnabled(False)
        self.ui.find_slice_time_group.clicked.connect(self.find_slice)
        self.ui.find_slice_time_start_line.textChanged.connect(self.find_slice)
        self.ui.find_slice_time_end_line.textChanged.connect(self.find_slice)

        # Slice energy
        self.ui.find_slice_energy_group.setEnabled(False)
        self.ui.find_slice_energy_group.clicked.connect(self.find_slice)
        self.ui.find_slice_energy_min_line.textChanged.connect(self.find_slice)
        self.ui.find_slice_energy_max_line.textChanged.connect(self.find_slice)

        #---

        # Preview & Search
        self.ui.find_preview_lc_button.setEnabled(False)
        self.ui.find_preview_lc_button.clicked.connect(self.find_preview)
        self.ui.find_search_grb_button.setEnabled(False)
        self.ui.find_search_grb_button.clicked.connect(self.find_search)

        #-----

        # Input trigger info.
        self.ui.localize_input_file_button.clicked.connect(self.localize_input_file)

        #---

        # Localize
        self.ui.localize_grb_button.setEnabled(False)
        self.ui.localize_grb_button.clicked.connect(self.localize_start)

        ### localizer_end ###