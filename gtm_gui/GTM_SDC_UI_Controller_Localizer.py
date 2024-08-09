#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 5 15:40 2023

@author: jasonpbu
"""

import os

import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog

from GTM_SDC_UI_Controller_Localizer_Find_Backend import *
from GTM_SDC_UI_Controller_Localizer_Localize_Backend import *

class UiLocalizer(object):
    
    def __init__(self):
        pass
    
    ### localizer_link_interface ###

    def find_input_file(self):

        # Get input file
        self.find_input_data, _ = QFileDialog.getOpenFileName(self, "Open file", "./")

        # Cache input file
        if len(self.find_input_data) != 0: # with input file
            self.find_cached_input_file = self.find_input_data

            # Print cached input file
            self.ui.find_input_file_text.setText(self.find_cached_input_file)

            # Turn on relevant function and update it
            self.ui.find_slice_time_group.setEnabled(True)
            self.ui.find_slice_energy_group.setEnabled(True)
            self.ui.find_preview_lc_button.setEnabled(True)
            self.ui.find_search_grb_button.setEnabled(True)
            self.find_slice()

    def find_slice(self):

        if self.ui.find_slice_time_group.isChecked():
            self.find_slice_time_flag = True
            self.find_slice_time_start = self.ui.find_slice_time_start_line.text()
            self.find_slice_time_end = self.ui.find_slice_time_end_line.text()
        else:
            self.find_slice_time_flag = False
        
        if self.ui.find_slice_energy_group.isChecked():
            self.find_slice_energy_flag = True
            self.find_slice_energy_min = self.ui.find_slice_energy_min_line.text()
            self.find_slice_energy_max = self.ui.find_slice_energy_max_line.text()
        else:
            self.find_slice_energy_flag = False

        if ((self.find_slice_time_flag == False) and (self.find_slice_energy_flag == False)) or \
            ((self.find_slice_time_flag == False) and (self.find_slice_energy_flag == True) and (len(self.find_slice_energy_min) != 0) and (len(self.find_slice_energy_max) != 0)) or \
            ((self.find_slice_time_flag == True) and (len(self.find_slice_time_start) != 0) and (len(self.find_slice_time_end) != 0) and (self.find_slice_energy_flag == False)) or \
            ((self.find_slice_time_flag == True) and (len(self.find_slice_time_start) != 0) and (len(self.find_slice_time_end) != 0) and (self.find_slice_energy_flag == True) and (len(self.find_slice_energy_min) != 0) and (len(self.find_slice_energy_max) != 0)):
            self.ui.find_preview_lc_button.setEnabled(True)
            self.ui.find_search_grb_button.setEnabled(True)
        else:
            self.ui.find_preview_lc_button.setEnabled(False)
            self.ui.find_search_grb_button.setEnabled(False)
            
    def localize_input_file(self):

        # Get input file
        self.localize_input_data, _ = QFileDialog.getOpenFileName(self, "Open file", "./")

        # Cache input file
        if len(self.localize_input_data) != 0: # with input file
            self.localize_cached_input_file = self.localize_input_data

            # Print cached input file
            self.ui.localize_input_file_text.setText(self.localize_cached_input_file)

            # Turn on relevant function
            self.ui.localize_grb_button.setEnabled(True)
            
    ### localizer_link_interface_end ###

    ### localizer_run ###

    def find_preview(self):

        if self.ui.find_slice_time_group.isChecked():
            self.find_df_temp = csv2df(self.find_cached_input_file)
            self.find_df = slice_GTI(self.find_df_temp, int(self.find_slice_time_start), int(self.find_slice_time_end))
        else:
            self.find_df = csv2df(self.find_cached_input_file)
        
        self.find_open_preview_window()

        self.find_df_grouped = self.find_df.groupby(['GTM ID'])

        self.find_plot_preview(self.find_df_grouped.get_group((0)), self.find_df_grouped.get_group((1)))

    def find_open_preview_window(self):

        # Create layout to hold multiple subplot
        self.find_preview_pg_layout = pg.GraphicsLayoutWidget(title='Preview')
        self.find_preview_pg_layout.showMaximized()
        self.find_preview_pg_layout.setBackground('w')
    
    def find_plot_preview(self, df_master, df_slave):
            
        # Add subplot
        self.find_preview_pg_layout_master \
        = self.find_preview_pg_layout.addPlot(row=0,
                                            col=0, 
                                            title='Master Light Curve (bin = 1s)', 
                                            labels={'left': 'Count [#/bin]', 'bottom': 'Time [s]'})
        self.find_preview_pg_layout_slave \
        = self.find_preview_pg_layout.addPlot(row=0, 
                                            col=1, 
                                            title='Slave Light Curve (bin = 1s)', 
                                            labels={'left': 'Count [#/bin]', 'bottom': 'Time [s]'})

        # Bin data
        self.find_df_master_hist, self.find_df_master_bin_edges = \
        np.histogram(
            df_master['Relative Time'], 
            bins=np.arange(
                int(np.min(df_master['Relative Time'])), 
                int(np.max(df_master['Relative Time']))+1, 
                1), 
            density=False)
        self.find_df_slave_hist, self.find_df_slave_bin_edges = \
        np.histogram(
            df_slave['Relative Time'], 
            bins=np.arange(
                int(np.min(df_slave['Relative Time'])), 
                int(np.max(df_slave['Relative Time']))+1, 
                1), 
            density=False)

        # Plot
        self.find_preview_pg_layout_master_line \
        = self.find_preview_pg_layout_master.plot(self.find_df_master_bin_edges[:-1], 
                                                self.find_df_master_hist, 
                                                pen=pg.mkPen(color=(255, 0, 0), width=3))
        self.find_preview_pg_layout_slave_line \
        = self.find_preview_pg_layout_slave.plot(self.find_df_slave_bin_edges[:-1], 
                                                self.find_df_slave_hist, 
                                                pen=pg.mkPen(color=(0, 0, 255), width=3))
    
    def find_search(self):

        plt.style.use('default')

        if self.ui.find_slice_time_group.isChecked():
            self.find_df_temp = csv2df(self.find_cached_input_file)
            self.find_df = slice_GTI(self.find_df_temp, int(self.find_slice_time_start), int(self.find_slice_time_end))
        else:
            self.find_df = csv2df(self.find_cached_input_file)

        # Collect data from M, M1~4, S & S1~4
        self.find_df_list, self.find_df_name_list = split_df(self.find_df)

        # Find trigger and report trigger & end time
        self.trigger_time, self.end_time = \
        find_trigger(os.path.basename(self.find_cached_input_file),
                     self.find_df, self.find_df_list, self.find_df_name_list, 
                     bin_size_list=[0.001, 0.002, 0.005 ,0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10],
                     ) 

        if self.trigger_time != None:
            
            # Visualize light cureve using best binsize and calculate time info. by best case name
            data_with_grb_start_time, data_with_grb_end_time, best_bin_edges, t05, t25, t75, t95, t50, t90 = \
            find_time_info(os.path.basename(self.find_cached_input_file),
                           self.find_df_list, self.find_df_name_list,
                           self.trigger_time, self.end_time,
                           best_bin_size=1, 
                           best_case_name='Slave',
                           )
            
            df_output = report_trigger_info(os.path.basename(self.find_cached_input_file),
                                            self.find_df_list, self.find_df_name_list,
                                            self.trigger_time, data_with_grb_start_time, data_with_grb_end_time,
                                            t05, t25, t75, t95, t50, t90,
                                            best_bin_edges,
                                            best_bin_size=1,
                                            )
            print('==============================')
            print('Can start to localize GRB!')
    
    def localize_start(self):

        plt.style.use('dark_background')

        localize_grb(self.localize_cached_input_file)
    
    ### localizer_run_end ###


