import datetime
import os

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
        self.out = cv2.VideoWriter(
            f"{folder}/{datetime.datetime.now().isoformat().replace(' ', '')}.{extension}",
            cv2.VideoWriter_fourcc(*codec),
            fps,
            (int(width), int(height)),  # Ensure width and height are explicitly converted to int
        )

    def write_frame(self, frame):
        """Write a frame to the video."""
        self.out.write(frame)

    def release(self):
        """Release the video."""
        self.out.release()
