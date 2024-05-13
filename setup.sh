# Update the system
sudo apt update -y

# Install OpenCV for Linux from binaries (since it's faster)
sudo apt install libopencv-dev python3-opencv -y

python3 -m venv ~/.smartcam
source ~/.smartcam/bin/activate
