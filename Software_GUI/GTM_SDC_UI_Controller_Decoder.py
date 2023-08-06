#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

# Ref: https://shengyu7697.github.io/python-pyqt-qthread/

import os
import sys
import numpy as np

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog

import pyqtgraph as pg
import pyqtgraph.exporters

from GTM_SDC_UI_Controller_Decoder_Thread import UiDecoderThread

class UiDecoder(object):
    def __init__(self):
        pass
    
    ### decoder_link_interface ###

    def decoder_input_file(self):

        # Get input file
        self.decoder_input_file_list, _ = QFileDialog.getOpenFileNames(self, "Open file", "./")

        # Cache input file
        if len(self.decoder_input_file_list) != 0: # with input file
            self.decoder_cached_input_file_list = self.decoder_input_file_list.copy()

        if len(self.decoder_cached_input_file_list) != 0: # with cached input file

            # Concatenate cached input file
            decoder_cached_input_file_list_print = ""
            for decoder_cached_input_file in self.decoder_cached_input_file_list:
                decoder_cached_input_file_list_print += f'{decoder_cached_input_file};'

            # Print cached input file
            self.ui.decoder_input_file_text.setText(decoder_cached_input_file_list_print)

            # Turn on relevant function and update it
            self.ui.decoder_data_type_group.setEnabled(True)
            self.decoder_data_type()

        else: # only in the beginning, not important
            pass

    def decoder_data_type(self):

        if self.ui.decoder_data_type_group.isEnabled():

            if self.ui.decoder_data_type_in_space_radio_button.isChecked(): # in space
                
                # Update value
                self.in_space_flag = 1

                # Turn on relevant function and update it
                self.ui.decoder_data_import_group.setEnabled(True)
                self.decoder_data_import()

            elif self.ui.decoder_data_type_on_ground_radio_button.isChecked(): # on ground

                # Update value
                self.in_space_flag = 2

                # Turn on relevant function and update it
                self.ui.decoder_data_import_group.setEnabled(True)
                self.decoder_data_import()
            
            else: # only in the beginning, not important
                pass
        
        else: # only in the beginning, not important
            pass

    def decoder_data_import(self):

        if self.ui.decoder_data_import_group.isEnabled():

            if self.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc
                
                # Update value
                self.decode_mode = 1
                
                # Turn off relevant function and update it
                self.ui.decoder_science_export_group.setEnabled(False)
                self.decoder_science_export()

            elif self.ui.decoder_data_import_science_radio_button.isChecked(): # science

                # Update value
                self.decode_mode = 2

                # Turn on relevant function and update it
                self.ui.decoder_science_export_group.setEnabled(True)
                self.decoder_science_export()

            else: # only in the beginning, not important
                pass

        else: # only in the beginning, not important
            pass

    def decoder_science_export(self):

        if self.ui.decoder_science_export_group.isEnabled(): # science
            
            if self.ui.decoder_science_export_raw_radio_button.isChecked(): # raw
                
                # Update value
                self.export_mode = 1

                # Turn off relevant function and update it
                self.ui.decoder_real_time_display_group.setEnabled(False)
                self.decoder_real_time_display()

            elif self.ui.decoder_science_export_pipeline_radio_button.isChecked(): # pipeline
                
                # Update value
                self.export_mode = 2

                # Turn on relevant function and update it
                self.ui.decoder_real_time_display_group.setEnabled(True)
                self.decoder_real_time_display()

            elif self.ui.decoder_science_export_both_radio_button.isChecked(): # both
                
                # Update value
                self.export_mode = 3

                # Turn on relevant function and update it
                self.ui.decoder_real_time_display_group.setEnabled(True)
                self.decoder_real_time_display()

            else: # only in the beginning, important due to tmtc no need science_export
                
                # Turn off relevant function and update it
                self.ui.decoder_real_time_display_group.setEnabled(False)
                self.decoder_real_time_display()
        
        else:

            if self.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc

                # Update value
                self.export_mode = 0

                # Turn on relevant function and update it
                self.ui.decoder_real_time_display_group.setEnabled(True)
                self.decoder_real_time_display()

            else: # only in the beginning, not important
                pass

    def decoder_real_time_display(self):

        if self.ui.decoder_real_time_display_group.isEnabled(): # tmtc or science

            if self.ui.decoder_real_time_display_on_check_box.isChecked(): # with real-time display

                # Turn on relevant function
                self.ui.decoder_auto_save_figure_group.setEnabled(True)

                if self.ui.decoder_data_type_in_space_radio_button.isChecked(): # in space

                    # Turn off relevant function
                    self.ui.decoder_update_time_group.setEnabled(False)

                elif self.ui.decoder_data_type_on_ground_radio_button.isChecked(): # on ground

                    # Turn on relevant function
                    self.ui.decoder_update_time_group.setEnabled(True)

                # Turn on relevant function and update it
                self.ui.decoder_display_selection_group.setEnabled(True)
                self.decoder_display_selection()
                
            else: # without real-time display

                # Turn off relevant function
                self.ui.decoder_auto_save_figure_group.setEnabled(False)
                self.ui.decoder_update_time_group.setEnabled(False)

                # Turn off relevant function and update it
                self.ui.decoder_display_selection_group.setEnabled(False)
                self.decoder_display_selection()

        else:

            if self.ui.decoder_science_export_raw_radio_button.isChecked(): # science raw

                # Turn off relevant function
                self.ui.decoder_auto_save_figure_group.setEnabled(False)
                self.ui.decoder_update_time_group.setEnabled(False)
                
                # Turn off relevant function and update it
                self.ui.decoder_display_selection_group.setEnabled(False)
                self.decoder_display_selection()

            else: # only in the beginning, important due to tmtc no need science_export
                
                # Turn off relevant function
                self.ui.decoder_auto_save_figure_group.setEnabled(False)
                self.ui.decoder_update_time_group.setEnabled(False)
                
                # Turn off relevant function and update it
                self.ui.decoder_display_selection_group.setEnabled(False)
                self.decoder_display_selection()

    def decoder_display_selection(self):

        if self.ui.decoder_display_selection_group.isEnabled():

            if self.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc

                # Turn off relevant function
                self.ui.decoder_display_selection_master_s1_check_box.setEnabled(False)
                self.ui.decoder_display_selection_master_s2_check_box.setEnabled(False)
                self.ui.decoder_display_selection_master_s3_check_box.setEnabled(False)
                self.ui.decoder_display_selection_master_s4_check_box.setEnabled(False)
                self.ui.decoder_display_selection_slave_s1_check_box.setEnabled(False)
                self.ui.decoder_display_selection_slave_s2_check_box.setEnabled(False)
                self.ui.decoder_display_selection_slave_s3_check_box.setEnabled(False)
                self.ui.decoder_display_selection_slave_s4_check_box.setEnabled(False)

                if self.ui.decoder_display_selection_master_group.isChecked() or \
                self.ui.decoder_display_selection_slave_group.isChecked():  # with any module checked

                    # Ready to run
                    self.ui.decoder_run_group.setEnabled(True)
                
                else: # without any module checked

                    # Turn off relevant function
                    self.ui.decoder_run_group.setEnabled(False)

            else: # science

                # Turn on relevant function due to tmtc no need sensor check box
                self.ui.decoder_display_selection_master_s1_check_box.setEnabled(True)
                self.ui.decoder_display_selection_master_s2_check_box.setEnabled(True)
                self.ui.decoder_display_selection_master_s3_check_box.setEnabled(True)
                self.ui.decoder_display_selection_master_s4_check_box.setEnabled(True)
                self.ui.decoder_display_selection_slave_s1_check_box.setEnabled(True)
                self.ui.decoder_display_selection_slave_s2_check_box.setEnabled(True)
                self.ui.decoder_display_selection_slave_s3_check_box.setEnabled(True)
                self.ui.decoder_display_selection_slave_s4_check_box.setEnabled(True)
            
                if self.ui.decoder_display_selection_master_group.isChecked(): # display master

                    if (not self.ui.decoder_display_selection_master_s1_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_master_s2_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_master_s3_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_master_s4_check_box.isChecked()): # without any master's sensor checked

                        # Turn off relevant function
                        self.ui.decoder_run_group.setEnabled(False)
                    
                    else: 

                        if self.ui.decoder_display_selection_slave_group.isChecked(): # also display slave

                            if (not self.ui.decoder_display_selection_slave_s1_check_box.isChecked()) and \
                            (not self.ui.decoder_display_selection_slave_s2_check_box.isChecked()) and \
                            (not self.ui.decoder_display_selection_slave_s3_check_box.isChecked()) and \
                            (not self.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # without any slave's sensor checked

                                # Turn off relevant function
                                self.ui.decoder_run_group.setEnabled(False)

                            else: # with any slave's sensor checked

                                # Ready to run
                                self.ui.decoder_run_group.setEnabled(True)
                        
                        else: # with any master's sensor checked

                            # Ready to run
                            self.ui.decoder_run_group.setEnabled(True)
                
                elif self.ui.decoder_display_selection_slave_group.isChecked(): # only display slave

                    if (not self.ui.decoder_display_selection_slave_s1_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_slave_s2_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_slave_s3_check_box.isChecked()) and \
                    (not self.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # without any slave's sensor checked

                        # Turn off relevant function
                        self.ui.decoder_run_group.setEnabled(False)
                    
                    else: # with any slave's sensor checked

                        # Ready to run
                        self.ui.decoder_run_group.setEnabled(True)

                else: # without any module checked

                    # Turn off relevant function
                    self.ui.decoder_run_group.setEnabled(False)
        
        else: 
            
            if self.ui.decoder_real_time_display_group.isEnabled(): # without real-time display

                # Ready to run
                self.ui.decoder_run_group.setEnabled(True)
            
            else:

                if self.ui.decoder_science_export_raw_radio_button.isChecked(): # science raw

                    # Ready to run
                    self.ui.decoder_run_group.setEnabled(True)
                
                else: # only in the beginning, important due to tmtc no need science_export
                    
                    # Turn off relevant function
                    self.ui.decoder_run_group.setEnabled(False)
    
    ### decoder_link_interface_end ###

    ### decoder_start ###

    def decoder_start(self):

        # Create list to store layout for closing
        self.decoder_plot_open_window_list = []

        # Import UiDecoderThread
        self.decoder_thread = UiDecoderThread(self)

        # Connect pyqt signal
        self.decoder_thread.decoder_thread_open_tmtc_signal.connect(self.decoder_plot_open_window_tmtc) 
        self.decoder_thread.decoder_thread_open_science_signal.connect(self.decoder_plot_open_window_science) 
        self.decoder_thread.decoder_thread_clear_layout_signal.connect(self.decoder_clear_layout) 
        self.decoder_thread.decoder_thread_file_signal.connect(self.decoder_cache_file_dirname_basename)
        self.decoder_thread.decoder_thread_update_count_signal.connect(self.decoder_cache_update_count)
        self.decoder_thread.decoder_thread_plot_tmtc_signal.connect(self.decoder_plot_tmtc)
        self.decoder_thread.decoder_thread_update_tmtc_signal.connect(self.decoder_update_plot_tmtc) 
        self.decoder_thread.decoder_thread_plot_update_science_hg_signal.connect(self.decoder_plot_science_robotic) 
        self.decoder_thread.decoder_thread_plot_update_science_lg_signal.connect(self.decoder_plot_science_robotic) 
        self.decoder_thread.decoder_thread_finish_signal.connect(self.decoder_close_all_figure_refresh)

        # Start threading
        self.decoder_thread.start()
    
    def decoder_plot_open_window_tmtc(self):

        # Create layout to hold multiple subplot
        self.decoder_plot_tmtc_pg_layout = pg.GraphicsLayoutWidget(title='TMTC')
        self.decoder_plot_tmtc_pg_layout.showMaximized()

        # Store layout for closing
        self.decoder_plot_open_window_list.append(self.decoder_plot_tmtc_pg_layout)

    def decoder_plot_open_window_science(self):

        if self.ui.decoder_display_selection_master_group.isChecked() and \
        (self.ui.decoder_display_selection_master_s1_check_box.isChecked() or \
        self.ui.decoder_display_selection_master_s2_check_box.isChecked()): # M1 or M2

            # Create layout to hold multiple subplot
            globals()['self.decoder_plot_science_pg_layout_master_b_hg'] = pg.GraphicsLayoutWidget(title='Master CITIROC B HG')
            globals()['self.decoder_plot_science_pg_layout_master_b_hg'].showMaximized()
            globals()['self.decoder_plot_science_pg_layout_master_b_lg'] = pg.GraphicsLayoutWidget(title='Master CITIROC B LG')
            globals()['self.decoder_plot_science_pg_layout_master_b_lg'].showMaximized()

            # Store layout for closing
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_master_b_hg'])
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_master_b_lg'])

        if self.ui.decoder_display_selection_master_group.isChecked() and \
        (self.ui.decoder_display_selection_master_s3_check_box.isChecked() or \
        self.ui.decoder_display_selection_master_s4_check_box.isChecked()): # M3 or M4

            # Create layout to hold multiple subplot
            globals()['self.decoder_plot_science_pg_layout_master_a_hg'] = pg.GraphicsLayoutWidget(title='Master CITIROC A HG')
            globals()['self.decoder_plot_science_pg_layout_master_a_hg'].showMaximized()
            globals()['self.decoder_plot_science_pg_layout_master_a_lg'] = pg.GraphicsLayoutWidget(title='Master CITIROC A LG')
            globals()['self.decoder_plot_science_pg_layout_master_a_lg'].showMaximized()

            # Store layout for closing
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_master_a_hg'])
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_master_a_lg'])

        if self.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.ui.decoder_display_selection_slave_s1_check_box.isChecked() or \
        self.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # S1 or S2

            # Create layout to hold multiple subplot
            globals()['self.decoder_plot_science_pg_layout_slave_b_hg'] = pg.GraphicsLayoutWidget(title='Slave CITIROC B HG')
            globals()['self.decoder_plot_science_pg_layout_slave_b_hg'].showMaximized()
            globals()['self.decoder_plot_science_pg_layout_slave_b_lg'] = pg.GraphicsLayoutWidget(title='Slave CITIROC B LG')
            globals()['self.decoder_plot_science_pg_layout_slave_b_lg'].showMaximized()

            # Store layout for closing
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_slave_b_hg'])
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_slave_b_lg'])

        if self.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.ui.decoder_display_selection_slave_s3_check_box.isChecked() or \
        self.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # S3 or S4

            # Create layout to hold multiple subplot
            globals()['self.decoder_plot_science_pg_layout_slave_a_hg'] = pg.GraphicsLayoutWidget(title='Slave CITIROC A HG')
            globals()['self.decoder_plot_science_pg_layout_slave_a_hg'].showMaximized()
            globals()['self.decoder_plot_science_pg_layout_slave_a_lg'] = pg.GraphicsLayoutWidget(title='Slave CITIROC A LG')
            globals()['self.decoder_plot_science_pg_layout_slave_a_lg'].showMaximized()

            # Store layout for closing
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_slave_a_hg'])
            self.decoder_plot_open_window_list.append(globals()['self.decoder_plot_science_pg_layout_slave_a_lg'])
    
    def decoder_clear_layout(self):

        # Clear all opened layout
        for decoder_plot_open_window_science in self.decoder_plot_open_window_list:
            decoder_plot_open_window_science.clear()

    def decoder_cache_file_dirname_basename(self, file_list):
        
        # Cache dirname and basename
        self.decoder_cached_input_file_dirname = file_list[0]
        self.decoder_cached_input_file_basename = file_list[1]
    
    def decoder_cache_update_count(self, update_count):
        
        # Cache update count
        self.decoder_update_counter = update_count

    def decoder_plot_tmtc(self, df_list):

        if self.ui.decoder_display_selection_master_group.isChecked() and \
        self.ui.decoder_display_selection_slave_group.isChecked(): # master and slave
            
            # Add subplot
            self.decoder_plot_tmtc_pg_layout_master \
            = self.decoder_plot_tmtc_pg_layout.addPlot(row=0, 
                                                       col=0, 
                                                       title='Master Board Temperature # 1', 
                                                       labels={'left': 'Temperature [°C]', 'bottom': 'Data Count [#]'})
            self.decoder_plot_tmtc_pg_layout_slave \
            = self.decoder_plot_tmtc_pg_layout.addPlot(row=0, 
                                                       col=1, 
                                                       title='Slave Board Temperature # 1', 
                                                       labels={'left': 'Temperature [°C]', 'bottom': 'Data Count [#]'})

            # Plot
            self.decoder_plot_tmtc_pg_layout_master_line \
            = self.decoder_plot_tmtc_pg_layout_master.plot(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                           df_list[0]['Board Temperature#1'].to_numpy(), 
                                                           pen=pg.mkPen(color=(255, 0, 0)))
            self.decoder_plot_tmtc_pg_layout_slave_line \
            = self.decoder_plot_tmtc_pg_layout_slave.plot(np.arange(len(df_list[1]['Board Temperature#1'])), 
                                                          df_list[1]['Board Temperature#1'].to_numpy(), 
                                                          pen=pg.mkPen(color=(0, 0, 255)))

        elif self.ui.decoder_display_selection_master_group.isChecked(): # only master
            
            # Add subplot
            self.decoder_plot_tmtc_pg_layout_master \
            = self.decoder_plot_tmtc_pg_layout.addPlot(row=0, 
                                                       col=0, 
                                                       title='Master Board Temperature # 1', 
                                                       labels={'left': 'Temperature [°C]', 'bottom': 'Data Count [#]'})

            # Plot
            self.decoder_plot_tmtc_pg_layout_master_line \
            = self.decoder_plot_tmtc_pg_layout_master.plot(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                           df_list[0]['Board Temperature#1'].to_numpy(), 
                                                           pen=pg.mkPen(color=(255, 0, 0)))

        else: # only slave
            
            # Add subplot
            self.decoder_plot_tmtc_pg_layout_slave \
            = self.decoder_plot_tmtc_pg_layout.addPlot(row=0, 
                                                       col=0, 
                                                       title='Slave Board Temperature # 1', 
                                                       labels={'left': 'Temperature [°C]', 'bottom': 'Data Count [#]'})

            # Plot
            self.decoder_plot_tmtc_pg_layout_slave_line \
            = self.decoder_plot_tmtc_pg_layout_slave.plot(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                          df_list[0]['Board Temperature#1'].to_numpy(), 
                                                          pen=pg.mkPen(color=(0, 0, 255)))
        
        # Show layout
        self.decoder_plot_tmtc_pg_layout.show()

        if self.ui.decoder_auto_save_figure_group.isEnabled() and \
        self.ui.decoder_auto_save_figure_on_check_box.isChecked(): # need auto-save figure
                
            # Save layout
            exporter = pg.exporters.ImageExporter(self.decoder_plot_tmtc_pg_layout.scene())
            exporter.export(os.path.join(self.decoder_cached_input_file_dirname, f'{self.decoder_cached_input_file_basename}.decoder_plot_tmtc_pg_layout.png'))

        else: # just display on screen
            pass
    
    def decoder_update_plot_tmtc(self, df_list):

        if self.ui.decoder_display_selection_master_group.isChecked() and \
        self.ui.decoder_display_selection_slave_group.isChecked(): # master and slave
            
            # Update plotting
            self.decoder_plot_tmtc_pg_layout_master_line.setData(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                                 df_list[0]['Board Temperature#1'].to_numpy())
            self.decoder_plot_tmtc_pg_layout_slave_line.setData(np.arange(len(df_list[1]['Board Temperature#1'])), 
                                                                df_list[1]['Board Temperature#1'].to_numpy()) 
        
        elif self.ui.decoder_display_selection_master_group.isChecked(): # only master
            
            # Update plotting
            self.decoder_plot_tmtc_pg_layout_master_line.setData(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                                 df_list[0]['Board Temperature#1'].to_numpy()) 

        else: # only slave
            
            # Update plotting
            self.decoder_plot_tmtc_pg_layout_slave_line.setData(np.arange(len(df_list[0]['Board Temperature#1'])), 
                                                                df_list[0]['Board Temperature#1'].to_numpy())

        # Show layout
        self.decoder_plot_tmtc_pg_layout.show()

        # Keep the application responsive!
        QtWidgets.QApplication.processEvents()  

        if self.ui.decoder_auto_save_figure_group.isEnabled() and \
            self.ui.decoder_auto_save_figure_on_check_box.isChecked(): # need auto-save figure
                
            # Save new layout
            exporter = pg.exporters.ImageExporter(self.decoder_plot_tmtc_pg_layout.scene())
            exporter.export(os.path.join(self.decoder_cached_input_file_dirname, f'{self.decoder_cached_input_file_basename}.decoder_plot_tmtc_pg_layout_{self.decoder_update_counter}.png'))

        else: # just display on screen
            pass

    def decoder_plot_science_robotic(self, info_list):
        
        if info_list[0] == True: # plot each channel

            if info_list[1] == False: # first plotting

                if info_list[8] == 1: # hg

                    # Add subplot
                    globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg_{info_list[5]+info_list[8]}'] \
                    = globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg'].addPlot(row=info_list[4][0], 
                                                                                                        col=info_list[4][1], 
                                                                                                        title=f'{info_list[7]}_channel_{info_list[5]+info_list[8]}')
                    if info_list[-1] != False: # with data
                        
                        # Plot
                        globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg_{info_list[5]+info_list[8]}_line'] \
                        = globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg_{info_list[5]+info_list[8]}'].plot(info_list[11][:-1], 
                                                                                                                                    info_list[10], 
                                                                                                                                    pen=pg.mkPen(color=info_list[9]))

                if info_list[8] == 0: # lg

                    # Add subplot
                    globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg_{info_list[5]+info_list[8]}'] \
                    = globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg'].addPlot(row=info_list[4][0], 
                                                                                                        col=info_list[4][1], 
                                                                                                        title=f'{info_list[7]}_channel_{info_list[5]+info_list[8]}')

                    if info_list[-1] != False: # with data

                        # Plot
                        globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg_{info_list[5]+info_list[8]}_line'] \
                        = globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg_{info_list[5]+info_list[8]}'].plot(info_list[11][:-1], 
                                                                                                                                    info_list[10], 
                                                                                                                                    pen=pg.mkPen(color=info_list[9]))

            else: # update plotting

                if info_list[8] == 1: # hg

                    if info_list[-1] != 0: # with data

                        # Update plotting
                        globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg_{info_list[5]+info_list[8]}_line'].setData(info_list[11][:-1], info_list[10])

                if info_list[8] == 0: # lg

                    if info_list[-1] != False: # with data

                        # Update plotting
                        globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg_{info_list[5]+info_list[8]}_line'].setData(info_list[11][:-1], info_list[10])

        else: # display and save

            if info_list[1] == False: # first plotting

                # Show layout 
                globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg'].show()
                globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg'].show()

                if self.ui.decoder_auto_save_figure_group.isEnabled() and \
                self.ui.decoder_auto_save_figure_on_check_box.isChecked(): # need auto-save figure
                    
                    # Save layout
                    exporter_hg = pg.exporters.ImageExporter(globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg'].scene())
                    exporter_lg = pg.exporters.ImageExporter(globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg'].scene())
                    exporter_hg.export(os.path.join(self.decoder_cached_input_file_dirname, 
                                                    f'{self.decoder_cached_input_file_basename}.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg.png'))
                    exporter_lg.export(os.path.join(self.decoder_cached_input_file_dirname, 
                                                    f'{self.decoder_cached_input_file_basename}.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg.png'))

                else: # just display on screen
                    pass
            
            else: # update plotting
                
                # Show layout 
                globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg'].show()
                globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg'].show()

                # Keep the application responsive!
                QtWidgets.QApplication.processEvents()

                if self.ui.decoder_auto_save_figure_group.isEnabled() and \
                self.ui.decoder_auto_save_figure_on_check_box.isChecked(): # need auto-save figure
                    
                    # Save new layout
                    exporter_hg = pg.exporters.ImageExporter(globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg'].scene())
                    exporter_lg = pg.exporters.ImageExporter(globals()[f'self.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg'].scene())
                    exporter_hg.export(os.path.join(self.decoder_cached_input_file_dirname, 
                                                    f'{self.decoder_cached_input_file_basename}.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_hg_{self.decoder_update_counter}.png'))
                    exporter_lg.export(os.path.join(self.decoder_cached_input_file_dirname, 
                                                    f'{self.decoder_cached_input_file_basename}.decoder_plot_science_pg_layout_{info_list[2]}_{info_list[3]}_lg_{self.decoder_update_counter}.png'))

                else: # just display on screen
                    pass

    ### decoder_start_end ###

    ### decoder_close_all_figure ###

    def decoder_close_all_figure_refresh(self):
        
        if len(self.decoder_plot_open_window_list) == 0: # without layout

            # Turn on relevant function
            self.ui.decoder_close_all_figure_button.setEnabled(False)

        else: # with layout

            # Turn on relevant function
            self.ui.decoder_close_all_figure_button.setEnabled(True)

    def decoder_close_all_figure(self):

        # Run all opened layout
        for decoder_plot_open_window_science in self.decoder_plot_open_window_list:
            decoder_plot_open_window_science.clear()
            decoder_plot_open_window_science.close()
        
        # Initialize layout list
        self.decoder_plot_open_window_list = []
        
        # Turn off relevant function
        self.ui.decoder_close_all_figure_button.setEnabled(False)

    ### decoder_close_all_figure_end ###
    
    ### decoder_terminate ###

    def decoder_terminate(self):
        sys.exit()

    ### decoder_terminate_end ###