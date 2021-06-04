import os

import cv2
import numpy as np

from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator


def test_voronoi_bitmap():
    voronoi_bitmap = VoronoiGraphGenerator(env_name='house1', floor=0).generate_voronoi_bitmap()

    voronoi_bitmap_loaded = cv2.imread(os.path.join(os.path.dirname(__file__), 'images', 'house_1_floor_0_voronoi_graph.png'), flags=cv2.IMREAD_GRAYSCALE)
    assert np.array_equal(voronoi_bitmap_loaded, voronoi_bitmap)


def test_graph_nodes():
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    # Test nodes
    black_pixels = voronoi_bitmap[voronoi_bitmap == 0]
    assert len(graph.get_nodes().values()) == len(black_pixels)


def test_graph_bitmap():
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    assert np.array_equal(voronoi_bitmap, graph.get_graph_bitmap())


def test_graph_connected_components():
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    components_image = np.array([[255 for _ in range(voronoi_bitmap.shape[0])] for _ in range(voronoi_bitmap.shape[1])], dtype=np.uint8)
    for component in graph.get_connected_components().values():
        for node in component:
            components_image[node.get_image_coordinates()[0], node.get_image_coordinates()[1]] = 0

    assert np.array_equal(components_image, voronoi_bitmap)
