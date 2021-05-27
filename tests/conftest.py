import os

from gibson.assets.assets_manager import AssetsManager, AssetsPathNotSetException
from gibson.assets.assets_actions import download_assets_core


def pytest_configure(config):
    try:
        AssetsManager().get_assets_path()
    except AssetsPathNotSetException:
        AssetsManager().set_assets_path(os.path.join(os.path.dirname(__file__), 'assets_test')).save_assets_information()
        download_assets_core()