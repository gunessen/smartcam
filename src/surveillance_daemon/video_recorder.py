import os
from datetime import datetime

import cv2


class VideoRecorder:
    """Class to record video of the environment."""

    def __init__(
        self, codec="XVID", extension="avi", folder="videos", width=800, height=600, fps=15
    ):
        """
        Create the video directory and initialize the video recorder with the specified codec,
        resolution, and FPS.
        """
        os.makedirs(folder, exist_ok=True)
        self.output_path = (
            f"{folder}/{datetime.now().strftime('%Y-%m-%dT%H:%M:%S').replace(' ', '')}.{extension}"
        )
        self.out = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*codec),
            fps,
            (int(width), int(height)),
        )

    def write_frame(self, frame):
        """Write a frame to the video."""
        self.out.write(frame)

    def release(self):
        """Release the video."""
        self.out.release()

    def get_video_path(self):
        """Get the path to the video."""
        return self.output_path
