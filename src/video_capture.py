import cv2


class VideoCapture:
    """A class to capture video from the camera"""

    def __init__(self, codec="MJPG", width=800, height=600, fps=30):
        """
        Setup the camera with the specified codec, resolution, and FPS

        :param codec: the codec to capture the video
        :param width: the width of the camera frame
        :param height: the height of the camera frame
        :param fps: the FPS of the camera
        """
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*codec))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

    def read_frame(self):
        """Read a frame from the camera"""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        """Release the camera"""
        self.cap.release()
