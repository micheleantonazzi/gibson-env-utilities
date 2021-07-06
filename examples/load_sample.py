import cv2
from generic_dataset.dataset_folder_manager import DatasetFolderManager
from generic_dataset.utilities.color import Color

from gibson_env_utilities.doors_dataset.door_sample import DoorSample

env_name, floor = 'house1', 0
dataset_path = '/home/michele/myfiles/doors_dataset'
dataset = DatasetFolderManager(dataset_path=dataset_path, folder_name=env_name, sample_class=DoorSample, max_treads=8)

# Negative sample
negative_sample: DoorSample = dataset.load_sample_using_relative_count(label=0, relative_count=0, use_thread=False)

negative_sample.set_pretty_semantic_image(negative_sample.get_semantic_image().copy())
negative_sample.create_pretty_semantic_image(color=Color(red=0, green=255, blue=0))
negative_sample.pipeline_depth_data_to_image().run(use_gpu=False).get_data()

negative_sample.visualize()

# Positive sample
positive_sample: DoorSample = dataset.load_sample_using_relative_count(label=1, relative_count=1, use_thread=False)

positive_sample.set_pretty_semantic_image(positive_sample.get_semantic_image().copy())
positive_sample.create_pretty_semantic_image(color=Color(red=0, green=255, blue=0))
positive_sample.pipeline_depth_data_to_image().run(use_gpu=False).get_data()

positive_sample.visualize()
