import cv2
from object_detector import ObjectDetector
from video_capture import VideoCapture


def main():
    # Initialize camera and object detector
    detector = ObjectDetector(
        "models/yolov7-tiny/yolov7-tiny.cfg",
        "models/yolov7-tiny/yolov7-tiny.weights",
        "data/coco.names",
    )

    with VideoCapture() as camera:
        while True:
            frame = camera.read_frame()
            if frame is None:
                break

            outs = detector.detect_objects(frame)
            boxes, confidences, class_ids = detector.process_detections_vectorized(outs, frame, 0.5)
            object_details = detector.get_object_details(boxes, confidences, class_ids, True)
            detector.draw_frame_bounding_boxes(frame, object_details)
            # detector.draw_bounding_boxes(frame, boxes, confidences, class_ids)

            cv2.imshow("Object detection", frame)

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
