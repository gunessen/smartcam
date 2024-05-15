import cv2


class MotionDetector:
    """A class to detect motion in a video stream"""

    def __init__(self, history: int = 100, threshold: float = 600):
        """
        Initialize the background subtractor with the specified history and variance threshold

        :param history: the number of frames to use for the background model
        :param var_threshold: the variance threshold for the background model
        """
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history, varThreshold=threshold
        )

    def detect_motion(self, frame) -> bool:
        """
        Detect motion in the frame

        :param frame: the frame to detect motion in
        :return: the motion detected in the frame
        """
        fg_mask = self.bg_subtractor.apply(frame)
        result = cv2.countNonZero(fg_mask) > 0
        return result
