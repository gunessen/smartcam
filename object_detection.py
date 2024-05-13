import cv2
import numpy as np
import time

# Load YOLO
# https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4-tiny.weights
# https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov4-tiny.cfg
# https://pjreddie.com/media/files/yolov3-tiny.weights
# https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov3-tiny.cfg
net = cv2.dnn.readNet("models/yolov7-tiny/yolov7-tiny.weights", "models/yolov7-tiny/yolov7-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

classes = []
with open("data/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()

# Adjust the index access method for output layers
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Start the webcam
# TODO: possible edge case that video index starts from an arbitrary number,
# then list devices with /dev/video* and choose the first one
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Set the codec to MJPEG (available formats: `v4l2-ctl --list-formats-ext`)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)

# Set camera resolution (if needed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 5)


# Variables to calculate FPS
frame_count = 0
fps = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame of video to 1/4 size for faster face recognition processing
    frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Information to show on the screen (class ids and confidence values)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        if frame_count % 4 == 0:
                for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            # Object detected
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)

                            # Rectangle coordinates
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            print(label, confidences[i])

    # Increment the frame count
    frame_count += 1

    # Calculate FPS every second
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()

    # Display FPS on the frame
    # cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    print(f"FPS: {fps:.2f}")
    
    # cv2.imshow("Image", frame)
    # key = cv2.waitKey(1)
    # if key == 27: # ESC key to break
    #     break