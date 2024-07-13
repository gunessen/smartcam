import argparse
import json

import cv2
import numpy as np
from object_detector import ObjectDetector

model_config = {
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
        "model_path": "../../models/efficientdet-lite/efficientdet-lite1-detection-default.tflite",
        "input_width": 384,
        "input_height": 384,
        "classes_path": "../../data/coco-efficientdet.names",
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

parser = argparse.ArgumentParser(description="Evaluate the object detector")
parser.add_argument(
    "--model",
    type=str,
    default="efficientdet-lite1",
    help="The model to use for object detection",
)
parser.add_argument(
    "--batch_size",
    type=int,
    default=100,
    help="The batch size to use for object detection",
)
parser.add_argument(
    "--num_threads",
    type=int,
    default=4,
    help="The number of threads to use for object detection",
)
args = parser.parse_args()

CURRENT_MODEL = model_config[args.model]

object_detector = ObjectDetector(
    model_path=CURRENT_MODEL["model_path"],
    input_width=CURRENT_MODEL["input_width"],
    input_height=CURRENT_MODEL["input_height"],
    classes_path=CURRENT_MODEL["classes_path"],
    is_yolo=CURRENT_MODEL["is_yolo"],
    num_threads=args.num_threads,
)

print(f"Using model: {args.model}")

with open("Objects365/test/filtered_data_coco.json", "r") as f:
    ds = json.load(f)

# Store COCO detection results
detection_results = []

ann_id = 0

total_processing_time = 0
batch_processing_time = 0

# Table header
print(
    f"""{'Index':<10} | {'Batch (s)':<20} | {'Total per image (s)':<20} | {'Batch per image (s)':<20} | {'Total FPS':<20} | {'Batch FPS':<20} |"""
)

batch_size = args.batch_size

for i, img in enumerate(ds["images"]):
    # Read the frame and resize it
    frame = cv2.imread(f"./Objects365/test/small-ds/{img['file_name']}")
    frame_height, frame_width, _ = frame.shape
    frame_resized = cv2.resize(frame, (CURRENT_MODEL["input_width"], CURRENT_MODEL["input_height"]))
    input_data = np.expand_dims(frame_resized, axis=0)
    if CURRENT_MODEL["is_yolo"]:
        input_data = np.expand_dims(frame_resized, axis=0).astype(np.float32) / 255.0

    detected_objects, processing_time = object_detector.process_frame(
        frame=input_data, frame_width=frame_width, frame_height=frame_height
    )
    total_processing_time += processing_time
    batch_processing_time += processing_time

    # Store the detection results
    for obj in detected_objects:
        ann_id += 1
        detection_results.append(
            {
                "image_id": img["id"],
                "category_id": int(obj.category_id),
                "bbox": list(obj.bbox),
                "score": float(obj.confidence),
            }
        )

    if i > 0 and (i + 1) % batch_size == 0:
        print(
            f"""{i+1:>10} | {batch_processing_time:>20.2f} | {total_processing_time / (i + 1):>20.2f} | {batch_processing_time / (batch_size):>20.3f} | {1 / (total_processing_time / (i + 1)):>20.2f} | {1 / (batch_processing_time / (batch_size)):>20.2f} |"""
        )
        batch_processing_time = 0

    # annotated_frame = object_detector.draw_frame_bounding_boxes(frame, detected_objects)

    # cv2.imshow('Object Detection', annotated_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    if i + 1 >= 1000:
        break

# Save the detection results
# with open("./Objects365/test/yolov5n-fp16.json", "w") as f:
#     json.dump(detection_results, f)
