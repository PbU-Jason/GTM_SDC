#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:58:23 2022

@author: jasonpbu
"""

# Ref: https://shengyu7697.github.io/python-pyqt-qthread/

import os
import time
import numpy as np
import pandas as pd
from itertools import product

from PyQt5.QtCore import QThread, pyqtSignal

from GTM_SDC_UI_Controller_Decoder_Thread_C import c_decoder

class UiDecoderThread(QThread):

    # Create pyqt signal
    decoder_thread_open_tmtc_signal = pyqtSignal()
    decoder_thread_open_science_signal = pyqtSignal()
    decoder_thread_clear_layout_signal = pyqtSignal()
    decoder_thread_file_signal = pyqtSignal(list)
    decoder_thread_update_count_signal = pyqtSignal(int)
    decoder_thread_plot_tmtc_signal = pyqtSignal(list)
    decoder_thread_update_tmtc_signal = pyqtSignal(list)
    decoder_thread_plot_update_science_hg_signal = pyqtSignal(list)
    decoder_thread_plot_update_science_lg_signal = pyqtSignal(list)
    decoder_thread_finish_signal = pyqtSignal()

    def __init__(self, parent):
        
        # Run __init__() in parent class
        # Here is forQThread
        super().__init__() # in python3, super(Class, self).xxx = super().xxx

        # Import useful info in MainWindowController, mainly parent.ui
        self.parent = parent
    
    # Make thread happend in QThread!
    def run(self):
        self.decoder_start()

    ### decoder_start ###

    def decoder_start(self):

        # Get number of input file
        self.decoder_cached_input_file_number = len(self.parent.decoder_cached_input_file_list)
        
        if (not self.parent.ui.decoder_real_time_display_on_check_box.isChecked()) or \
        self.parent.ui.decoder_science_export_raw_radio_button.isChecked(): # only decode

            # Loop all file
            for decoder_cached_input_file_idx, decoder_cached_input_file in enumerate(self.parent.decoder_cached_input_file_list):

                # Initailize output file
                self.decoder_initailize_output_file(decoder_cached_input_file)

                # Run decoder in c
                _ = c_decoder(decoder_cached_input_file,
                              self.parent.in_space_flag,
                              self.parent.decode_mode, 
                              self.parent.export_mode, 
                              initail_file_pointer=0)
                
                # Print progress
                print(f'Finished/Total: {decoder_cached_input_file_idx+1} / {self.decoder_cached_input_file_number}')

                # Emit siganl back to parent class
                self.decoder_thread_finish_signal.emit()

        else: # decode and plot

            # Define fixed plotting variable
            self.decoder_plot_low_gain  = 2
            self.decoder_plot_high_gain = 20
            self.decoder_plot_bin_size  = 5
            self.decoder_plot_range_min  = -1000
            self.decoder_plot_range_max  = 2**14

            # Decode and plot
            self.decoder_plot()

            # Emit siganl back to parent class
            self.decoder_thread_finish_signal.emit()

    def decoder_initailize_output_file(self, filename):

        if self.parent.decode_mode == 1: # tmtc
            if os.path.exists(f'{filename}_tmtc_all.csv'):
                os.remove(f'{filename}_tmtc_all.csv')
            if os.path.exists(f'{filename}_tmtc_master.csv'):
                os.remove(f'{filename}_tmtc_master.csv')
            if os.path.exists(f'{filename}_tmtc_slave.csv'):
                os.remove(f'{filename}_tmtc_slave.csv')

        if (self.parent.decode_mode == 2) and ((self.parent.export_mode == 1) or (self.parent.export_mode == 3)): # science raw
            if os.path.exists(f'{filename}_science_raw.csv'):
                os.remove(f'{filename}_science_raw.csv')
        
        if (self.parent.decode_mode == 2) and ((self.parent.export_mode == 2) or (self.parent.export_mode == 3)): # science pipeline
            if os.path.exists(f'{filename}_science_pipeline.csv'):
                os.remove(f'{filename}_science_pipeline.csv')

    def decoder_initailize_plot_df_skip_number(self):

        # For tmtc
        self.decoder_plot_tmtc_master_df = pd.DataFrame()
        self.decoder_plot_tmtc_master_df_skip_number = 0
        self.decoder_plot_tmtc_slave_df = pd.DataFrame()
        self.decoder_plot_tmtc_slave_df_skip_number = 0

        # For science
        self.decoder_plot_science_df = pd.DataFrame()
        self.decoder_plot_science_df_skip_number = 0
        self.decoder_plot_science_grouped_df = pd.DataFrame()

    def decoder_plot(self):

        if self.parent.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc 

            # Emit siganl back to parent class
            self.decoder_thread_open_tmtc_signal.emit()
        
        else: # science

            # Emit siganl back to parent class
            self.decoder_thread_open_science_signal.emit()

        if (not self.parent.ui.decoder_update_time_group.isEnabled()): # only plot one time
            self.decoder_update_time_s = 0 # 0 == False

        else: 

            if self.parent.ui.decoder_update_time_combo_box.currentText() == 'None': # only plot one time
                self.decoder_update_time_s = 0 # 0 == False

            else: # plot continuously
                self.decoder_update_time_s = int(self.parent.ui.Update_Rate_comboBox.currentText())

        # Loop all file
        for decoder_cached_input_file_idx, decoder_cached_input_file in enumerate(self.parent.decoder_cached_input_file_list):
            
            # Initailize output file
            self.decoder_initailize_output_file(decoder_cached_input_file)

            # Initialize changing plotting variable
            self.decoder_initailize_plot_df_skip_number()
            
            if self.parent.ui.decoder_auto_save_figure_group.isEnabled() and \
            self.parent.ui.decoder_auto_save_figure_on_check_box.isChecked(): # need auto-save figure

                # Emit siganl back to parent class
                self.decoder_thread_file_signal.emit([os.path.dirname(decoder_cached_input_file), os.path.basename(decoder_cached_input_file)])

            else: # just display on screen
                pass

            # Run decoder in c
            new_file_pointer = c_decoder(decoder_cached_input_file,
                                         self.parent.in_space_flag,
                                         self.parent.decode_mode, 
                                         self.parent.export_mode, 
                                         initail_file_pointer=0)

            # Emit siganl back to parent class
            self.decoder_thread_clear_layout_signal.emit()

            if self.parent.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc 

                if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
                self.parent.ui.decoder_display_selection_slave_group.isChecked(): # master and slave

                    # Plot tmtc
                    self.decoder_plot_tmtc([f'{decoder_cached_input_file}_tmtc_master.csv', f'{decoder_cached_input_file}_tmtc_slave.csv'])
                
                elif self.parent.ui.decoder_display_selection_master_group.isChecked(): # only master

                    # Plot tmtc
                    self.decoder_plot_tmtc([f'{decoder_cached_input_file}_tmtc_master.csv'])
                
                else: # only slave

                    # Plot tmtc
                    self.decoder_plot_tmtc([f'{decoder_cached_input_file}_tmtc_slave.csv'])
            
            else: # science

                # Plot science
                self.decoder_plot_science([f'{decoder_cached_input_file}_science_pipeline.csv'])

            if self.decoder_update_time_s == 0: # only plot one time

                # Print progress
                print(f'Finished/Total: {decoder_cached_input_file_idx+1} / {self.decoder_cached_input_file_number}')
            
            else: # plot continuously

                # Initailize update counter for save fugure
                self.decoder_update_counter = 0

                # Loop until break
                while True:
                    
                    # Refresh update counter
                    self.decoder_update_counter += 1

                    # Emit siganl back to parent class
                    self.decoder_thread_update_count_signal.emit(self.decoder_update_counter)

                    # Cache new file pointer
                    new_file_pointer_cached = new_file_pointer

                    # Wait update time (s)
                    print(f'Wait {self.decoder_update_time_s} s...')
                    time.sleep(self.decoder_update_time_s)

                    # Run decoder in c
                    new_file_pointer = c_decoder(decoder_cached_input_file,
                                                 self.parent.in_space_flag,
                                                 self.parent.decode_mode, 
                                                 self.parent.export_mode, 
                                                 initail_file_pointer=new_file_pointer_cached)
                    
                    # Compare new file pointer
                    if new_file_pointer == new_file_pointer_cached:

                        # Print progress
                        print(f'Finished/Total: {decoder_cached_input_file_idx+1} / {self.decoder_cached_input_file_number}')

                        break

                    else:

                        if self.parent.ui.decoder_data_import_tmtc_radio_button.isChecked(): # tmtc 

                            if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
                            self.parent.ui.decoder_display_selection_slave_group.isChecked(): # master and slave

                                # Update plotted tmtc
                                self.decoder_update_plot_tmtc([f'{decoder_cached_input_file}_tmtc_master.csv', f'{decoder_cached_input_file}_tmtc_slave.csv'])
                            
                            elif self.parent.ui.decoder_display_selection_master_group.isChecked(): # only master

                                # Update plotted tmtc
                                self.decoder_update_plot_tmtc([f'{decoder_cached_input_file}_tmtc_master.csv'])
                            
                            else: # only slave

                                # Update plotted tmtc
                                self.decoder_update_plot_tmtc([f'{decoder_cached_input_file}_tmtc_slave.csv'])
                        
                        else: # science

                            # Update plotted science
                            self.decoder_update_plot_science([f'{decoder_cached_input_file}_science_pipeline.csv'])      

    def decoder_plot_tmtc(self, filename_list):

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_group.isChecked(): # master and slave

            # Load df
            self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number)
            self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number \
            = self.decoder_load_df(filename_list[1], self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number)

            # Emit siganl back to parent class
            self.decoder_thread_plot_tmtc_signal.emit([self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_slave_df])

        elif self.parent.ui.decoder_display_selection_master_group.isChecked(): # only master
            
            # Load df
            self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number)
            
            # Emit siganl back to parent class
            self.decoder_thread_plot_tmtc_signal.emit([self.decoder_plot_tmtc_master_df])

        else: # only slave
            
            # Load df
            self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number)
            
            # Emit siganl back to parent class
            self.decoder_thread_plot_tmtc_signal.emit([self.decoder_plot_tmtc_slave_df])

    def decoder_load_df(self, filename, df, skip_number):

        if df.empty: # without data
            df = pd.read_csv(filename, sep=';')
        
        else: # with data

            # Load new data
            df_new = pd.read_csv(filename, sep=';', skiprows=skip_number)
            
            # Add column from old data for concatenate
            df_new.columns = df.columns

            # Concatenate df
            df = pd.concat([df, df_new], axis=0, ignore_channel_idx=True)
        
        # Update skip number
        skip_number = df.shape[0]
        
        return df, skip_number

    def decoder_update_plot_tmtc(self, filename_list):

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_group.isChecked(): # master and slave

            # Update df
            self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number)
            self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number \
            = self.decoder_load_df(filename_list[1], self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number)
            
            # Emit siganl back to parent class
            self.decoder_thread_update_tmtc_signal.emit([self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_slave_df])
        
        elif self.parent.ui.decoder_display_selection_master_group.isChecked(): # only master

            # Update df
            self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_master_df, self.decoder_plot_tmtc_master_df_skip_number)
            
            # Emit siganl back to parent class
            self.decoder_thread_update_tmtc_signal.emit([self.decoder_plot_tmtc_master_df])

        else: # only slave

            # Update df
            self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number \
            = self.decoder_load_df(filename_list[0], self.decoder_plot_tmtc_slave_df, self.decoder_plot_tmtc_slave_df_skip_number)
            
            # Emit siganl back to parent class
            self.decoder_thread_update_tmtc_signal.emit([self.decoder_plot_tmtc_slave_df])

    def decoder_plot_science(self, filename_list):

        # Load df
        self.decoder_plot_science_df, self.decoder_plot_science_df_skip_number \
        = self.decoder_load_df(filename_list[0], self.decoder_plot_science_df, self.decoder_plot_science_df_skip_number)
        
        # Group df
        self.decoder_plot_science_grouped_df = self.decoder_plot_science_df.groupby(['GTM ID', 'CITIROC', 'Channel', 'Gain'])

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # need to plot M1 and M2

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # only need to plot M1

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16)
        
        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # only need to plot M2

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # need to plot M3 and M4

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # only need to plot M3

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16)
        
        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # only need to plot M4

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # need to plot S1 and S2

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # only need to plot S1

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # only need to plot S2

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # need to plot S3 and S4

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # only need to plot S3

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # only need to plot S4

            # Plot, show and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0)
        
    def decoder_plot_science_robotic(self, module, citiroc, channel_row, channel_column, channel_shift, update=False):

        # Loop all channel
        for channel_idx, channel in enumerate(list(product(range(channel_row), range(channel_column)))):

            # Determine further variable (not concrete, but easier to read)
            if module == 'master':
                config_module = 0
                if citiroc == 'a':
                    config_citiroc = 0
                    hg_line_color = (250, 140, 0)
                    lg_line_color = (240, 170, 75)
                    if channel_row == 8: # plot two sensor
                        if channel[0] >= 4: # M3
                            sensor_name = 'sensor_3'
                        else: # M4
                            sensor_name = 'sensor_4'
                    else: # only plot one sensor
                        if channel_shift == 16: # M3
                            sensor_name = 'sensor_3'
                        else: # M4
                            sensor_name = 'sensor_2'
                else: 
                    config_citiroc = 1
                    hg_line_color = (255, 0, 0)
                    lg_line_color = (255, 110, 110)
                    if channel_row == 8: # plot two sensor
                        if channel[0] >= 4: # M1
                            sensor_name = 'sensor_1'
                        else: # M2
                            sensor_name = 'sensor_2'
                    else: # only plot one sensor
                        if channel_shift == 16: # M1
                            sensor_name = 'sensor_1'
                        else: # M2
                            sensor_name = 'sensor_2'
            else:
                config_module = 1
                if citiroc == 'a':
                    config_citiroc = 0
                    hg_line_color = (0, 100, 250)
                    lg_line_color = (90, 150, 252)
                    if channel_row == 8: # plot two sensor
                        if channel[0] >= 4: # S3
                            sensor_name = 'sensor_3'
                        else: # S4
                            sensor_name = 'sensor_4'
                    else: # only plot one sensor
                        if channel_shift == 16: # S3
                            sensor_name = 'sensor_3'
                        else: # S4
                            sensor_name = 'sensor_2'
                else: 
                    config_citiroc = 1
                    hg_line_color = (0, 0, 250)
                    lg_line_color = (80, 80, 250)
                    if channel_row == 8: # plot two sensor
                        if channel[0] >= 4: # S1
                            sensor_name = 'sensor_1'
                        else: # S2
                            sensor_name = 'sensor_2'
                    else: # only plot one sensor
                        if channel_shift == 16: # S1
                            sensor_name = 'sensor_1'
                        else: # S2
                            sensor_name = 'sensor_2'
            
            if update == False: # first plotting
                
                # Create configuration for groupby
                hg_config = ((config_module, config_citiroc, channel_idx+channel_shift, 1))
                lg_config = ((config_module, config_citiroc, channel_idx+channel_shift, 0))

                if hg_config in self.decoder_plot_science_grouped_df.groups.keys(): # with configuration

                    # Extract data by configuration
                    hg_config_df = self.decoder_plot_science_grouped_df.get_group(hg_config)

                    # Bin data
                    hist, bin_edges = np.histogram(hg_config_df['ADC'], 
                                                   bins=np.arange(self.decoder_plot_range_min, self.decoder_plot_range_max+self.decoder_plot_bin_size, self.decoder_plot_bin_size), 
                                                   density=False)

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_hg_signal.emit([True, update, module, citiroc, 
                                                                           channel, channel_idx, channel_shift, sensor_name,
                                                                           1, hg_line_color, hist, bin_edges,
                                                                           True])
                
                else: # without configuration

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_hg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            1, hg_line_color, 0, 0,
                                                                            False])

                if lg_config in self.decoder_plot_science_grouped_df.groups.keys(): # configuration exist

                    # Extract data by configuration
                    lg_config_df = self.decoder_plot_science_grouped_df.get_group(lg_config)

                    # Bin data
                    hist, bin_edges = np.histogram(lg_config_df['ADC'], 
                                                   bins=np.arange(self.decoder_plot_range_min, self.decoder_plot_range_max+self.decoder_plot_bin_size, self.decoder_plot_bin_size), 
                                                   density=False)
                    
                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_lg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            0, lg_line_color, hist, bin_edges,
                                                                            True])
                
                else: # without configuration

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_lg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            0, lg_line_color, 0, 0,
                                                                            False])
                

            else: # update plotting

                # Create configuration for groupby
                hg_config = ((config_module, config_citiroc, channel_idx+channel_shift, 1))
                lg_config = ((config_module, config_citiroc, channel_idx+channel_shift, 0))

                if hg_config in self.decoder_plot_science_grouped_df.groups.keys(): # configuration exist

                    # Extract data by configuration
                    hg_config_df = self.decoder_plot_science_grouped_df.get_group(hg_config)

                    # Bin data
                    hist, bin_edges = np.histogram(hg_config_df['ADC'], 
                                                   bins=np.arange(self.decoder_plot_range_min, self.decoder_plot_range_max+self.decoder_plot_bin_size, self.decoder_plot_bin_size), 
                                                   density=False)

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_hg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            1, hg_line_color, hist, bin_edges,
                                                                            True])
                
                else: # without configuration

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_hg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            1, hg_line_color, 0, 0,
                                                                            False])

                if lg_config in self.decoder_plot_science_grouped_df.groups.keys(): # configuration exist

                    # Extract data by configuration
                    lg_config_df = self.decoder_plot_science_grouped_df.get_group(lg_config)

                    # Bin data
                    hist, bin_edges = np.histogram(lg_config_df['ADC'], 
                                                   bins=np.arange(self.decoder_plot_range_min, self.decoder_plot_range_max+self.decoder_plot_bin_size, self.decoder_plot_bin_size), 
                                                   density=False)

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_lg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            0, lg_line_color, hist, bin_edges])
                
                else: # without configuration

                    # Emit siganl back to parent class
                    self.decoder_thread_plot_update_science_lg_signal.emit([True, update, module, citiroc, 
                                                                            channel, channel_idx, channel_shift, sensor_name,
                                                                            0, lg_line_color, 0, 0, ])
        # Emit siganl back to parent class
        self.decoder_thread_plot_update_science_lg_signal.emit([False, update, module, citiroc])

    def decoder_update_plot_science(self, filename_list):

        # Update df
        self.decoder_plot_science_df, self.decoder_plot_science_df_skip_number \
        = self.decoder_load_df(filename_list[0], self.decoder_plot_science_df, self.decoder_plot_science_df_skip_number)
        
        # Re-group df
        self.decoder_plot_science_grouped_df = self.decoder_plot_science_df.groupby(['GTM ID', 'CITIROC', 'Channel', 'Gain'])

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # need to plot M1 and M2

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # only need to plot M1

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16,
                                              update=True)
        
        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_master_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s2_check_box.isChecked()): # only need to plot M2

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # need to plot M3 and M4

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # only need to plot M3

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16,
                                              update=True)
        
        if self.parent.ui.decoder_display_selection_master_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_master_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_master_s4_check_box.isChecked()): # only need to plot M4

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='master',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # need to plot S1 and S2

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # only need to plot S1

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16,
                                              update=True)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_slave_s1_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s2_check_box.isChecked()): # only need to plot S2

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='b',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # need to plot S3 and S4

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=8,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        not self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # only need to plot S3

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=16,
                                              update=True)
        
        if self.parent.ui.decoder_display_selection_slave_group.isChecked() and \
        (not self.parent.ui.decoder_display_selection_slave_s3_check_box.isChecked() and \
        self.parent.ui.decoder_display_selection_slave_s4_check_box.isChecked()): # only need to plot S4

            # Update, respond and save robotically
            self.decoder_plot_science_robotic(module='slave',
                                              citiroc='a',
                                              channel_row=4,
                                              channel_column=4,
                                              channel_shift=0,
                                              update=True)

    ### decoder_start_end ###