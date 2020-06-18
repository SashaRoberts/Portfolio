#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:15:15 2020

@author: nickgallagher
"""

# imports
import os
import sys
from datetime import datetime
import tensorflow as tf
from tensorflow.python.util import deprecation

# disables tensorflow warnings
deprecation._PRINT_DEPRECATION_WARNINGS = False
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# create PATHs
main_path = os.path.dirname(os.path.realpath(__file__))
# main_path = '/Users/nickgallagher/Desktop/OBJECT_DETECTION'

# cones module paths
infer_path = os.path.join(main_path, "TrainYourOwnYOLO", "3_Inference")
utils_path = os.path.join(main_path, "TrainYourOwnYOLO", "Utils")

# edge tpu module paths
edge_path = os.path.join(main_path, 'tflite/python/examples/detection')
img_path = os.path.join(edge_path, 'images')
model_file_tpu = os.path.join(edge_path, 'models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
model_file = os.path.join(edge_path, 'models/mobilenet_ssd_v2_coco_quant_postprocess.tflite')
labels_file = os.path.join(edge_path, 'models/coco_labels.txt')

# load custom modules
sys.path.append(main_path)
from capture_image_webcam import *
from load_cones_yolo import yolo

# load custom modules #1
sys.path.append(utils_path)
from utils import detect_object

# load custom modules #2
sys.path.append(edge_path)
from detect_image import edge_detect
from load_model_classes import load_labels, make_interpreter

# load custom modules #3
sys.path.append(infer_path)
from ConesInference import detect_cones

# get label and load interpreter
labels = load_labels(labels_file) if labels_file else {}

# load the edge tpu model for object detection
try:
    interpreter = make_interpreter(model_file_tpu, edge=True)
    print('\nEdge TPU object detector loaded successfully.')
except ValueError:
    print('\nEdge TPU not plugged in. Please check that it is plugged into a USB-c slot.')

    resp = input('-Would you like to run without TPU? Yes (y) or No (n): ')
    if resp != 'y' and resp != 'n':
        print('---Invalid choice, exiting program.')
        sys.exit(1)
    elif resp == 'n':
        print('---Exiting program...')
        sys.exit(1)
    else:
        try:
            interpreter = make_interpreter(model_file, edge=False)
            print('---Non-TPU object detector loaded successfully.')
        except ValueError:
            print('---Unable to load object detection model.')
            sys.exit(1)


def easy_detect(k, cam_type):
    # function to run detections
    if k == 'c':
        cone_preds = detect_cones(yolo, main_path, take_picture, cam_type, detect_object, save_img=True)
        return cone_preds

    # take picture and detect objects
    elif k == 'o':
        take_picture(cam_type, img_path, 'object.jpg')
        return edge_detect(interpreter, labels, edge_path, show_image=False)
