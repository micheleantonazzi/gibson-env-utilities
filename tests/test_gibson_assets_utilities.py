import pytest

from gibson_env_utilities.assets_utilities.gibson_assets_utilities import GibsonAssetsUtilities

assets_manager = GibsonAssetsUtilities()


def test_load_obj():
    assets_manager.load_obj('space7')
    assets_manager.load_obj('house1')

    with pytest.raises(FileNotFoundError):
        assets_manager.load_obj('house-1')
