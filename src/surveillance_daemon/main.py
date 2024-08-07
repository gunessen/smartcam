import logging
import os
import queue
import threading
from datetime import UTC, datetime

from object_detector import ModelConfig, ObjectDetector

from db_models.base import create_tables
from services.event_service import add_event
from services.settings_service import get_settings
from surveillance_daemon.motion_detector import MotionDetector
from surveillance_daemon.notification import Notification
from surveillance_daemon.video_capture import VideoCapture
from surveillance_daemon.video_recorder import VideoRecorder

# Initialize settings
settings = get_settings()

# Initialize the database session
create_tables()

current_model = ModelConfig.get_config(settings["object_detection_model"])
object_detector = ObjectDetector(
    model_path=current_model["model_path"],
    input_width=current_model["input_width"],
    input_height=current_model["input_height"],
    classes_path=current_model["classes_path"],
    is_yolo=current_model["is_yolo"],
    num_threads=4,
)
motion_detector = MotionDetector()
notification = Notification(
    mailjet_api_key=settings["mailjet_api_key"], mailjet_secret_key=settings["mailjet_secret_key"]
)

# Queue to store video paths to be processed
unannotated_video_queue = queue.Queue()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def worker():
    """Worker thread that processes video files from the queue."""
    while True:
        logger.info("Start object detection worker.")
        # Unpack the video information from the queue
        raw_video_path, video_length, event_time = unannotated_video_queue.get()

        # Break the loop if the raw_video_path is None
        if raw_video_path is None:
            # Indicate that the task is done before breaking
            unannotated_video_queue.task_done()
            break

        # Perform object detection on the unannotated video
        detected_objects, video_path, _ = object_detector.process_video(
            in_video_path=raw_video_path, store_out_video=True
        )
        logger.info(f"Processed video: {video_path}")

        # Remove the unannotated video
        os.remove(raw_video_path)

        # Add the event to the database and send a notification
        if detected_objects:
            logger.info(f"Detected objects: {detected_objects}")
            add_event(video_path, detected_objects, event_time, video_length)
            if int(settings["notifications_active"]) == 1:
                notification.send(detected_objects)
        else:
            logger.info("No objects detected, deleting video.")
            os.remove(video_path)

        # Indicate that the task is done
        unannotated_video_queue.task_done()


def stop_workers():
    """Stop worker threads gracefully"""
    # Add None to the queue to signal the worker to exit
    for _ in range(num_worker_threads):
        unannotated_video_queue.put(None)
    # Wait for all threads to finish
    for t in threads:
        t.join()


# Create and start the worker thread
num_worker_threads = 1
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)


def main():
    recording = False
    event_time = None

    camera_width = int(settings["camera_resolution"].split("x")[0])
    camera_height = int(settings["camera_resolution"].split("x")[1])
    camera_fps = int(settings["camera_fps"])

    # Start the camera
    with VideoCapture(device=0, width=camera_width, height=camera_height, fps=camera_fps) as camera:
        # Frame processing loop
        while True:
            # Read the frame from the camera
            frame = camera.read_frame()

            # Break the loop if the frame is None
            if frame is None:
                break

            # Detect motion and start recording video
            if motion_detector.detect_motion(frame):
                if not recording:
                    logger.info("Start recording.")
                    recording = True
                    event_time = datetime.now(UTC)
                    video_recorder = VideoRecorder(
                        folder=os.path.join(
                            os.path.abspath(
                                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                            ),
                            "videos",
                        ),
                        fps=camera.get_fps(),
                        width=camera.get_frame_width(),
                        height=camera.get_frame_height(),
                    )
                    video_recorder.start_recording()

            # Record video for 5 seconds
            if recording:
                video_recorder.write_frame(frame)
                video_length = (datetime.now(UTC) - event_time).total_seconds()
                if video_length > int(settings["recording_length"]):
                    logger.info("Stop recording.")
                    video_recorder.stop_recording()
                    # Start object detection on a separate thread when video recording stops
                    unannotated_video_queue.put(
                        (video_recorder.get_video_path(), int(video_length), event_time)
                    )

                    # Clear the video recorder object
                    recording = False
                    video_recorder.release()
                    del video_recorder


if __name__ == "__main__":
    try:
        main()
    finally:
        stop_workers()
        logger.info("Exiting surveillance daemon.")
