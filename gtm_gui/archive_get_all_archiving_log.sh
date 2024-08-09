#!/usr/bin/expect

log_user 0

set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]

set path_import_mcc "/home/gtm/archive/level_0/import_mcc\n"
set path_export_mcc "/home/gtm/archive/level_0/export_mcc\n"
set path_export_dcc "/home/gtm/archive/level_0/export_dcc\n"
set path_level_1 "/home/gtm/archive/level_1\n"
set path_level_2 "/home/gtm/archive/level_2\n"

set log_import_mcc "../level_0/log/to_archiving/archiving_import_mcc.log"
set log_export_mcc "../level_0/log/to_archiving/archiving_export_mcc.log"
set log_export_dcc "../level_0/log/to_archiving/archiving_export_dcc.log"
set log_level_1 "../level_0/log/to_archiving/archiving_level_1.log"
set log_level_2 "../level_0/log/to_archiving/archiving_level_2.log"

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

# level 1
send "cd $path_level_1"
expect "sftp>"

log_file -a -noappend $log_level_1
send "ls -l\n"
expect "sftp>"
log_file

# level 2
send "cd $path_level_2"
expect "sftp>"

log_file -a -noappend $log_level_2
send "ls -l\n"
expect "sftp>"
log_file

send "exit\n"
