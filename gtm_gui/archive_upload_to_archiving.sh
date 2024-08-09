#!/bin/bash

remote_user=$1
remote_host=$2
remote_password=$3

arr_processing_import_mcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/to_archiving/processing_import_mcc.log))
arr_processing_export_mcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/to_archiving/processing_export_mcc.log))
arr_processing_export_dcc=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/to_archiving/processing_export_dcc.log))
arr_processing_level_1=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/to_archiving/processing_level_1.log))
arr_processing_level_2=($(awk -F ' ' '{sub(/\r$/, "", $9); print $9}' ../level_0/log/to_archiving/processing_level_2.log))

arr_archiving_import_mcc_need=()
arr_archiving_export_mcc_need=()
arr_archiving_export_dcc_need=()
arr_archiving_level_1_need=()
arr_archiving_level_2_need=()

# import mcc
arr_archiving_import_mcc_need+=($remote_user)
arr_archiving_import_mcc_need+=($remote_host)
arr_archiving_import_mcc_need+=($remote_password)
for processing_import_mcc in "${arr_processing_import_mcc[@]}"
do
    if ! (grep -q $processing_import_mcc ../level_0/log/to_archiving/archiving_import_mcc.log)
    then
        arr_archiving_import_mcc_need+=($processing_import_mcc)
    fi
done

expect -f - -- "${arr_archiving_import_mcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_import_mcc "/home/gtm/archive/level_0/import_mcc\n"
set path_import_mcc_upload "../level_0/import_mcc\n"
set import_mcc_upload_log "../level_0/log/to_archiving/import_mcc_upload_to_archiving.log"
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

# export mcc
arr_archiving_export_mcc_need+=($remote_user)
arr_archiving_export_mcc_need+=($remote_host)
arr_archiving_export_mcc_need+=($remote_password)
for processing_export_mcc in "${arr_processing_export_mcc[@]}"
do
    if ! (grep -q $processing_export_mcc ../level_0/log/to_archiving/archiving_export_mcc.log)
    then
        arr_archiving_export_mcc_need+=($processing_export_mcc)
    fi
done

expect -f - -- "${arr_archiving_export_mcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_export_mcc "/home/gtm/archive/level_0/export_mcc\n"
set path_export_mcc_upload "../level_0/export_mcc\n"
set export_mcc_upload_log "../level_0/log/to_archiving/export_mcc_upload_to_archiving.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_export_mcc"
expect "sftp>"
send "lcd $path_export_mcc_upload"
expect "sftp>"
log_file -a -noappend $export_mcc_upload_log
foreach arg [lrange $argv 3 end] {
    send "put $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

# export dcc
arr_archiving_export_dcc_need+=($remote_user)
arr_archiving_export_dcc_need+=($remote_host)
arr_archiving_export_dcc_need+=($remote_password)
for processing_export_dcc in "${arr_processing_export_dcc[@]}"
do
    if ! (grep -q $processing_export_dcc ../level_0/log/to_archiving/archiving_export_dcc.log)
    then
        arr_archiving_export_dcc_need+=($processing_export_dcc)
    fi
done

expect -f - -- "${arr_archiving_export_dcc_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_export_dcc "/home/gtm/archive/level_0/export_dcc\n"
set path_export_dcc_upload "../level_0/export_dcc\n"
set export_dcc_upload_log "../level_0/log/to_archiving/export_dcc_upload_to_archiving.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_export_dcc"
expect "sftp>"
send "lcd $path_export_dcc_upload"
expect "sftp>"
log_file -a -noappend $export_dcc_upload_log
foreach arg [lrange $argv 3 end] {
    send "put $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

# level 1
arr_archiving_level_1_need+=($remote_user)
arr_archiving_level_1_need+=($remote_host)
arr_archiving_level_1_need+=($remote_password)
for processing_level_1 in "${arr_processing_level_1[@]}"
do
    if ! (grep -q $processing_level_1 ../level_0/log/to_archiving/archiving_level_1.log)
    then
        arr_archiving_level_1_need+=($processing_level_1)
    fi
done

expect -f - -- "${arr_archiving_level_1_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_level_1 "/home/gtm/archive/level_1\n"
set path_level_1_upload "../level_1\n"
set level_1_upload_log "../level_0/log/to_archiving/level_1_upload_to_archiving.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_level_1"
expect "sftp>"
send "lcd $path_level_1_upload"
expect "sftp>"
log_file -a -noappend $level_1_upload_log
foreach arg [lrange $argv 3 end] {
    send "put $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

# level 2
arr_archiving_level_2_need+=($remote_user)
arr_archiving_level_2_need+=($remote_host)
arr_archiving_level_2_need+=($remote_password)
for processing_level_2 in "${arr_processing_level_2[@]}"
do
    if ! (grep -q $processing_level_2 ../level_0/log/to_archiving/archiving_level_2.log)
    then
        arr_archiving_level_2_need+=($processing_level_2)
    fi
done

expect -f - -- "${arr_archiving_level_2_need[@]}" <<'EOF'
log_user 0
set remote_user [lindex $argv 0]
set remote_host [lindex $argv 1]
set remote_password [lindex $argv 2]
set path_level_2 "/home/gtm/archive/level_2\n"
set path_level_2_upload "../level_2\n"
set level_2_upload_log "../level_0/log/to_archiving/level_2_upload_to_archiving.log"
spawn sftp $remote_user@$remote_host
expect "password:"
send "$remote_password\n"
expect "sftp>"
send "cd $path_level_2"
expect "sftp>"
send "lcd $path_level_2_upload"
expect "sftp>"
log_file -a -noappend $level_2_upload_log
foreach arg [lrange $argv 3 end] {
    send "put $arg\n"
    expect "sftp>"
}
log_file
send "exit\n"
EOF

