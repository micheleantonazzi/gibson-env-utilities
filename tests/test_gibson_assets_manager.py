from gibson_env_utilities.assets_manager.gibson_assets_manager import GibsonAssetsManager

assets_manager = GibsonAssetsManager()


def test_load_obj():
    assets_manager.load_obj('space7')
