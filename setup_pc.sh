#!/bin/bash

# IMPORTANT: Run this script by sourcing it:
# source setup_pc.sh

# Create a virtual environment
python3 -m venv ~/.smartcam
source ~/.smartcam/bin/activate

# Install OpenCV
python -m pip install opencv-python==4.6.0.66

# Install SQLAlchemy
python -m pip install SQLAlchemy==2.0.30

# Install formatter/linter
python -m pip install black==24.4.2 
python -m pip install flake8==6.1.0
# python -m pip install line-profiler==4.1.3
