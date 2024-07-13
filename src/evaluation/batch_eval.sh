#!/bin/bash

python3 evaluate.py --model efficientdet-lite1 --batch_size 100 --num_threads 4 > efficientdet-lite1.txt
python3 evaluate.py --model efficientdet-lite2 --batch_size 100 --num_threads 4 > efficientdet-lite2.txt
python3 evaluate.py --model efficientdet-lite3 --batch_size 100 --num_threads 4 > efficientdet-lite3.txt
python3 evaluate.py --model efficientdet-lite4 --batch_size 100 --num_threads 4 > efficientdet-lite4.txt
python3 evaluate.py --model ssd-mobilenet-v1 --batch_size 100 --num_threads 4 > ssd-mobilenet-v1.txt
python3 evaluate.py --model yolov5-small --batch_size 100 --num_threads 4 > yolov5-small
python3 evaluate.py --model yolov5-nano --batch_size 100 --num_threads 4 > yolov5-nano
