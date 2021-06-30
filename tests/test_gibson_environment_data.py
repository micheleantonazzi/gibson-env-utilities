from gibson_env_utilities.gibson_environments_data import GibsonEnvironmentsData


def test_get_data():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_data().keys()) == 666

    assert data.get_environments_data()['house1'] == data.get_environment_data('house1')


def test_get_semantic_environments():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_with_semantics()) == 89


def test_get_environments_name():
    data = GibsonEnvironmentsData()
    assert len(data.get_env_names()) == 666
