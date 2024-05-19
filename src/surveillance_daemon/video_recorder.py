import os
import queue
import threading
from datetime import UTC, datetime

import cv2


class VideoRecorder:
    """Class to record video of the environment."""

    def __init__(
        self, codec="MJPG", extension="avi", folder="videos", width=800, height=600, fps=10
    ):
        """
        Create the video directory and initialize the video recorder with the specified codec,
        resolution, and FPS. Frames are written to the video using a separate thread because
        writing frames can be time-consuming due to slow disk I/O on the Raspberry Pi.
        """
        os.makedirs(folder, exist_ok=True)
        date_string = f"{folder}/{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S').replace(' ', '')}"
        self.output_path = f"{date_string}_unannotated.{extension}"
        self.out = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*codec),
            fps,
            (int(width), int(height)),
        )

        # Initialize the frame queue and start the recording thread
        self.frame_queue = queue.Queue()
        self.recording = False
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._write_frames)
        self.thread.start()

    def _write_frames(self):
        """Processing loop to write frames to the video from the queue."""
        while not self.stop_event.is_set():
            try:
                frame = self.frame_queue.get(timeout=0.1)
                print(f"Writing frame to the video: {self.output_path}")
                self.out.write(frame)
            except queue.Empty:
                continue

    def write_frame(self, frame):
        """Write a frame to the video."""
        if self.recording:
            print("Adding frame to the queue")
            self.frame_queue.put(frame)

    def release(self):
        """Release the video."""
        # Send the stop event to the thread and wait for it to finish
        self.stop_event.set()
        self.thread.join()

        # Process any remaining frames in the queue
        while not self.frame_queue.empty():
            frame = self.frame_queue.get()
            self.out.write(frame)

        self.out.release()
        print(f"Released the video: {self.output_path}")

    def get_video_path(self):
        """Get the path to the video."""
        return self.output_path

    def start_recording(self):
        """Start recording video."""
        self.recording = True

    def stop_recording(self):
        """Stop recording video."""
        self.recording = False
