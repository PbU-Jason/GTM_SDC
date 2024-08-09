#!/bin/bash

# import mcc
cd ../level_0/import_mcc/
ls -l > ../log/processing_import_mcc.log

# export mcc
cd ../export_mcc/
ls -l > ../log/processing_export_mcc.log

# export dcc
cd ../export_dcc/
ls -l > ../log/processing_export_dcc.log
