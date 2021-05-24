import os

from gibson.assets.assets_manager import AssetsManager, AssetsPathNotSetException

from gibson_env_utilities.assets_manager.gibson_assets_manager import GibsonAssetsManager

assets_manager = GibsonAssetsManager()


def test_load_obj():
    mesh = assets_manager.load_obj('space7')
    assert len(sum(map(lambda material: material.vertices, mesh.materials.values()), [])) == 3789552