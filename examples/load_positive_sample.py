import cv2
import numpy as np
from generic_dataset.dataset_disk_manager import DatasetDiskManager
from generic_dataset.utilities.color import Color

from gibson_env_utilities.doors_dataset.door_sample import DoorSample

doors_dataset = DatasetDiskManager(dataset_path='/home/michele/myfiles/doors_dataset', folder_name='house1', sample_class=DoorSample)

sample: DoorSample = doors_dataset.load_sample_using_relative_count(label=1, relative_count=0, use_thread=False)
print(sample.get_bgr_image())
sample.set_pretty_semantic_image(sample.get_semantic_image().copy())
sample.pipeline_depth_data_to_image().run(use_gpu=False).get_data()
sample.create_pretty_semantic_image(color=Color(red=0, green=256, blue=0))

display_image_0 = np.concatenate((sample.get_bgr_image(), cv2.cvtColor(sample.get_depth_image(), cv2.COLOR_GRAY2BGR)), axis=1)
display_image_1 = np.concatenate((sample.get_semantic_image(), sample.get_pretty_semantic_image()), axis=1)

cv2.imshow('sample', np.concatenate((display_image_0, display_image_1), axis=0))
cv2.waitKey()