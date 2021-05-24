import pywavefront
import os

from gibson.assets.assets_manager import AssetsManager, AssetsPathNotSetException
from termcolor import colored


class GibsonAssetsManager:
    def __init__(self):
        try:
            self._assets_path = AssetsManager().get_assets_path()
        except AssetsPathNotSetException:
            print(colored('Gibson assets path is not correctly set! It is set to an example directory, used only for testing! ', 'red'))
        self._assets_path = os.path.dirname(__file__)

    def load_obj(self, environment_name: str) -> pywavefront.Wavefront:
        """
        Loads and returns the specified environment obj file
        :param environment_name: the name of the environment whose wavefront file is to be loaded
        :type environment_name: str
        :return:
        """

        obj_path = os.path.join(self._assets_path, 'dataset', environment_name, 'mesh_z_up.obj')
        mesh = pywavefront.Wavefront(obj_path, create_materials=True)
        return mesh