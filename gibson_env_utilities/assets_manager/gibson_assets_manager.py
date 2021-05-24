import pywavefront
import os


class GibsonAssetsManager:
    def __init__(self, assets_path: str):
        self._assets_path = assets_path

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