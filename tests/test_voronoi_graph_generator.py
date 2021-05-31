import os

import cv2
import numpy as np

from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator


def test_voronoi_bitmap():
    voronoi_bitmap = VoronoiGraphGenerator(env_name='house1', floor=0).generate_voronoi_bitmap()

    voronoi_bitmap_loaded = cv2.imread(os.path.join(os.path.dirname(__file__), 'images', 'house_1_floor_0_voronoi_graph.png'), flags=cv2.IMREAD_GRAYSCALE)
    assert np.array_equal(voronoi_bitmap_loaded, voronoi_bitmap)