import os

import cv2
import numpy as np
import pytest

from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator


def test_voronoi_bitmap():
    with pytest.raises(FileNotFoundError):
        VoronoiGraphGenerator(env_name='house14', floor=0)

    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    assert np.array_equal(graph.get_graph_bitmap(), voronoi_bitmap)


def test_graph_nodes():
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    # Test nodes
    black_pixels = voronoi_bitmap[voronoi_bitmap == 0]
    assert len(graph.get_nodes().values()) == len(black_pixels)


def test_graph_connected_components():
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap()
    graph = voronoi_graph_generator.get_voronoi_graph()

    components_image = np.array([[255 for _ in range(voronoi_bitmap.shape[0])] for _ in range(voronoi_bitmap.shape[1])], dtype=np.uint8)
    for component in graph.get_connected_components().values():
        for node in component:
            components_image[node.get_image_coordinates()[0], node.get_image_coordinates()[1]] = 0

    assert np.array_equal(components_image, voronoi_bitmap)
