import os

from gibson.assets.assets_manager import AssetsManager, AssetsPathNotSetException

from gibson_env_utilities.assets_manager.gibson_assets_manager import GibsonAssetsManager

try:
    assets_path = AssetsManager().get_assets_path()
except AssetsPathNotSetException:
    assets_path = os.path.dirname(__file__)

assets_manager = GibsonAssetsManager(assets_path=assets_path)


def test_load_obj():
    assets_manager.load_obj('space7')