#!/bin/bash

# IMPORTANT: Run this script by sourcing it (because it changes the environment):
# source setup_pc.sh

# Create a virtual environment
python3 -m venv ~/.smartcam
source ~/.smartcam/bin/activate

# Install OpenCV
python -m pip install opencv-python==4.6.0.66

# Install SQLAlchemy and
python -m pip install SQLAlchemy==2.0.30
python -m pip install Flask==3.0.3
python -m pip install Flask-SQLAlchemy==3.1.1
python -m pip install marshmallow==3.21.2
python -m pip install Flask-Cors==4.0.1

# Install formatter/linter/profiler (for development)
# python -m pip install black==24.4.2 
# python -m pip install flake8==6.1.0
# python -m pip install line-profiler==4.1.3
