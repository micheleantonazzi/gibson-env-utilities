import os.path
from typing import Dict
import copy

import yaml


class GibsonEnvironmentsData:
    KEY_HAS_SEMANTICS = 'has_semantics'
    KEY_DATASET = 'dataset'
    KEY_PLANS = 'plans'
    KEY_POSITION = 'position'
    KEY_ORIENTATION = 'orientation'
    KEY_FLOOR_HEIGHT = 'floor_height'

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'environments_data.yaml'), mode='r') as f:
            self._environments_data: Dict = yaml.load(f, Loader=yaml.FullLoader)

    def get_environments_data(self) -> Dict:
        return copy.deepcopy(self._environments_data)

    def get_environments_with_semantics(self) -> Dict:
        return copy.deepcopy({key: value for key, value in self._environments_data.items() if value[GibsonEnvironmentsData.KEY_HAS_SEMANTICS]})
