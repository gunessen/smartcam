import cv2
from flask import Blueprint, Response

from surveillance_daemon.video_capture import VideoCapture

livefeed_bp = Blueprint("livefeed", __name__)

camera = None


def generate_frames():
    global camera
    with VideoCapture(device=0) as camera_instance:
        camera = camera_instance
        while True:
            frame = camera.read_frame()
            if frame is None:
                break

            # Encode the frame as a JPEG image
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            # Generate parts of a multipart response that consists of video frames encoded as JPEG
            # images. This is known as motion JPEG (M-JPEG).
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@livefeed_bp.route("/api/v1/livefeed", methods=["GET"])
def livefeed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@livefeed_bp.route("/api/v1/livefeed/stop", methods=["POST"])
def stop_livefeed():
    """Stop the live feed and release the camera."""
    global camera
    if camera:
        camera.release()
        camera = None
    return "", 204
