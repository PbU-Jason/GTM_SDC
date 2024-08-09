#!/bin/bash

# import mcc
cd ../level_0/import_mcc/
ls -l > ../log/to_archiving/processing_import_mcc.log

# export mcc
cd ../export_mcc/
ls -l > ../log/to_archiving/processing_export_mcc.log

# export dcc
cd ../export_dcc/
ls -l > ../log/to_archiving/processing_export_dcc.log

# level_1
cd ../../level_1/
ls -l > ../level_0/log/to_archiving/processing_level_1.log

# level_2
cd ../level_2/
ls -l > ../level_0/log/to_archiving/processing_level_2.log

