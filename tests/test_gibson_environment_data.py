from gibson_env_utilities.assets_utilities.gibson_assets_utilities import GibsonAssetsUtilities
from gibson_env_utilities.assets_utilities.gibson_environments_data import GibsonEnvironmentsData


def test_get_data():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_data().keys()) == 665

    assert data.get_environments_data()['house1'] == data.get_environment_data('house1')


def test_get_semantic_environments():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_with_semantics()) == 88


def test_get_environments_name():
    data = GibsonEnvironmentsData()
    assert len(data.get_environment_names()) == 665


def test_create_floor_map():
    GibsonAssetsUtilities().create_floor_map(environment_name='house1', floor=0, save_to_image=True)
    GibsonAssetsUtilities().create_floor_map(environment_name='space7', floor=0, save_to_image=True)
