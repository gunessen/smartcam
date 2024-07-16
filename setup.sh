# Update the system
sudo apt update -y

# Install OpenCV for Linux from binaries (since it's faster)
sudo apt install libopencv-dev python3-opencv -y

sudo apt install python3-sqlalchemy python3-flask python3-flask-sqlalchemy python3-flask-cors python3-marshmallow python3-psutil -y

# python -m pip install SQLAlchemy==2.0.30
# python -m pip install Flask==3.0.3
# python -m pip install Flask-SQLAlchemy==3.1.1
# python -m pip install marshmallow==3.21.2
# python -m pip install Flask-Cors==4.0.1

# Needed for the tflite_runtime
sudo apt install python3-numpy libopenblas-dev python3-pip python3-venv -y

# python3 -m venv --system-site-packages ./.tflite_env
# source ./.tflite_env/bin/activate
# pip install tflite-runtime==2.14.0


# python3 -m venv ~/.smartcam
# source ~/.smartcam/bin/activate

pip install mailjet_rest==1.3.4