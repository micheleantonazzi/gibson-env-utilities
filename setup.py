import os
import re
import subprocess

# To use a consistent encoding
from codecs import open as copen

import yaml
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with copen(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with copen(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("gibson_env_utilities", "__version__.py")

test_deps = [
    "pytest",
    "pytest-cov",
    "opencv-python"
]

extras = {
    'test': test_deps,
}

# Create the gibson config file
config_parameters = {'model_id': '', 'is_discrete': False, 'random': {'random_initial_pose': False, 'random_init_z_range': [-0.1, 0.1], 'random_target_pose': False, 'random_init_x_range': [-0.1, 0.1], 'random_init_y_range': [-0.1, 0.1], 'random_init_rot_range': [-0.1, 0.1]}, 'ui_num': 3, 'envname': 'TurtlebotNavigateEnv', 'target_orn': [0, 0, 1.57], 'speed': {'timestep': 0.00417, 'frameskip': 10}, 'initial_pos': [0, 0, 0], 'verbose': False, 'fov': 1.57, 'display_ui': True, 'resolution': 512, 'semantic_source': 2, 'target_pos': [0, 0, 0], 'use_filler': True, 'semantic_color': 2, 'mode': 'gui', 'output': ['nonviz_sensor', 'rgb_filled', 'depth', 'semantics'], 'ui_components': ['RGB_FILLED', 'DEPTH', 'SEMANTICS'], 'initial_orn': [0, 0, 0], 'show_diagnostics': False}
with open(os.path.join(os.path.dirname(__file__), 'gibson_env_utilities', 'data', 'gibson_config_file.yaml'), mode='w') as gibson_config_file:
    yaml.dump(config_parameters, gibson_config_file, default_flow_style=False)

setup(
    name='gibson-env-utilities',
    version=__version__,
    description="GibsonEnv utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micheleantonazzi/gibson-env-utilities",
    author="Michele Antonazzi",
    author_email="micheleantonazzi@gmail.com",
    # Choose your license
    license='Apache Licence 2.0',
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    tests_require=test_deps,
    # Add here the package dependencies
    install_requires=[
        'gibson>=0.7',
        'PyYaml',
        'termcolor',
        'trimesh',
        'shapely',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    test_deps=test_deps,
    extras_require=extras,
)