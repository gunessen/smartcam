import cv2
import numpy as np


class ObjectDetector:
    """A class to detect objects in a video stream"""

    def __init__(self, config_path: str, weights_path: str, classes_path: str):
        """
        Load the network and classes

        :param config_path: path to the configuration file
        :param weights_path: path to the weights file
        :param classes_path: path to the classes file
        """
        self.net = self.load_network(config_path, weights_path)
        self.classes = self.load_classes(classes_path)
        self.output_layers = self.get_output_layers(self.net)

    def load_network(self, config_path: str, weights_path: str) -> cv2.dnn_Net:
        """
        Load the network with the specified configuration and weights

        :param config_path: path to the configuration file
        :param weights_path: path to the weights file
        :return: the loaded network
        """
        net = cv2.dnn.readNet(weights_path, config_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net

    def get_output_layers(self, net: cv2.dnn_Net) -> list:
        """
        Get the output layers of the network and adjust the index access method for output layers

        :param net: the network
        :return: the output layers
        """
        layer_names = net.getLayerNames()
        return [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    def load_classes(self, classes_path: str) -> list[str]:
        """
        Load the classes from the specified file

        :param classes_path: path to the classes file
        :return: the loaded classes
        """
        with open(classes_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def detect_objects(self, frame: np.ndarray) -> np.ndarray:
        """
        Detect objects in the frame

        :param frame: the frame to detect objects in
        :return: the detected objects, width, and height of the frame for further resizing
          of the bounding boxes
        """
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        return outs

    def process_detections(self, outs, frame, threshold=0.5):
        frame_height, frame_width = frame.shape[:2]
        class_ids, confidences, boxes = [], [], []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                # only check for the person (0) and chair (56) classes
                if scores[0] < threshold and scores[56] < threshold:
                    continue

                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    w = int(detection[2] * frame_width)
                    h = int(detection[3] * frame_height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        return boxes, confidences, class_ids

    def process_detections_vectorized(self, outs, frame, threshold=0.5):
        """
        Process the detections using vectorization and return the boxes, confidences, and class IDs

        :param outs: the detections
        :param width: the width of the frame
        :param height: the height of the frame
        :param threshold: the confidence threshold
        :return: the boxes, confidences, and class IDs
        """
        frame_height, frame_width = frame.shape[:2]
        class_ids, confidences, boxes = [], [], []

        # Concatenate all scores from detections into a single array
        all_scores = np.vstack([detection[5:] for out in outs for detection in out])

        # Filter detections where person(0) or chair(56) scores exceed the threshold
        # valid_indices = np.where(
        #     (all_scores[:, 0] >= threshold) | (all_scores[:, 56] >= threshold)
        # )[0]
        valid_indices = np.where(np.max(all_scores, axis=1) >= threshold)[0]

        # Process only valid detections
        filtered_detections = [out[i] for out in outs for i in range(len(out))]
        for index in valid_indices:
            scores = all_scores[index]
            detection = filtered_detections[index]

            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                w = int(detection[2] * frame_width)
                h = int(detection[3] * frame_height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        return boxes, confidences, class_ids

    def get_object_details(self, boxes: list, confidences: list, class_ids: list, use_nms=True):
        """
        Get label, confidence, and bounding box details of the detected objects

        :param frame: the frame to get the object details from
        :param boxes: the bounding boxes
        :param confidences: the confidences of the detections
        :param class_ids: the class IDs of the detections
        :return: the object details
        """
        object_details = []

        # Apply non-maximum suppression to remove overlapping bounding boxes, if requested
        if use_nms:
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if use_nms and i not in indexes:
                continue
            x, y, w, h = boxes[i]
            label = str(self.classes[class_ids[i]])
            confidence = confidences[i]
            object_details.append((label, confidence, (x, y, w, h)))
        return object_details

    def draw_frame_bounding_boxes(self, frame: np.ndarray, object_details: list):
        """
        Draw bounding boxes around detected objects

        :param frame: the frame to draw the bounding boxes on
        :param object_details: the object details
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)

        for label, confidence, (x, y, w, h) in object_details:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 5), font, 0.5, color, 2)

        return frame
