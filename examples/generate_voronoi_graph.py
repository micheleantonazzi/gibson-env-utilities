import cv2

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities
from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator

voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap(save_to_file=True)
#cv2.imshow('voronoi bitmap', voronoi_bitmap)
#cv2.waitKey()
graph = voronoi_graph_generator.generate_voronoi_graph()

