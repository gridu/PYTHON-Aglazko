#!/bin/bash

# This script creates virtualenv and install needed dependencies
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
