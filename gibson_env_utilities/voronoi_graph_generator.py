import os
from typing import List, Tuple, Dict, Set

import cv2
import numpy as np
import skimage
from skimage.morphology import skeletonize
from termcolor import colored

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities


class Node:
    def __init__(self, x_image: int, y_image: int, map_origin: (int, int), scale: float):
        self._x_image = x_image
        self._y_image = y_image
        self._x_real = (x_image - map_origin[0]) * scale
        self._y_real = (y_image - map_origin[1]) * scale
        self._connected_nodes: Set[Node] = set()

    def connect_with(self, node: 'Node'):
        self._connected_nodes.add(node)

    def get_image_coordinates(self):
        return self._x_image, self._y_image

    def get_connected_nodes(self) -> Set['Node']:
        return self._connected_nodes

    def __eq__(self, other):
        return isinstance(other, Node) and self._x_image == other._x_image and self._y_image == other._y_image

    def __hash__(self):
        return hash((self._x_image, self._y_image))


class Graph:
    def __init__(self, image_width, image_height):
        self._image_width = image_width
        self._image_height = image_height
        self._nodes: Dict[Tuple, Node] = {}
        self._arcs = set()
        self._connected_components: Dict[int, Set[Node]] = {}

    def add_node(self, node: Node):
        if node.get_image_coordinates() not in self._nodes:
            self._nodes[node.get_image_coordinates()] = node

    def get_nodes(self) -> Dict[Tuple[int, int], Node]:
        return self._nodes

    def add_connection(self, node1_coordinates: Tuple[int, int], node2_coordinates: Tuple[int, int]):
        self._nodes[node1_coordinates].connect_with(self._nodes[node2_coordinates])

    def get_connected_components(self):
        return self._connected_components

    def find_connected_components(self):
        component_id = 0

        visited_nodes = set()

        nodes_in_components: Dict[Node, int] = {}

        def find_connected_component(node: Node):
            if node in visited_nodes:
                return

            visited_nodes.add(node)
            self._connected_components[component_id].add(node)
            nodes_in_components[node] = component_id

            for connected_node in node.get_connected_nodes():
                find_connected_component(connected_node)

        for node in self._nodes.values():

            # Verify that the node does not already belong to a connected component
            if node not in nodes_in_components:
                visited_nodes = set()
                self._connected_components[component_id] = set()
                find_connected_component(node)
                component_id += 1


class VoronoiGraphGenerator:
    def __init__(self, env_name: str, floor: int):
        self._env_name = env_name
        self._floor = floor
        self._assets_manager = GibsonAssetsUtilities()
        try:
            self._map, self._map_metadata = self._assets_manager.load_map_and_metadata(env_name=env_name, floor=floor)
        except FileNotFoundError:
            print(colored('The map or its metadata of the {0} world do not exist! Create them before using this VoronoiGraphGenerator'.format(env_name), 'red'))
            raise FileNotFoundError

        self._map: np.array = cv2.cvtColor(self._map, cv2.COLOR_RGB2GRAY)
        self._voronoi_bitmap = np.array([], dtype=int)

        # Graph structure
        # Contains the black point of the voronoi bitmap (which are all graph nodes)
        self._graph = Graph(self._map.shape[0], self._map.shape[1])

    def generate_voronoi_bitmap(self, robot_radius: float = 0.05, save_to_file: bool = False) -> np.array:
        """
        This method generates a voronoi bitmap starting from a floor map.
        Steps:
            1) a thresholding procedure is applied to the original floor map (the values between 0 and 250 are turned to 0)
            2) then the resulting image is eroded and dilated
            3) the resulting image is processed to find the contours
            4) the building's outline is identified (searching the longest contour)
            5) the external area of the building's contour is black filled
            6) the contour inside the building's outline are drawn and black filled
               (now the floor plan is black outside the building and over the obstacles)
            7) now, new and simplified contours are found using the previous image (which is black outside the building outline and over the obstacles)
            8) using these simplified contours, it is calculated the voronoi diagram
            9) the segments of the voronoi facets perimeter are examined.
               They are drawn only if they are inside the building's outline and not overlap an obstacle
               (in other words, if the extreme points that define a segment are inside the image and the correspondent pixel is white)
            10) To clean the voronoi bitmap, it is dilated and then its skeleton is found using scikit-image
            11) Finally, all pixels of the voronoi bitmap too close to an obstacle are discarded (this operation is performed using robot_radius parameter).

        :param robot_radius: the robot radius in meter
        :return:
        """
        # 1) Threshold map
        ret, threshed_image = cv2.threshold(self._map, 250, 255, cv2.THRESH_BINARY)
        #cv2.imshow('thresh image', threshed_image)
        #cv2.waitKey(0)

        # 2) Map erosion and dilation
        eroded_image = cv2.erode(threshed_image, np.ones((3, 3), np.uint8), borderType=cv2.BORDER_REFLECT)
        #cv2.imshow('eroded image', threshed_image)
        #cv2.waitKey(0)

        dilated_image = cv2.dilate(eroded_image, np.ones((3, 3), np.uint8))
        #cv2.imshow('dilate image', threshed_image)
        #cv2.waitKey(0)

        # 3) Find contours
        (image_width, image_height) = dilated_image.shape
        contour_image = np.array([0 for _ in range(image_width * image_height)], dtype='uint8').reshape((image_width, image_height))

        contours, hierarchy = cv2.findContours(dilated_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        # 4) Find the building contour (it is assumed to be the longest one)
        l_contour_index, l_contour = max(enumerate(contours), key=lambda v: cv2.arcLength(v[1], closed=False))
        #  5) Filled the area outside the building's contour
        cv2.drawContours(contour_image, contours, contourIdx=l_contour_index, color=255, thickness=cv2.FILLED)
        #cv2.imshow('external contour image', contour_image)
        #cv2.waitKey(0)

        # 6) Draw only contours inside the longest one and fill them (hierarchy = [Next, Previous, First_Child, Parent])
        filled_image = contour_image.copy()
        enumerate_hierarchy = list(enumerate(hierarchy[0]))

        def draw_internal_contours(e_hierarchy: Tuple[int, List]):
            index = e_hierarchy[0]
            hierarchy_data = e_hierarchy[1]

            # Draw and fill contour
            cv2.drawContours(filled_image, [contours[index]], contourIdx=-1, color=0, thickness=cv2.FILLED)

            # If this contour has a next one at the same hierarchy level
            if hierarchy_data[0] != -1:
                draw_internal_contours(enumerate_hierarchy[hierarchy_data[0]])

            # If this contour has a child
            if hierarchy_data[2] != -1:
                draw_internal_contours(enumerate_hierarchy[hierarchy_data[2]])

        # Get first child of the external contour and all the internal contours are drawn and black filled
        fist_child = hierarchy[0][l_contour_index][2]
        draw_internal_contours(enumerate_hierarchy[fist_child])
        #cv2.imshow('filled image', filled_image)
        #cv2.waitKey(0)

        # 7) Find new simplified contours in the filled image (in this way, t
        contours, hierarchy = cv2.findContours(filled_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        # 8) The voronoi diagram is calculated using Delaunay triangulation
        rect = (0, 0, self._map.shape[1], self._map.shape[0])
        subdiv = cv2.Subdiv2D(rect)

        for contour, contour_hierarchy in zip(contours, hierarchy[0]):
            # Insert the all contours' points into subdiv
            for point in [np.array(p[0], dtype=float) for p in contour]:
                subdiv.insert(point)

        # 9) Draw voronoi facets contours and create the voronoi bitmap
        voronoi_bitmap = np.array([255 for _ in range(image_width * image_height)], dtype=np.uint8).reshape((image_width, image_height))
        (facets, centers) = subdiv.getVoronoiFacetList([])

        for facet in facets:
            facet_points = np.array(facet, int)

            # Draw voronoi facets contour lines only if they are inside image boundaries
            facet_lines = zip(np.roll(facet_points, 1, axis=0), facet_points)

            for p1, p2 in facet_lines:
                if 0 <= p1[0] < contour_image.shape[1] and 0 <= p1[1] < contour_image.shape[0] and \
                        0 < p2[0] < contour_image.shape[1] and 0 < p2[1] < contour_image.shape[0] \
                        and filled_image[p1[1], p1[0]] > 0 and filled_image[p2[1], p2[0]] > 0:
                    cv2.line(voronoi_bitmap, p1, p2, color=0, thickness=1)

        #cv2.imshow('voronoi bitmap', voronoi_bitmap)
        #cv2.waitKey()

        # 10) The voronoi bitmap is dilated and then the its skeleton are found
        dilated_voronoi_bitmap = cv2.bitwise_not(voronoi_bitmap)
        dilated_voronoi_bitmap = cv2.dilate(dilated_voronoi_bitmap, kernel=np.ones((9, 9), dtype=np.uint8))
        #cv2.imshow('dilated voronoi bitmap', dilated_voronoi_bitmap)
        #cv2.waitKey()

        dilated_voronoi_bitmap[dilated_voronoi_bitmap == 255] = 1
        skeleton_voronoi_bitmap = (skeletonize(dilated_voronoi_bitmap) * 255).astype(np.uint8)
        skeleton_voronoi_bitmap = cv2.bitwise_not(skeleton_voronoi_bitmap)

        # The dilation operation may ahve joined different voronoi line, so this operation discard all point in a wrong area (outside the building and over an obstacle)
        skeleton_voronoi_bitmap[(skeleton_voronoi_bitmap == 0) & (filled_image == 0)] = 255
        #cv2.imshow('dilated voronoi bitmap', skeleton_voronoi_bitmap)
        #cv2.waitKey()

        # 11) Discard the pixels too close to an obstacle
        for (x, y) in np.ndindex(skeleton_voronoi_bitmap.shape[:2]):
            if skeleton_voronoi_bitmap[x, y] == 0:
                image_origin = self._map_metadata['origin']
                scale = self._map_metadata['scale']

                x_real = (x - image_origin[0]) * scale
                y_real = (y - image_origin[1]) * scale

                # Find the 8 points in the circumference centered in (x_real, y_real) with radius = robot_radius
                angles = [(2 * k * np.pi) / 8 for k in range(8)]
                real_coordinates = [(robot_radius * np.cos(a) + x_real, robot_radius * np.sin(a) + y_real) for a in angles]
                pixel_coordinates = [(round(x_real_p / scale + image_origin[0]), round(y_real_p / scale + image_origin[1])) for x_real_p, y_real_p in real_coordinates]

                for x1, y1 in pixel_coordinates + [(x, y)]:
                    if filled_image[x1, y1] == 0:
                        skeleton_voronoi_bitmap[x, y] = 255
                        break

        self._voronoi_bitmap = skeleton_voronoi_bitmap

        if save_to_file:
            # Save voronoi bitmap
            cv2.imwrite(os.path.join(
                os.path.dirname(__file__), 'data', 'voronoi_bitmaps', GibsonAssetsUtilities.GET_FILE_NAME(self._env_name, self._floor) + '.png'),
                self._voronoi_bitmap)

            # Save map + voronoi bitmap
            map_voronoi_bitmap = filled_image.copy()
            map_voronoi_bitmap[self._voronoi_bitmap == 0] = 0
            cv2.imwrite(os.path.join(
                os.path.dirname(__file__), 'data', 'maps_with_voronoi_bitmaps', GibsonAssetsUtilities.GET_FILE_NAME(self._env_name, self._floor) + '.png'),
                map_voronoi_bitmap)

        return self._voronoi_bitmap

    def generate_voronoi_graph(self):
        """
        Extracts the graph from voronoi bitmap.
        The graph can be composed by multiple connected components, the graph entity stores all of them.
        Typically the robot positions are chosen from the longest one.
        :return: the graph
        """
        import sys
        sys.setrecursionlimit(10000)
        #cv2.imshow('voronoi bitmap', self._voronoi_bitmap)
        #cv2.waitKey()

        # Creates graph nodes converting black pixels
        for x, y in np.ndindex(self._voronoi_bitmap.shape[:2]):
            # If the pixel is black, it represents a graph node
            if self._voronoi_bitmap[x, y] == 0:
                 node = Node(x_image=x, y_image=y, map_origin=self._map_metadata['origin'], scale=self._map_metadata['scale'])
                 self._graph.add_node(node)

        # Search connection between nodes
        # Two nodes are connected it their image coordinates are adjacent
        # For each node, its surroundings is checked to find other black pixels (that are connected nodes).
        nodes = self._graph.get_nodes()
        for node in nodes.values():
            x, y = node.get_image_coordinates()
            mask_indexes = [(x1, y1)
                            for x1 in range(max(0, x - 1), min(x + 2, self._voronoi_bitmap.shape[0]))
                            for y1 in range(max(0, y - 1), min(y + 2, self._voronoi_bitmap.shape[1]))
                            if x1 != x or y1 != y]
            for x1, y1 in mask_indexes:
                if self._voronoi_bitmap[x1, y1] == 0:
                    self._graph.add_connection(node1_coordinates=(x, y), node2_coordinates=(x1, y1))

        self._graph.find_connected_components()

        return self._graph















