import pywavefront
from gibson.assets.assets_manager import AssetsManager
import os

from pywavefront import visualization


class GibsonAssetsManager:
    def __init__(self):
        self._assets_manager = AssetsManager()

    def load_obj(self, environment_name: str):
        """
        Loads and returns the specified environment obj file
        :param environment_name: the name of the environment whose wavefront file is to be loaded
        :type environment_name: str
        :return:
        """

        obj_path = os.path.join(self._assets_manager.get_assets_path(), environment_name, 'mesh_z_up.obj')
        mesh = pywavefront.Wavefront(obj_path)
        visualization.draw(mesh)