#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 5 15:40 2023

@author: jasonpbu
"""

from PyQt5.QtWidgets import QFileDialog

from GTM_SDC_UI_Controller_Mtl_Cmd_Backend import *

from datetime import datetime, timedelta

class UiMtlCmd(object):

    start_time_flag = 0
    period_flag = 0
    mtl_orbits = ''
    mtl_days = ''
    mtl_hours = ''
    mtl_minutes = ''
    
    def __init__(self):
        pass
    
    ### mtl_cmd_link_interface ###

    def mtl_input_2le(self):

        # Get input file
        self.mtl_input_file, _ = QFileDialog.getOpenFileName(self, "Open file", "./")

        # Cache input file
        if len(self.mtl_input_file) != 0: # with input file
            self.mtl_cached_input_file = self.mtl_input_file

            # Print cached input file
            self.ui.mtl_input_2le_text.setText(self.mtl_cached_input_file)

            # Turn on relevant function and update it
            self.ui.mtl_conditions_group.setEnabled(True)
            self.mtl_conditions()

    def mtl_conditions(self):

        if self.ui.mtl_conditions_group.isEnabled():

            # Start time
            if self.ui.mtl_current_utc_radio_button.isChecked(): 
                self.start_time_flag = 1

            if self.ui.mtl_assign_utc_radio_button.isChecked(): 
                self.start_time_flag = 2
            self.assign_utc = self.ui.mtl_assign_utc_line.text()

            # Period
            if self.ui.mtl_orbits_radio_button.isChecked(): 
                self.period_flag = 1
            self.mtl_orbits = self.ui.mtl_orbits_line.text()

            if self.ui.mtl_days_radio_button.isChecked(): 
                self.period_flag = 2
            self.mtl_days = self.ui.mtl_days_line.text()

            if self.ui.mtl_hours_radio_button.isChecked(): 
                self.period_flag = 3
            self.mtl_hours = self.ui.mtl_hours_line.text()

            if self.ui.mtl_minutes_radio_button.isChecked(): 
                self.period_flag = 4
            self.mtl_minutes = self.ui.mtl_minutes_line.text()

            # SAA threshold
            if self.ui.mtl_saa_check_box.isChecked(): 
                self.saa_flag = 1
            else:
                self.saa_flag = 0
            self.saa = self.ui.mtl_saa_line.text()

            # Generate
            if ((self.start_time_flag == 1) or ((self.start_time_flag == 2) and (len(self.assign_utc) != 0))) and \
            (((self.period_flag == 1) and (len(self.mtl_orbits) != 0)) or ((self.period_flag == 2) and (len(self.mtl_days) != 0)) or \
             ((self.period_flag == 3) and (len(self.mtl_hours) != 0)) or((self.period_flag == 4) and (len(self.mtl_minutes) != 0))):
                self.ui.mtl_generate_button.setEnabled(True)
            else:
                self.ui.mtl_generate_button.setEnabled(False)
                self.ui.cmd_generate_button.setEnabled(False)

    ### mtl_cmd_link_interface_end ###

    ### mtl_cmd_run ###

    def mtl_generate(self):

        if self.start_time_flag == 1:
            self.mtl_start_utc = datetime.utcnow()
        if self.start_time_flag == 2:
            self.mtl_start_utc = datetime.strptime(self.assign_utc, '%Y-%m-%d %H:%M:%S')

        if self.period_flag == 1:
            self.period_mins = int(self.mtl_orbits) * 90
        if self.period_flag == 2:
            self.period_mins = int(self.mtl_days) * 24 *60
        if self.period_flag == 3:
            self.period_mins = int(self.mtl_hours) * 60
        if self.period_flag == 4:
            self.period_mins = int(self.mtl_minutes)
        
        self.mtl_start_utc_2digit_year = datetime.strftime(self.mtl_start_utc, '%y')
        self.mtl_end_utc = self.mtl_start_utc + timedelta(minutes=self.period_mins)

        self.tle = load_tle(self.mtl_input_file)
        self.times, self.orbit, self.is_sunlight, self.minutes, _ = \
        calculate_orbit_eclipse(self.tle, 
                                (self.mtl_start_utc.year,
                                 self.mtl_start_utc.month, 
                                 self.mtl_start_utc.day, 
                                 self.mtl_start_utc.hour, 
                                 self.mtl_start_utc.minute, 
                                 self.mtl_start_utc.second), 
                                 self.period_mins)
        self.saa, _ = circle_saa('df_for_contour.pkl', 200000)
        self.is_saa, _, _ = in_saa(self.times, self.saa, self.orbit)

        # Shift to relative value
        self.minutes = self.minutes - self.mtl_start_utc.minute

        self.need_minutes_idx_list = []
        for time_idx, time in enumerate(self.minutes):
            if self.is_sunlight[time_idx] == 0:
                if self.is_saa[time_idx] == 0:
                    self.need_minutes_idx_list.append(time_idx)

        self.need_minutes_idx_list_subgroup_end_idx = np.where(np.diff(self.need_minutes_idx_list)>1)[0]

        self.mtl_on_off_minutes_group = []
        for subgroup_end_idx_idx, subgroup_end_idx in enumerate(self.need_minutes_idx_list_subgroup_end_idx):

            if subgroup_end_idx_idx == 0:
                self.mtl_on_off_minutes_group.append(
                    self.minutes[self.need_minutes_idx_list[0]: self.need_minutes_idx_list[subgroup_end_idx]+1]
                )
                self.mtl_on_off_minutes_group.append(
                    self.minutes[self.need_minutes_idx_list[subgroup_end_idx+1]: self.need_minutes_idx_list[self.need_minutes_idx_list_subgroup_end_idx[subgroup_end_idx_idx+1]]+1]
                )

            elif subgroup_end_idx_idx == len(self.need_minutes_idx_list_subgroup_end_idx)-1:
               self.mtl_on_off_minutes_group.append(
                    self.minutes[self.need_minutes_idx_list[subgroup_end_idx+1]:self.need_minutes_idx_list[-1]+1]
                )

            else:
                self.mtl_on_off_minutes_group.append(
                    self.minutes[self.need_minutes_idx_list[subgroup_end_idx+1]: self.need_minutes_idx_list[self.need_minutes_idx_list_subgroup_end_idx[subgroup_end_idx_idx+1]]+1]
                )
        
        self.mtl_write_xml()

        self.ui.cmd_generate_button.setEnabled(True)
        
    def mtl_write_xml(self):

        generation_utc = datetime.utcnow()

        mtl_xml_head = f'''<?xml version="1.0" encoding="utf-8"?>
        <GTM_Mission_Timeline xsi:noNamespaceSchemaLocation="schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <header>
                <originator>SDC</originator>
                <destination>SOCC</destination>
                <satellite_name>FS8B</satellite_name>
                <generation_time>{generation_utc.year}-{str(generation_utc.month).zfill(2)}-{str(generation_utc.day).zfill(2)}T{str(generation_utc.hour).zfill(2)}:{str(generation_utc.minute).zfill(2)}:{str(generation_utc.second).zfill(2)}</generation_time>
                <file_name>FS8B_{self.mtl_start_utc.year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_timeline.xml</file_name>
                <instrument>GTM</instrument>
                <start_date>{self.mtl_start_utc.year}-{str(self.mtl_start_utc.month).zfill(2)}-{str(self.mtl_start_utc.day).zfill(2)}T{str(self.mtl_start_utc.hour).zfill(2)}:{str(self.mtl_start_utc.minute).zfill(2)}:{str(self.mtl_start_utc.second).zfill(2)}</start_date>
                <end_date>{self.mtl_end_utc.year}-{str(self.mtl_end_utc.month).zfill(2)}-{str(self.mtl_end_utc.day).zfill(2)}T{str(self.mtl_end_utc.hour).zfill(2)}:{str(self.mtl_end_utc.minute).zfill(2)}:{str(self.mtl_end_utc.second).zfill(2)}</end_date>
            </header>
            <body>
        '''

        mtl_xml_tail = f'''
            </body>
        </GTM_Mission_Timeline>
        '''

        with open(f'../level_0/import_mcc/FS8B_{self.mtl_start_utc.year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_timeline.xml', 'w', encoding='utf-8') as f:
            
            f.write(mtl_xml_head)

            for mtl_on_off_minutes_idx, mtl_on_off_minutes in enumerate(self.mtl_on_off_minutes_group):

                on_time = self.mtl_start_utc + timedelta(minutes=mtl_on_off_minutes[0])
                off_time = self.mtl_start_utc + timedelta(minutes=mtl_on_off_minutes[-1])

                mtl_xml_time_line_on = f'''
                        <time_line>
                            <UTC>{on_time.year}-{str(on_time.month).zfill(2)}-{str(on_time.day).zfill(2)}T{str(on_time.hour).zfill(2)}:{str(on_time.minute).zfill(2)}:{str(on_time.second).zfill(2)}</UTC>
                            <action>ADD</action>
                            <duration>00:00:00.20</duration>
                            <quaternion_1>NA</quaternion_1>
                            <quaternion_2>NA</quaternion_2>
                            <quaternion_3>NA</quaternion_3>
                            <quaternion_4>NA</quaternion_4>
                            <procedure_name>GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_ON.prc</procedure_name>
                        </time_line>
                '''

                mtl_xml_time_line_off = f'''
                        <time_line>
                            <UTC>{off_time.year}-{str(off_time.month).zfill(2)}-{str(off_time.day).zfill(2)}T{str(off_time.hour).zfill(2)}:{str(off_time.minute).zfill(2)}:{str(off_time.second).zfill(2)}</UTC>
                            <action>ADD</action>
                            <duration>00:00:00.10</duration>
                            <quaternion_1>NA</quaternion_1>
                            <quaternion_2>NA</quaternion_2>
                            <quaternion_3>NA</quaternion_3>
                            <quaternion_4>NA</quaternion_4>
                            <procedure_name>GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_OFF.prc</procedure_name>
                        </time_line>
                '''

                f.write(mtl_xml_time_line_on)
                f.write(mtl_xml_time_line_off)

            f.write(mtl_xml_tail)

    def cmd_generate(self):

        self.cmd_write_on_xml()
        self.cmd_write_off_xml()

        self.ui.mtl_generate_button.setEnabled(False)
        self.ui.cmd_generate_button.setEnabled(False)
    
    def cmd_write_on_xml(self):

        for mtl_on_off_minutes_idx, mtl_on_off_minutes in enumerate(self.mtl_on_off_minutes_group):

            generation_utc = datetime.utcnow()

            on_start_time = self.mtl_start_utc + timedelta(minutes=mtl_on_off_minutes[0])
            on_end_time = on_start_time + timedelta(seconds=20)

            cmd_xml_time_line_on = f'''<?xml version="1.0" encoding="utf-8"?>
            <GTM_Cmd_Procedure xsi:noNamespaceSchemaLocation="schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <originator>SDC</originator>
                    <destination>SOCC</destination>
                    <satellite_name>FS8B</satellite_name>
                    <generation_time>{generation_utc.year}-{str(generation_utc.month).zfill(2)}-{str(generation_utc.day).zfill(2)}T{str(generation_utc.hour).zfill(2)}:{str(generation_utc.minute).zfill(2)}:{str(generation_utc.second).zfill(2)}</generation_time>
                    <file_name>GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_ON.prc</file_name>
                    <instrument>GTM</instrument>
                    <start_date>{on_start_time.year}-{str(on_start_time.month).zfill(2)}-{str(on_start_time.day).zfill(2)}T{str(on_start_time.hour).zfill(2)}:{str(on_start_time.minute).zfill(2)}:{str(on_start_time.second).zfill(2)}</start_date>
                    <end_date>{on_end_time.year}-{str(on_end_time.month).zfill(2)}-{str(on_end_time.day).zfill(2)}T{str(on_end_time.hour).zfill(2)}:{str(on_end_time.minute).zfill(2)}:{str(on_end_time.second).zfill(2)}</end_date>
                </header>
                <body>
                    <procedure>
                        <time_tag>00:00:00.00</time_tag>
                        <symbol>-</symbol>
                        <description>Turn On GTM Payload</description>
                        <command>CSPEUBON</command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:05.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_1</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x36 0x00 0x0E 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_2</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x56 0x00 0x2E 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_3</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x77 0x00 0x4F 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_4</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x97 0x00 0x6F 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_5</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x52 0x01 0x02 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x00 0x00 0x00 0x00 0x62 0x62 0x00 0x03 \\
                            0x00 0x00 0x00 0xAC 0x00 0x7A 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_6</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x52 0x01 0x05 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x00 0x00 0x00 0x00 0x62 0x62 0x00 0x03 \\
                            0x00 0x00 0x00 0xA9 0x00 0x7A 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_7</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x55 0x01 0x02 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x00 0x00 0x00 0x00 0x62 0x62 0x00 0x03 \\
                            0x00 0x00 0x00 0xAB 0x00 0x7C 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_ON_PROC_8</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x55 0x01 0x05 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 0x11 \\
                            0x11 0x11 0x00 0x00 0x00 0x00 0x62 0x62 0x00 0x03 \\
                            0x00 0x00 0x00 0xAD 0x00 0x81 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                </body>
            </GTM_Cmd_Procedure>
            '''

            with open(f'../level_0/import_mcc/GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_ON.prc', 'w', encoding='utf-8') as f:

                f.write(cmd_xml_time_line_on)

    def cmd_write_off_xml(self):

        for mtl_on_off_minutes_idx, mtl_on_off_minutes in enumerate(self.mtl_on_off_minutes_group):

            generation_utc = datetime.utcnow()

            off_start_time = self.mtl_start_utc + timedelta(minutes=mtl_on_off_minutes[-1])
            off_end_time = off_start_time + timedelta(seconds=10)

            cmd_xml_time_line_off = f'''<?xml version="1.0" encoding="utf-8"?>
            <GTM_Cmd_Procedure xsi:noNamespaceSchemaLocation="schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <originator>SDC</originator>
                    <destination>SOCC</destination>
                    <satellite_name>FS8B</satellite_name>
                    <generation_time>{generation_utc.year}-{str(generation_utc.month).zfill(2)}-{str(generation_utc.day).zfill(2)}T{str(generation_utc.hour).zfill(2)}:{str(generation_utc.minute).zfill(2)}:{str(generation_utc.second).zfill(2)}</generation_time>
                    <file_name>GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_OFF.prc</file_name>
                    <instrument>GTM</instrument>
                    <start_date>{off_start_time.year}-{str(off_start_time.month).zfill(2)}-{str(off_start_time.day).zfill(2)}T{str(off_start_time.hour).zfill(2)}:{str(off_start_time.minute).zfill(2)}:{str(off_start_time.second).zfill(2)}</start_date>
                    <end_date>{off_end_time.year}-{str(off_end_time.month).zfill(2)}-{str(off_end_time.day).zfill(2)}T{str(off_end_time.hour).zfill(2)}:{str(off_end_time.minute).zfill(2)}:{str(off_end_time.second).zfill(2)}</end_date>
                </header>
                <body>
                    <procedure>
                        <time_tag>00:00:00.00</time_tag>
                        <symbol>-</symbol>
                        <description>GTM_OFF_PROC_1</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x97 0x00 0x6F 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_OFF_PROC_2</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x77 0x00 0x4F 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_OFF_PROC_3</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x56 0x00 0x2E 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>GTM_OFF_PROC_4</description>
                        <command>
                            GTM_CFG 0x55 0xAA 0x5F 0x01 0x5F 0x00 0x78 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 \\
                            0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0x77 0xFF \\
                            0xFF 0xFF 0xFF 0x22 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01 \\
                            0x01 0x01 0x01 0x01 0x01 0x01 0xFF 0xFF 0xFF 0xFF \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 \\
                            0x00 0x00 0x00 0x00 0x00 0x00 0xC2 0xC2 0x00 0x03 \\
                            0x00 0x00 0x00 0x36 0x00 0x0E 0xFB 0xF2
                        </command>
                        <src>MPQ</src>
                    </procedure>
                    <procedure>
                        <time_tag>00:00:02.00</time_tag>
                        <symbol>^</symbol>
                        <description>Turn Off GTM Payload</description>
                        <command>CSPEUBOFF</command>
                        <src>MPQ</src>
                    </procedure>
                </body>
            </GTM_Cmd_Procedure>
            '''

            with open(f'../level_0/import_mcc/GTM_PROC{self.mtl_start_utc_2digit_year}{str(self.mtl_start_utc.month).zfill(2)}{str(self.mtl_start_utc.day).zfill(2)}_{str(mtl_on_off_minutes_idx).zfill(2)}_OFF.prc', 'w', encoding='utf-8') as f:

                f.write(cmd_xml_time_line_off)

    ### mtl_cmd_run_end ###


