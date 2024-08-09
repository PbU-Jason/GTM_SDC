#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 4 11:32 2023

@author: jasonpbu
"""

from subprocess import Popen

class UiFlow(object):

    operation_user_flag = False
    operation_host_flag = False
    operation_password_flag = False
    archiving_user_flag = False
    archiving_host_flag = False
    archiving_password_flag = False
    
    def __init__(self):
        pass
    
    ### flow_link_interface ###

    def flow_operation_user(self):

        self.operation_user = self.ui.flow_operation_user_line.text()

        if len(self.operation_user) == 0:
            self.operation_user_flag = False
        else:
            self.operation_user_flag = True
        
        self.flow_socc_operation_processing()

    def flow_operation_host(self):

        self.operation_host = self.ui.flow_operation_host_line.text()

        if len(self.operation_host) == 0:
            self.operation_host_flag = False
        else:
            self.operation_host_flag = True
        
        self.flow_socc_operation_processing()

    def flow_operation_password(self):

        self.operation_password = self.ui.flow_operation_password_line.text()

        if len(self.operation_password) == 0:
            self.operation_password_flag = False
        else:
            self.operation_password_flag = True
        
        self.flow_socc_operation_processing()        

    def flow_socc_operation_processing(self):

        if self.operation_user_flag and self.operation_host_flag and self.operation_password_flag:
            self.ui.flow_socc_operation_group.setEnabled(True)
            self.ui.flow_operation_processing_group.setEnabled(True)
        else:
            self.ui.flow_socc_operation_group.setEnabled(False)
            self.ui.flow_operation_processing_group.setEnabled(False)
    
    def flow_archiving_user(self):

        self.archiving_user = self.ui.flow_archiving_user_line.text()

        if len(self.archiving_user) == 0:
            self.archiving_user_flag = False
        else:
            self.archiving_user_flag = True
        
        self.flow_processing_archiving()

    def flow_archiving_host(self):

        self.archiving_host = self.ui.flow_archiving_host_line.text()

        if len(self.archiving_host) == 0:
            self.archiving_host_flag = False
        else:
            self.archiving_host_flag = True
        
        self.flow_processing_archiving()

    def flow_archiving_password(self):

        self.archiving_password = self.ui.flow_archiving_password_line.text()

        if len(self.archiving_password) == 0:
            self.archiving_password_flag = False
        else:
            self.archiving_password_flag = True
        
        self.flow_processing_archiving()        

    def flow_processing_archiving(self):

        if self.archiving_user_flag and self.archiving_host_flag and self.archiving_password_flag:
            self.ui.flow_processing_archiving_group.setEnabled(True)
        else:
            self.ui.flow_processing_archiving_group.setEnabled(False)
    
    ### flow_link_interface_end ###

    ### flow_run ###

    def flow_socc_operation_update_socc(self):
        Popen(['./run_get_socc_log.sh', self.operation_user, self.operation_host, self.operation_password])
    def flow_socc_operation_update_operation(self):
        Popen(['./run_get_operation_log.sh', self.operation_user, self.operation_host, self.operation_password])
    def flow_socc_operation_clone(self):
        Popen(['./run_download_from_socc.sh', self.operation_user, self.operation_host, self.operation_password])
    def flow_socc_operation_push(self):
        Popen(['./run_upload_to_socc.sh', self.operation_user, self.operation_host, self.operation_password])

    def flow_operation_processing_update_operation(self):
        Popen(['./get_operation_log.sh', self.operation_user, self.operation_host, self.operation_password])
    def flow_operation_processing_update_processing(self):
        Popen('./get_processing_log.sh')
    def flow_operation_processing_clone(self):
        Popen(['./download_from_operation.sh', self.operation_user, self.operation_host, self.operation_password])
    def flow_operation_processing_push(self):
        Popen(['./upload_to_operation.sh', self.operation_user, self.operation_host, self.operation_password])

    def flow_processing_archiving_update_processing(self):
        Popen('./archive_get_all_processing_log.sh')
    def flow_processing_archiving_update_archiving(self):
        Popen(['./archive_get_all_archiving_log.sh', self.archiving_user, self.archiving_host, self.archiving_password])
    def flow_processing_archiving_push(self):
        Popen(['./archive_upload_to_archiving.sh', self.archiving_user, self.archiving_host, self.archiving_password])


    ### flow_run_end ###


