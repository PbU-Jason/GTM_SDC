#!/usr/bin/expect

log_user 0

set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]

set path_import_mcc "/home/crab2/TASA/data/import_mcc\n"
set path_export_mcc "/home/crab2/TASA/data/export_mcc\n"
set path_export_dcc "/home/crab2/TASA/data/export_dcc\n"

set log_import_mcc "../level_0/log/operation_import_mcc.log"
set log_export_mcc "../level_0/log/operation_export_mcc.log"
set log_export_dcc "../level_0/log/operation_export_dcc.log"

spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"

# import mcc
send "cd $path_import_mcc"
expect "sftp>"

log_file -a -noappend $log_import_mcc
send "ls -l\n"
expect "sftp>"
log_file

# export mcc
send "cd $path_export_mcc"
expect "sftp>"

log_file -a -noappend $log_export_mcc
send "ls -l\n"
expect "sftp>"
log_file

# export dcc
send "cd $path_export_dcc"
expect "sftp>"

log_file -a -noappend $log_export_dcc
send "ls -l\n"
expect "sftp>"
log_file

send "exit\n"
