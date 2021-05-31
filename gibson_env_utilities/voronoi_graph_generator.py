import operator
import random
from typing import List, Tuple

import cv2
import numpy as np
from termcolor import colored

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities


class VoronoiGraphGenerator:
    def __init__(self, env_name: str, floor: int):
        self._assets_manager = GibsonAssetsUtilities()
        try:
            self._map, self._map_metadata = self._assets_manager.load_map_and_metadata(env_name=env_name, floor=floor)
        except FileNotFoundError:
            print(colored('The map or its metadata of the {0} world do not exist: they will be generated using the default parameters!'.format(env_name), red))
            self._assets_manager.create_floor_map(env_name=env_name, floor=floor)
            self._map, self._map_metadata = self._assets_manager.load_map_and_metadata(env_name=env_name, floor=floor)

        self._map = cv2.cvtColor(self._map, cv2.COLOR_RGB2GRAY)

    def rect_contains(self, rect, point) :
        if point[0] < rect[0]:
            return False
        elif point[1] < rect[1]:
            return False
        elif point[0] > rect[2]:
            return False
        elif point[1] > rect[3]:
            return False
        return True

    def draw_voronoi(self, img, subdiv) :

        (facets, centers) = subdiv.getVoronoiFacetList([])

        for i in range(0,len(facets)) :
            ifacet_arr = []
            for f in facets[i] :
                ifacet_arr.append(f)

            ifacet = np.array(ifacet_arr, np.int)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            cv2.fillConvexPoly(img, ifacet, color, 0, 0)
            ifacets = np.array([ifacet])
            cv2.polylines(img, ifacets, True, (0, 0, 0), 1, 0, 0)
            cv2.circle(img, (int(centers[i][0]), int(centers[i][1])), 3, (0, 0, 0), 0, 0, 0)

    def generate_voronoi_graph(self):
        # Threshold map
        ret, threshed_image = cv2.threshold(self._map, 250, 255, cv2.THRESH_BINARY)

        #cv2.imshow('thresh image', threshed_image)
        #cv2.waitKey(0)

        threshed_image = cv2.erode(threshed_image, np.ones((3, 3), np.uint8), borderType=cv2.BORDER_REFLECT)
        #cv2.imshow('eroded image', threshed_image)
        #cv2.waitKey(0)

        threshed_image = cv2.dilate(threshed_image, np.ones((3, 3), np.uint8))
        #cv2.imshow('dilate image', threshed_image)
        #cv2.waitKey(0)

        # Find contours
        (image_width, image_height) = threshed_image.shape
        contour_image = np.array([0 for _ in range(image_width * image_height)], dtype='uint8').reshape((image_width, image_height))

        contours, hierarchy = cv2.findContours(threshed_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        # Find the building contour (it is assumed to be the longest one)
        l_contour_index, l_contour = max(enumerate(contours), key=lambda v: cv2.arcLength(v[1], closed=True))
        cv2.drawContours(contour_image, contours, contourIdx=l_contour_index, color=255, thickness=cv2.FILLED)
        #cv2.imshow('external contour image', contour_image)
        #cv2.waitKey(0)

        # Draw only contour inside the longest one and fill them (hierarchy = [Next, Previous, First_Child, Parent])
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

        # Get first child of the external contour
        fist_child = hierarchy[0][l_contour_index][2]
        draw_internal_contours(enumerate_hierarchy[fist_child])
        #cv2.imshow('filled image', filled_image)
        #cv2.waitKey(0)

        # Find new contours in the filled image (in this way, t
        new_contour_image = np.array([255 for _ in range(image_width * image_height)], dtype='uint8').reshape((image_width, image_height))
        contours, hierarchy = cv2.findContours(filled_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(new_contour_image, contours, contourIdx=-1, thickness=1, color=0)
        #cv2.imshow('contours in the filled image image', new_contour_image)
        #cv2.waitKey(0)

        # Delaunay triangulation
        rect = (0, 0, self._map.shape[1], self._map.shape[0])
        subdiv = cv2.Subdiv2D(rect)

        for contour, contour_hierarchy in zip(contours, hierarchy[0]):
            # Insert the all contours' points into subdiv
            for point in [np.array(p[0], dtype=np.float) for p in contour]:
                subdiv.insert(point)

        # Draw voronoi facets contours and create the voronoi bitmap
        voronoi_bitmap = filled_image.copy()
        (facets, centers) = subdiv.getVoronoiFacetList([])

        for facet in facets:
            facet_points = np.array(facet, np.int)

            # Draw voronoi facets contour lines only if they are inside image boundaries
            facet_lines = zip(np.roll(facet_points, 1, axis=0), facet_points)

            for p1, p2 in facet_lines:
                if 0 <= p1[0] <= contour_image.shape[1] and 0 <= p1[1] <= contour_image.shape[0] and \
                        0 <= p2[0] <= contour_image.shape[1] and 0 <= p2[1] <= contour_image.shape[0] \
                        and filled_image[p1[1], p1[0]] > 0 and filled_image[p2[1], p2[0]] > 0:
                    cv2.line(voronoi_bitmap, p1, p2, color=127, thickness=1)

        cv2.imshow('voronoi bitmap', voronoi_bitmap)
        cv2.waitKey()








