import cv2
from generic_dataset.dataset_disk_manager import DatasetDiskManager
from generic_dataset.utilities.color import Color

from gibson_env_utilities.doors_dataset.door_sample import DoorSample

env_name, floor = 'house1', 0
dataset_path = '/home/michele/myfiles/doors_dataset'
dataset = DatasetDiskManager(dataset_path=dataset_path, folder_name=env_name, sample_class=DoorSample, max_treads=8)

# Negative sample
negative_sample: DoorSample = dataset.load_sample_using_relative_count(label=0, relative_count=0, use_thread=False)

negative_sample.set_pretty_semantic_image(negative_sample.get_semantic_image().copy())
negative_sample.create_pretty_semantic_image(color=Color(red=0, green=255, blue=0))
negative_sample.pipeline_depth_data_to_image().run(use_gpu=False).get_data()

print('NEGATIVE SAMPLE ROBOT POSE', negative_sample.get_robot_pose())
print('NEGATIVE SAMPLE DEPTH DATA', negative_sample.get_depth_data())

cv2.imshow('Negative sample bgr image', negative_sample.get_bgr_image())
cv2.imshow('Negative sample depth image', negative_sample.get_depth_image())
cv2.imshow('Negative sample semantic image', negative_sample.get_semantic_image())
cv2.imshow('Negative sample pretty semantic image', negative_sample.get_pretty_semantic_image())
cv2.waitKey()

# Positive sample
positive_sample: DoorSample = dataset.load_sample_using_relative_count(label=1, relative_count=1, use_thread=False)

positive_sample.set_pretty_semantic_image(positive_sample.get_semantic_image().copy())
positive_sample.create_pretty_semantic_image(color=Color(red=0, green=255, blue=0))
positive_sample.pipeline_depth_data_to_image().run(use_gpu=False).get_data()

print('POSITIVE SAMPLE ROBOT POSE', positive_sample.get_robot_pose())
print('POSITIVE SAMPLE DEPTH DATA', positive_sample.get_depth_data())

cv2.imshow('Positive sample bgr image', positive_sample.get_bgr_image())
cv2.imshow('Positive sample depth image', positive_sample.get_depth_image())
cv2.imshow('Positive sample semantic image', positive_sample.get_semantic_image())
cv2.imshow('Positive sample pretty semantic image', positive_sample.get_pretty_semantic_image())
cv2.waitKey()
