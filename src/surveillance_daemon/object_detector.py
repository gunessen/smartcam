import importlib
import platform
import time

import cv2
import numpy as np


class ModelConfig:
    """Model configuration class."""

    _configs = {
        "efficientdet-lite4": {
            "model_path": "../../models/efficientdet-lite/efficientdet-lite4-detection-default.tflite",
            "input_width": 640,
            "input_height": 640,
            "classes_path": "../../data/coco-efficientdet.names",
            "is_yolo": False,
        },
        "efficientdet-lite3": {
            "model_path": "../../models/efficientdet-lite/efficientdet-lite3-detection-default.tflite",
            "input_width": 512,
            "input_height": 512,
            "classes_path": "../../data/coco-efficientdet.names",
            "is_yolo": False,
        },
        "efficientdet-lite2": {
            "model_path": "../../models/efficientdet-lite/efficientdet-lite2-detection-default.tflite",
            "input_width": 448,
            "input_height": 448,
            "classes_path": "../../data/coco-efficientdet.names",
            "is_yolo": False,
        },
        "efficientdet-lite1": {
            "model_path": "../models/efficientdet-lite/efficientdet-lite1-detection-default.tflite",
            "input_width": 384,
            "input_height": 384,
            "classes_path": "../data/coco-efficientdet.names",
            "is_yolo": False,
        },
        "ssd-mobilenet-v1": {
            "model_path": "../../models/mobilenetv1/ssd-mobilenet-v1-default.tflite",
            "input_width": 300,
            "input_height": 300,
            "classes_path": "../../data/coco-efficientdet.names",
            "is_yolo": False,
        },
        "yolov5-small": {
            "model_path": "../../models/yolov5-small/yolov5-small.tflite",
            "input_width": 320,
            "input_height": 320,
            "classes_path": "../../data/coco.names",
            "is_yolo": True,
        },
        "yolov5-nano": {
            "model_path": "../../models/yolov5/yolov5n-fp16.tflite",
            "input_width": 320,
            "input_height": 320,
            "classes_path": "../../data/coco.names",
            "is_yolo": True,
        },
    }

    @staticmethod
    def get_config(model_name):
        """Get the model configuration."""
        return ModelConfig._configs[model_name]

    @staticmethod
    def list_models():
        """List the available models."""
        return list(ModelConfig._configs.keys())


class DetectedObject:
    def __init__(
        self, category: str, category_id, confidence: float, bbox: tuple[int, int, int, int]
    ):
        self.category = category
        self.category_id = category_id
        self.confidence = confidence
        self.bbox = bbox


class ObjectDetector:
    def __init__(
        self,
        model_path: str,
        input_width: int,
        input_height: int,
        classes_path: str,
        is_yolo: bool,
        num_threads: int = 3,
    ):
        """
        Load the network and classes

        :param config_path: path to the configuration file
        :param weights_path: path to the weights file
        :param classes_path: path to the classes file
        """
        self.classes = self.load_classes(classes_path)
        self._allowed_class_ids = [
            index
            for index, cls in enumerate(self.classes)
            if cls in ("person", "cat", "dog", "bird")
        ]
        self.model_path = model_path
        self.input_width = input_width
        self.input_height = input_height
        self.is_yolo = is_yolo

        # Determine CPU type or system constraint
        arch = platform.machine()

        # If ARM architecture, use TensorFlow Lite, otherwise use full TensorFlow
        if "ARM" in arch.upper():
            tflite = importlib.import_module("tflite_runtime.interpreter")
            self.interpreter = tflite.Interpreter(
                model_path=self.model_path, num_threads=num_threads
            )
        else:
            tf = importlib.import_module("tensorflow")
            self.interpreter = tf.lite.Interpreter(
                model_path=self.model_path, num_threads=num_threads
            )

        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def load_classes(self, classes_path: str) -> list[str]:
        """
        Load the classes from the specified file

        :param classes_path: path to the classes file
        :return: the loaded classes
        """
        with open(classes_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def process_detections_vectorized_tf(
        self,
        detection_boxes,
        detection_scores,
        detection_classes,
        frame_width,
        frame_height,
        inverted_coords=False,
        threshold=0.5,
    ):
        """
        Process the detections using vectorization and return the boxes, confidences, and class IDs
        formatted for drawing.

        :param detection_boxes: tensor of bounding boxes
        :param detection_scores: tensor of confidence scores
        :param detection_classes: tensor of class IDs
        :param input_width: the width the model is expecting
        :param input_height: the height the model is expecting
        :param frame_width: the actual width of the frame
        :param frame_height: the actual height of the frame
        :param threshold: the confidence threshold
        :return: List of tuples containing (label, confidence, (x, y, w, h))
        """
        # Filter out detections below the threshold
        valid_indices = np.where(detection_scores >= threshold)[0]

        detected_objects = []
        for idx in valid_indices:
            # Only process detections above the threshold
            score = detection_scores[idx]
            if score < threshold:
                continue

            # Only process detections for the specified classes
            class_id = int(detection_classes[idx])
            if class_id not in self._allowed_class_ids:
                continue

            box = detection_boxes[idx]

            # Rescale box from input dimensions to frame dimensions
            x0 = box[0] * frame_width
            y0 = box[1] * frame_height
            x1 = box[2] * frame_width
            y1 = box[3] * frame_height
            if inverted_coords:
                y0 = box[0] * frame_height
                x0 = box[1] * frame_width
                y1 = box[2] * frame_height
                x1 = box[3] * frame_width

            x = int(x0)
            y = int(y0)
            w = int((x1 - x0))
            h = int((y1 - y0))

            detected_objects.append(
                DetectedObject(self.classes[class_id], max(class_id - 1, 0), score, (x, y, w, h))
            )

        return detected_objects

    def process_detections_vectorized_yolo(self, outs, frame_width, frame_height, threshold=0.5):
        """
        Process the detections using vectorization and return the boxes, confidences, and class IDs
        formatted for drawing.

        :param outs: the detections output tensor from TensorFlow Lite
        :param frame_width: the width of the frame
        :param frame_height: the height of the frame
        :param threshold: the confidence threshold
        :return: List of tuples containing (label, confidence, (x, y, w, h))
        """
        scores = outs[:, 4]  # Assuming the fifth column in each row is the confidence score
        classes = outs[:, 5:].argmax(
            axis=-1
        )  # Assuming class probabilities start from the sixth column
        confidences = outs[:, 5:].max(axis=-1)

        # Filter out detections below the threshold
        valid_indices = np.where(scores >= threshold)[0]

        detected_objects = []
        for idx in valid_indices:
            score = scores[idx]
            if score < threshold:
                continue

            # Only process detections for the specified classes
            class_id = classes[idx]
            if class_id not in self._allowed_class_ids:
                continue

            confidence = confidences[idx]
            box = outs[idx, :4]  # Get the box details

            # Transform the normalized coordinates to pixel coordinates
            cx, cy, w, h = box
            cx *= frame_width
            cy *= frame_height
            w *= frame_width
            h *= frame_height
            x = int(cx - w / 2)
            y = int(cy - h / 2)
            w = int(w)
            h = int(h)

            detected_objects.append(
                DetectedObject(self.classes[class_id], class_id, confidence, (x, y, w, h))
            )

        return detected_objects

    def process_detections_vectorized_yolo_nms(
        self, outs, frame_width, frame_height, threshold=0.5
    ):
        scores = outs[:, 4]  # Confidence scores
        classes = outs[:, 5:].argmax(axis=-1)  # Class IDs
        confidences = outs[:, 5:].max(axis=-1)

        boxes = []
        class_ids = []
        conf_scores = []

        # Filter out detections below the threshold and prepare for NMS
        for i in range(len(scores)):
            score = scores[i]
            if score < threshold:
                continue

            class_id = classes[i]
            if class_id not in self._allowed_class_ids:
                continue

            confidence = confidences[i]

            # Convert the box to pixel coordinates
            box = outs[i, :4]
            cx, cy, w, h = box
            x = int((cx - w / 2) * frame_width)
            y = int((cy - h / 2) * frame_height)
            w = int(w * frame_width)
            h = int(h * frame_height)

            boxes.append([x, y, w, h])
            conf_scores.append(float(confidence))
            class_ids.append(class_id)

        # Applying NMS
        indices = cv2.dnn.NMSBoxes(boxes, conf_scores, score_threshold=threshold, nms_threshold=0.4)

        detected_objects = []
        for i in indices:
            box = boxes[i]
            class_id = class_ids[i]
            confidence = conf_scores[i]

            # Assuming 'DetectedObject' is a constructor for detected items
            detected_objects.append(
                DetectedObject(self.classes[class_id], class_id, confidence, tuple(box))
            )

        return detected_objects

    def draw_frame_bounding_boxes(self, frame: np.ndarray, detected_objects: list):
        """
        Draw bounding boxes around detected objects

        :param frame: the frame to draw the bounding boxes on
        :param object_details: the object details
        """
        font = cv2.FONT_HERSHEY_SIMPLEX

        for obj in detected_objects:
            x, y, w, h = obj.bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{obj.category} {obj.confidence:.2f}",
                (x, y - 5),
                font,
                0.5,
                (255, 255, 255),
                2,
            )

        return frame

    def process_frame(self, frame: np.ndarray, frame_width: int, frame_height: int, threshold=0.5):
        """
        Process a frame and return the object details

        :param frame: the frame to process
        :param threshold: the confidence threshold
        :return: the object details
        """
        start_time = time.time()

        # Set the input tensor and invoke the interpreter
        self.interpreter.set_tensor(self.input_details[0]["index"], frame)
        self.interpreter.invoke()

        # Retrieve output tensors and process the detections
        if self.is_yolo:
            output_data = self.interpreter.get_tensor(self.output_details[0]["index"])
            object_details = self.process_detections_vectorized_yolo_nms(
                output_data[0],
                frame_width,
                frame_height,
                threshold=threshold,
            )
        else:
            boxes = self.interpreter.get_tensor(self.output_details[0]["index"])  # Bounding boxes
            classes = self.interpreter.get_tensor(self.output_details[1]["index"])  # Class labels
            scores = self.interpreter.get_tensor(
                self.output_details[2]["index"]
            )  # Confidence scores
            _ = self.interpreter.get_tensor(self.output_details[3]["index"])  # Number of detections

            object_details = self.process_detections_vectorized_tf(
                detection_boxes=boxes[0],
                detection_scores=scores[0],
                detection_classes=classes[0],
                frame_width=frame_width,
                frame_height=frame_height,
                inverted_coords=True,
                threshold=threshold,
            )

        # Calculate processing time and FPS
        end_time = time.time()
        processing_time = end_time - start_time

        return object_details, processing_time

    def process_video(
        self,
        in_video_path: str,
        store_out_video=True,
        threshold=0.5,
        output_codec="VP90",
        output_ext="webm",
    ) -> set[str]:
        """
        Process and save the video and write the detected objects to the video
        into the database

        :param video_path: the path to the video
        :param threshold: the confidence threshold
        :return: the detected objects and the path to the annotated video
        """
        cap = cv2.VideoCapture(in_video_path)
        if not cap.isOpened():
            print(f"Failed to open video: {in_video_path}")
            return

        # Get the frame width, height, and FPS
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the output path
        output_path = None
        if store_out_video and in_video_path.endswith("_unannotated.avi"):
            output_path = in_video_path.replace("_unannotated.avi", f".{output_ext}")
        elif store_out_video:
            output_path = in_video_path[: in_video_path.rfind(".")] + f"_annotated.{output_ext}"

        # Initialize the video writer
        out = None
        if store_out_video:
            out = cv2.VideoWriter(
                output_path,
                cv2.VideoWriter_fourcc(*output_codec),
                fps,
                (frame_width, frame_height),
            )

        event_objects = dict()
        processed_frames = 0
        start_time = time.time()

        # Process each frame in the video
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Prepare the frame for processing
            frame_resized = cv2.resize(frame, (self.input_width, self.input_height))
            input_data = np.expand_dims(frame_resized, axis=0)
            if self.is_yolo:
                input_data = np.expand_dims(frame_resized, axis=0).astype(np.float32) / 255.0

            detected_objects, _ = self.process_frame(
                frame=input_data,
                frame_width=frame_width,
                frame_height=frame_height,
                threshold=threshold,
            )
            for obj in detected_objects:
                event_objects[obj.category] = max(
                    obj.confidence, event_objects.get(obj.category, 0)
                )
            frame = self.draw_frame_bounding_boxes(frame, detected_objects)
            if store_out_video:
                out.write(frame)

            processed_frames += 1
            # print(f"Processed {processed_frames}/{total_frames} frames", end="\n")

        cap.release()
        if store_out_video:
            out.release()
            print(f"Released the video: {output_path}")

        # Calculate processing time and FPS
        end_time = time.time()
        processing_time = end_time - start_time
        processing_fps = processed_frames / processing_time if processing_time > 0 else 0

        return event_objects, output_path, processing_fps
