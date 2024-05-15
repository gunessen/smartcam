import cv2


class VideoCapture:
    """A class to capture video from the camera"""

    def __init__(self, device=0, codec="MJPG", width=800, height=600, fps=15):
        """
        Setup the camera with the specified codec, resolution, and FPS and create videos directory

        :param codec: the codec to capture the video
        :param width: the width of the camera frame
        :param height: the height of the camera frame
        :param fps: the FPS of the camera
        """
        self.cap = cv2.VideoCapture(device, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*codec))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

    def get_fps(self):
        """Get the FPS of the camera"""
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_frame_width(self):
        """Get the frame width of the camera"""
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_frame_height(self):
        """Get the frame height of the camera"""
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def read_frame(self):
        """Read a frame from the camera"""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        """Release the camera"""
        self.cap.release()
