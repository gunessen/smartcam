import cv2
import numpy as np
import time
from numba import jit
from line_profiler import profile


def load_network(config_path: str, weights_path: str) -> cv2.dnn_Net:
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


def get_output_layers(net: cv2.dnn_Net) -> list:
    """
    Get the output layers of the network and adjust the index access method for output layers

    :param net: the network
    :return: the output layers
    """
    layer_names = net.getLayerNames()
    return [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]


def load_classes(classes_path: str) -> list[str]:
    """
    Load the classes from the specified file

    :param classes_path: path to the classes file
    :return: the loaded classes
    """
    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return classes


def setup_camera(fourcc: str, width: int, height: int, fps: int) -> cv2.VideoCapture:
    """
    Setup the camera with the specified codec, resolution, and FPS

    :param fourcc: the codec
    :param width: the width of the camera frame
    :param height: the height of the camera frame
    :param fps: the FPS of the camera
    :return: the camera object
    """
    cap = cv2.VideoCapture(0, cv2.CAP_ANY)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    return cap


@profile
def detect_objects(
    frame: np.ndarray, net: cv2.dnn_Net, output_layers: list[str]
) -> tuple[np.ndarray, int, int]:
    """
    Detect objects in the frame

    :param frame: the frame
    :param net: the network
    :param output_layers: the output layers
    :return: the detected objects, width, and height of the frame for further resizing
        of the bounding boxes
    """
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    return outs, width, height


@jit(nopython=True, cache=False, parallel=False, fastmath=False, nogil=False)
def process_detections(
    outs, width, height, threshold
) -> tuple[list[list[int]], list[float], list[int]]:
    """
    Process the detections and return the boxes, confidences, and class IDs

    :param outs: the detections
    :param width: the width of the frame
    :param height: the height of the frame
    :param threshold: the confidence threshold
    :return: the boxes, confidences, and class IDs
    """
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            # only check for the person (0) and chair (56) classes
            if scores[0] < threshold and scores[56] < threshold:
                continue
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids


def process_detections_vectorized(outs, width, height, threshold):
    """
    Process the detections using vectorization and return the boxes, confidences, and class IDs

    :param outs: the detections
    :param width: the width of the frame
    :param height: the height of the frame
    :param threshold: the confidence threshold
    :return: the boxes, confidences, and class IDs
    """
    class_ids = []
    confidences = []
    boxes = []

    # Concatenate all scores from detections into a single array
    all_scores = np.vstack([detection[5:] for out in outs for detection in out])

    # Filter detections where person (0) or chair (56) scores exceed the threshold
    valid_indices = np.where((all_scores[:, 0] >= threshold) | (all_scores[:, 56] >= threshold))[0]

    # Process only valid detections
    filtered_detections = [out[i] for out in outs for i in range(len(out))]
    for index in valid_indices:
        scores = all_scores[index]
        detection = filtered_detections[index]

        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > threshold:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    return boxes, confidences, class_ids


@profile
def main():
    """Driver function for object detection"""
    # Load the network, classes, and output layers
    net = load_network(
        "models/yolov7-tiny/yolov7-tiny.cfg", "models/yolov7-tiny/yolov7-tiny.weights"
    )
    classes = load_classes("data/coco.names")
    output_layers = get_output_layers(net)

    # Setup the camera
    # cap = setup_camera("MJPG", 800, 600, 10)
    cap = setup_camera("MJPG", 800, 600, 30)

    # Variables to calculate FPS
    start_time = time.time()
    frame_count = 0
    z = 0

    # Main loop for object detection
    while True:
        # Read the frame and break the loop if there is no frame
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects in the frame and process the detections
        outs, width, height = detect_objects(frame, net, output_layers)
        boxes, confidences, class_ids = process_detections(outs, width, height, 0.5)

        # Drawing boxes and displaying the frames would go here
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                print(label, confidences[i])

        # Calculate FPS
        frame_count += 1
        if time.time() - start_time > 1:
            print(f"FPS: {frame_count / (time.time() - start_time)}")
            frame_count = 0
            start_time = time.time()

        # Wait for ESC key to break the loop
        if cv2.waitKey(1) == 27:
            break
        
        z += 1
        if z == 100:
            break

    # Release the camera and destroy all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
