import os
from functools import reduce

import trimesh
from gibson.assets.assets_manager import AssetsManager, AssetsPathNotSetException
from termcolor import colored


class GibsonAssetsManager:
    def __init__(self):
        try:
            self._assets_path = AssetsManager().get_assets_path()
        except AssetsPathNotSetException:
            print(colored('Gibson assets path is not correctly set! It is set to an example directory, used only for testing! ', 'red'))
            self._assets_path = os.path.dirname(__file__)

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