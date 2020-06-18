import os
import sys

main_path = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(main_path, "TrainYourOwnYOLO", "2_Training", "src")

# load custom modules
sys.path.append(src_path)
from keras_yolo3.yolo import YOLO

data_folder = os.path.join(main_path, "TrainYourOwnYOLO", "Data")
image_folder = os.path.join(data_folder, "Source_Images")
model_folder = os.path.join(data_folder, "Model_Weights")

model_weights = os.path.join(model_folder, "trained_weights_final.h5")
anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")
model_classes = os.path.join(model_folder, "data_classes.txt")


"""ACTIVATE YOLO CONES DETECTION MODEL"""
yolo = YOLO(
    **{
        "model_path": model_weights,
        "anchors_path": anchors_path,
        "classes_path": model_classes,
        "score": .3,
        "gpu_num": 1,
        "model_image_size": (416, 416),
    }
)