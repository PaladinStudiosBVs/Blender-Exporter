#!/bin/bash
python3 create_virtualenv.py
source ./venv/bin/activate
./venv/bin/python -m pip install fake-bpy-module-3.4
read -n1 -r -p "Press any key to continue..." key