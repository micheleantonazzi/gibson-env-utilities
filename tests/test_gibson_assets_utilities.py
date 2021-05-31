import pytest

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities

assets_manager = GibsonAssetsUtilities()


def test_load_obj():
    assets_manager.load_obj('space7')
    assets_manager.load_obj('house1')

    with pytest.raises(FileNotFoundError):
        assets_manager.load_obj('house-1')


def test_create_floor_map():
    GibsonAssetsUtilities().create_floor_map(env_name='house1', floor=0, image_size=(500, 500), save_to_file=True)
    GibsonAssetsUtilities().create_floor_map(env_name='house1', floor=0, save_to_file=True)
    GibsonAssetsUtilities().create_floor_map(env_name='space7', floor=0, save_to_file=True)


def test_load_map_and_metadata():
    GibsonAssetsUtilities().load_map_and_metadata(env_name='house1', floor=0)
