import cv2

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities
from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator

# Load house1 map
voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
house1_map = voronoi_graph_generator.get_map()
cv2.imshow('map', house1_map)
cv2.waitKey()

# Generate voronoi bitmap and the relative graph starting from the map of house 1
voronoi_bitmap = voronoi_graph_generator.generate_voronoi_bitmap(save_to_file=False)
cv2.imshow('voronoi bitmap', voronoi_bitmap)
cv2.waitKey()

# Get positions every 10cm and print them in the map
graph = voronoi_graph_generator.get_voronoi_graph()
positions = graph.get_real_position(0.01)
for position in positions:
    house1_map[position.to_img_index()] = 127
cv2.imshow('map with selected positions', house1_map)
cv2.waitKey()


