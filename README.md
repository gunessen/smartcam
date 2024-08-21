# SmartCam - Home Security Camera System

**SmartCam** is a lightweight, open-source home security camera system designed to run efficiently on low-power devices such as the Raspberry Pi Zero 2 W. The system is built for privacy-conscious residential users who require a simple, cost-effective, and robust surveillance solution.

SmartCam offers local processing of video feeds, advanced object detection using efficient models like YOLO Tiny, MobileNetV3, and EfficientDet Lite, and provides a user-friendly interface for configuration and monitoring through a web dashboard. The project is designed to work out of the box without needing advanced technical skills, making it accessible to a broad range of users.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Privacy-Focused**: All video processing is performed locally on the device, ensuring complete control over your data.
- **Low Power Consumption**: Optimized for devices like Raspberry Pi Zero 2 W, making it energy-efficient and suitable for 24/7 operation.
- **Advanced Object Detection**: Uses lightweight models (YOLO Tiny, MobileNetV3, EfficientDet Lite) optimized for real-time detection on low-spec hardware.
- **User-Friendly Web Interface**: Configurable settings, live feed monitoring, event management, and system statistics accessible through an intuitive web dashboard.
- **Modular Design**: Easily extendable architecture for adding new features or integrating additional detection models.
- **Email Notifications**: Real-time alerts when specific objects (e.g., people, pets) are detected, using MailJet as the email service.

## System Architecture

The system architecture follows a modular approach:

1. **Web Application**: Built with React.js (frontend) and Flask (backend), offering a clean, intuitive UI with support for configuration and monitoring.
2. **Surveillance Daemon**: Handles video capture, motion detection, object detection, and recording. Uses OpenCV and TensorFlow Lite for efficient video processing.
3. **Database Management**: SQLite is used for lightweight data storage, managed through SQLAlchemy ORM for seamless backend interactions.
4. **Notification Module**: Sends real-time email alerts based on detected events using the MailJet API.

## Technologies Used

- **Frontend**: React.js, Chakra UI
- **Backend**: Flask, SQLAlchemy, SQLite
- **Object Detection Models**: YOLO Tiny, MobileNetV3, EfficientDet Lite (via TensorFlow Lite)
- **Video Processing**: OpenCV
- **Notification Service**: MailJet API

## Installation

### Prerequisites

- Raspberry Pi Zero 2 W (or compatible device)
- Raspberry Pi OS Lite
- Python 3.7+
- Camera module compatible with Raspberry Pi (e.g., IMX335 sensor)

### Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/gunessen/smartcam.git
    cd smartcam
    ```

2. Install dependencies:
    ```bash
    sudo apt update -y
    sudo apt install libopencv-dev python3-opencv -y
    sudo apt install python3-sqlalchemy python3-flask python3-flask-sqlalchemy python3-flask-cors python3-marshmallow python3-psutil -y
    sudo apt install python3-numpy libopenblas-dev python3-pip python3-venv -y
    pip install mailjet_rest==1.3.4
    ```

3. Start the backend server:
    ```bash
    make start_prod
    ```

4. Start the surveillance daemon:
    ```bash
    make start_daemon
    ```

5. Access the web interface at `http://<your-pi-ip>:5000` in your browser.

## Configuration

- Configuration options are accessible via the web interface under the "Settings" menu.
- You can adjust motion detection sensitivity, object detection models, video quality, and notification settings.

## Usage

- **Login**: Access the system via the login page using your credentials.
- **Dashboard**: View system status, recent events, and system health metrics.
- **Live Feed**: Monitor real-time video from your camera.
- **Events**: Review recorded events, manage recordings, and delete old footage.
- **System Info**: Monitor CPU/RAM usage, storage availability, and other stats.
- **Notifications**: Configure alerts for detected objects.

## Directory Structure

```plaintext
smartcam/
├── data/                  # Data files (e.g., model label files)
├── keys/                  # SSH keys for secure access
├── models/                # Pretrained models for object detection
├── notebooks/             # Jupyter notebooks for evaluation and experiments
├── src/                   # Main application code
│   ├── backend/           # Flask API and backend logic
│   ├── db_models/         # Database models and initialization scripts
│   ├── evaluation/        # Scripts for model evaluation
│   ├── frontend/          # React.js frontend code
│   ├── services/          # Backend services and utilities
│   └── surveillance_daemon/  # Surveillance daemon handling video capture and detection
└── README.md              # Project readme
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with detailed information on your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
