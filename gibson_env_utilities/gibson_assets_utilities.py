import os
from functools import reduce
from typing import Tuple

import yaml
from matplotlib.figure import Figure
import numpy as np
import trimesh
from gibson.assets.assets_manager import AssetsManager
from matplotlib import pyplot as plt
from termcolor import colored

from gibson_env_utilities.gibson_environments_data import GibsonEnvironmentsData


class GibsonAssetsUtilities:
    def __init__(self):
        self._assets_path = AssetsManager().get_assets_path()
        self._environments_data = GibsonEnvironmentsData()

    def load_obj(self, environment_name: str) -> trimesh.Trimesh:
        """
        Loads and returns the specified environment obj file
        :param environment_name: the name of the environment whose wavefront file is to be loaded
        :type environment_name: str
        :return: the mesh stored in the obj file
        :rtype: trimesh.Trimesh
        """

        obj_path = os.path.join(self._assets_path, 'dataset', environment_name, 'mesh_z_up.obj')
        if not os.path.exists(obj_path):
            print(colored('The specified object file does not exists!!', 'red'))
            raise FileNotFoundError(obj_path)

        mesh = trimesh.load_mesh(obj_path, file_type='obj')

        # If the loaded onj file generates a scene, the meshes inside it must be concatenated
        if isinstance(mesh, trimesh.Scene):
            mesh = reduce(lambda mesh1, mesh2: trimesh.util.concatenate(mesh1, mesh2), list(mesh.geometry.values()))

        return mesh

    def create_floor_map(self, environment_name: str, floor: int, image_size: Tuple[int, int] = (640, 480), floor_offset: float = 0.10, height: float = 1.0, step: float = 0.10, save_to_image: bool = False):
        """
        Generates the map of the environment at the given floor and the relative metadata.
        The floor map is a png image, while metadata indicates:
            1) the pixel coordinates to the origin point (0.0, 0.0)
            2) the scale to map a pixel to the real-world distance it covers
        To generate the map, the mesh is sliced at multiple heights.
        The cuts begin from the floor offset and they are made at each step up to the maximum height.
        :param environment_name:
        :param floor:
        :param floor_offset: the offset to start cutting the mesh (the first cross section is performed at [floor_height + floor_offset]
        :type floor_offset: float
        :param image_size: the size of the map image in pixel
        :type image_size: Tuple[int, int]
        :param height: the maximum height to stop cutting the mesh. This means that the last mesh cut has is made at [floor_height + floor_offset + height]
        :type height: float
        :param step: the step used to cut the environment's mesh
        :type step: float
        :param save_to_image
        :type save_to_image: bool
        :return: None
        """
        mesh = self.load_obj(environment_name=environment_name)

        origin = self._environments_data.get_environment_data(environment_name)[GibsonEnvironmentsData.KEY_FLOORS][floor][GibsonEnvironmentsData.KEY_POSITION]
        origin[2] += floor_offset
        slices_2D = mesh.section_multiplane(plane_origin=origin, plane_normal=[0, 0, 1], heights=np.arange(0.0, height, step).tolist())

        plt.close()
        plt.axis('off')

        for slice in slices_2D:
            slice.plot_entities(show=False, annotations=True, color='k')

        fig: Figure = plt.gcf()
        fig.set_size_inches(image_size[0] / 100.0, image_size[1] / 100.0)
        fig.canvas.draw()

        # Extract metadata
        ax = fig.gca()
        x_0, y_0 = ax.transData.transform((0.0, 0.0))
        x_1, y_1 = ax.transData.transform((1.0, 0.0))
        scale = abs(x_0 - x_1) / 100
        metadata = {'origin': (int(x_0), int(y_0)), 'scale': float(round(scale, 4))}
        print(metadata)

        if save_to_image:
            file_name = environment_name + '_floor_' + str(floor)
            fig.savefig(os.path.join(os.path.dirname(__file__), 'data', 'maps', file_name + '.png'), dpi=1000)
            with open(os.path.join(os.path.dirname(__file__), 'data', 'maps_metadata', file_name + '.yaml'), mode='w') as f:
                yaml.dump(metadata, f, default_flow_style=False)