#!/bin/bash

# IMPORTANT: Run this script by sourcing it (because it changes the environment):
# source setup_pc.sh

# Create a virtual environment
python3 -m venv ~/.smartcam
source ~/.smartcam/bin/activate

# Install OpenCV, ipykernel
python -m pip install opencv-python==4.10.0.84
python -m pip install ipykernel==6.29.5

# Install SQLAlchemy and
python -m pip install SQLAlchemy==2.0.30
python -m pip install Flask==3.0.3
python -m pip install Flask-SQLAlchemy==3.1.1
python -m pip install marshmallow==3.21.2
python -m pip install Flask-Cors==4.0.1

# Following are needed for yolov7 model conversion from pytorch to tflite
# https://mpolinowski.github.io/docs/IoT-and-Machine-Learning/ML/2023-01-14-yolov7_to_tensorflow/2023-01-14/
# python -m pip install torch torchaudio torchvision
# python -m pip install pandas requests tqdm yaml
# python -m pip install matplotlib seaborn scipy onnx
# python -m pip install onnx-tf 
# python -m pip install tensorflow-probability==0.23.0
# python -m pip install tensorflow==2.15.0
# python -m pip install tf_keras==2.15.0
# python -m pip install tensorflow-addons==0.23.0

# Find the slow parts of the code
# python -m pip install line_profiler

# install tflite-support for streamlined conversion of models to tflite
python -m pip install tflite-support==0.4.4


# Install formatter/linter/profiler (for development)
# python -m pip install black==24.4.2 
# python -m pip install flake8==6.1.0
# python -m pip install line-profiler==4.1.3

# Install SQLite
python -m pip install pysqlite3==0.5.3
python -m pip install pycocotools==2.0.8
