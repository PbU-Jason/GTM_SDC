#!/usr/bin/expect

log_user 0

set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]

set path_bash "/home/crab2/TASA\n"
set path_log "/home/crab2/TASA/log\n"

spawn ssh $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "$ "

send "cd $path_bash"
expect "$ "

send "./get_operation_log.sh\n"
expect "$ "

send "exit\n"

spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"

send "cd $path_log"
expect "sftp>"
send "lcd ../level_0/log/from_operation\n"
expect "sftp>"

# import mcc
send "get operation_import_mcc.log\n"
expect "sftp>"

# export mcc
send "get operation_export_mcc.log\n"
expect "sftp>"

# export dcc
send "get operation_export_dcc.log\n"
expect "sftp>"

send "exit\n"