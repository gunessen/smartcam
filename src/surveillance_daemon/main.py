import os
import queue

# import sys
import threading
from datetime import UTC, datetime

# Add the src directory to the sys.path list
# sys.path.insert(0, os.path.abspath("../src"))
from db_models.init_db import create_tables
from services.event_service import add_event
from surveillance_daemon.motion_detector import MotionDetector
from surveillance_daemon.notification import Notification
from surveillance_daemon.object_detector import ObjectDetector
from surveillance_daemon.video_capture import VideoCapture
from surveillance_daemon.video_recorder import VideoRecorder

# import cv2


# Initialize the database session
create_tables()

# Initialize system components
object_detector = ObjectDetector(
    "../models/yolov7-tiny/yolov7-tiny.cfg",
    "../models/yolov7-tiny/yolov7-tiny.weights",
    "../data/coco.names",
)
motion_detector = MotionDetector()
notification = Notification(to_email="gunes314@gmail.com")

# Queue to store video paths to be processed
video_queue = queue.Queue()


def worker():
    """Worker thread that processes video files from the queue."""
    while True:
        print("Start object detection worker.")
        # Unpack the video information from the queue
        raw_video_path, video_length, event_time = video_queue.get()
        if raw_video_path is None:
            break

        # Perform object detection on the unannotated video
        detected_objects, video_path = object_detector.process_video(raw_video_path)
        print(video_path)

        # Add the event to the database
        add_event(video_path, detected_objects, event_time, video_length)

        # Remove the unannotated video
        os.remove(raw_video_path)

        # send a notification if an object is detected
        if detected_objects:
            notification.send(detected_objects)
        video_queue.task_done()


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

    with VideoCapture(device=0) as camera:
        while True:
            frame = camera.read_frame()
            if frame is None:
                break

            # font = cv2.FONT_HERSHEY_SIMPLEX
            # color = (0, 255, 0)

            # Detect motion and start recording video
            if motion_detector.detect_motion(frame):
                # cv2.putText(frame, "M", (10, 30), font, 0.5, color, 2)
                if not recording:
                    print("Start recording.")
                    recording = True
                    event_time = datetime.now(UTC)
                    video_recorder = VideoRecorder(
                        folder="/home/matrik/Yandex.Disk/CM3070_FP/code/videos",
                        fps=camera.get_fps(),
                        width=camera.get_frame_width(),
                        height=camera.get_frame_height(),
                    )

            # Record video for 5 seconds
            if recording:
                # cv2.putText(frame, "R", (30, 30), font, 0.5, color, 2)
                video_recorder.write_frame(frame)
                video_length = (datetime.now(UTC) - event_time).total_seconds()
                if video_length > 5:
                    print("Stop recording.")
                    # Start object detection on a separate thread when video recording stops
                    video_queue.put(
                        (video_recorder.get_video_path(), int(video_length), event_time)
                    )

                    # Clear the video recorder object
                    recording = False
                    video_recorder.release()
                    del video_recorder

            # cv2.imshow("Object detection", frame)
            # if cv2.waitKey(1) == 27:
            #     break

        # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
