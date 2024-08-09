#!/bin/bash

remote_user=$1
remote_host=$2
remote_password=$3

arr_operation_import_mcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/operation_import_mcc.log))
arr_operation_export_mcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/operation_export_mcc.log))
arr_operation_export_dcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/operation_export_dcc.log))

arr_operation_import_mcc_need=()
arr_operation_export_mcc_need=()
arr_operation_export_dcc_need=()

# import mcc
arr_operation_import_mcc_need+=($remote_user)
arr_operation_import_mcc_need+=($remote_host)
arr_operation_import_mcc_need+=($remote_password)
for operation_import_mcc in "${arr_operation_import_mcc[@]}"
do
    if ! (grep -q $operation_import_mcc ../level_0/log/processing_import_mcc.log)
    then
        arr_operation_import_mcc_need+=($operation_import_mcc)
    fi
done

expect -f - -- "${arr_operation_import_mcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_import_mcc "/home/crab2/TASA/data/import_mcc\n"
set path_import_mcc_download "../level_0/import_mcc\n"
set import_mcc_download_log "../level_0/log/import_mcc_download_from_operation.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_import_mcc"
expect "sftp>"
send "lcd $path_import_mcc_download"
expect "sftp>"
log_file -a -noappend $import_mcc_download_log
foreach arg [lrange $argv 3 end] {
    send "get $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

# export mcc
arr_operation_export_mcc_need+=($remote_user)
arr_operation_export_mcc_need+=($remote_host)
arr_operation_export_mcc_need+=($remote_password)
for operation_export_mcc in "${arr_operation_export_mcc[@]}"
do
    if ! (grep -q $operation_export_mcc ../level_0/log/processing_export_mcc.log)
    then
        arr_operation_export_mcc_need+=($operation_export_mcc)
    fi
done

expect -f - -- "${arr_operation_export_mcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_export_mcc "/home/crab2/TASA/data/export_mcc\n"
set path_export_mcc_download "../level_0/export_mcc\n"
set export_mcc_download_log "../level_0/log/export_mcc_download_from_operation.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_export_mcc"
expect "sftp>"
send "lcd $path_export_mcc_download"
expect "sftp>"
log_file -a -noappend $export_mcc_download_log
foreach arg [lrange $argv 3 end] {
    send "get $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

# export dcc
arr_operation_export_dcc_need+=($remote_user)
arr_operation_export_dcc_need+=($remote_host)
arr_operation_export_dcc_need+=($remote_password)
for operation_export_dcc in "${arr_operation_export_dcc[@]}"
do
    if ! (grep -q $operation_export_dcc ../level_0/log/processing_export_dcc.log)
    then
        arr_operation_export_dcc_need+=($operation_export_dcc)
    fi
done

expect -f - -- "${arr_operation_export_dcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_export_dcc "/home/crab2/TASA/data/export_dcc\n"
set path_export_dcc_download "../level_0/export_dcc\n"
set export_dcc_download_log "../level_0/log/export_dcc_download_from_operation.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_export_dcc"
expect "sftp>"
send "lcd $path_export_dcc_download"
expect "sftp>"
log_file -a -noappend $export_dcc_download_log
foreach arg [lrange $argv 3 end] {
    send "get $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF
