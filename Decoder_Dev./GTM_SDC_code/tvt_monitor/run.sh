#!/bin/sh

nohup python sending_simulation.py &
sleep 2
nohup python decoding.py &
sleep 2
nohup ipython monitoring.ipy &
