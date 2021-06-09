import numpy as np
from generic_dataset.sample_generator import SampleGenerator
from generic_dataset.utilities.save_load_methods import save_cv2_image, load_cv2_image

DoorSample = SampleGenerator(name='DoorSample', label_set={0, 1}).add_dataset_field(field_name='bgr_image', field_type=np.ndarray, save_function=save_cv2_image, load_function=load_cv2_image) \
    .generate_sample_class()