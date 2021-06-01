import cv2
from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator

voronoi_bitmap = VoronoiGraphGenerator(env_name='space7', floor=0).generate_voronoi_bitmap()
cv2.imshow('voronoi bitmap', voronoi_bitmap)
cv2.waitKey()
