#!/bin/bash
set -e
python3 startup.py
sleep 5s
clear
python3 run.py
clear
echo "Process was exited."
