#!/bin/bash

remote_user=$1
remote_host=$2
remote_password=$3

arr_processing_import_mcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/processing_import_mcc.log))

arr_operation_import_mcc_need=()

# import mcc
arr_operation_import_mcc_need+=($remote_user)
arr_operation_import_mcc_need+=($remote_host)
arr_operation_import_mcc_need+=($remote_password)
for processing_import_mcc in "${arr_processing_import_mcc[@]}"
do
    if ! (grep -q $processing_import_mcc ../level_0/log/operation_import_mcc.log)
    then
        arr_operation_import_mcc_need+=($processing_import_mcc)
    fi
done

expect -f - -- "${arr_operation_import_mcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_import_mcc "/home/crab2/TASA/data/import_mcc\n"
set path_import_mcc_upload "../level_0/import_mcc\n"
set import_mcc_upload_log "../level_0/log/import_mcc_upload_to_operation.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_import_mcc"
expect "sftp>"
send "lcd $path_import_mcc_upload"
expect "sftp>"
log_file -a -noappend $import_mcc_upload_log
foreach arg [lrange $argv 3 end] {
    send "put $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

