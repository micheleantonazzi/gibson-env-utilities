from gibson_env_utilities.environments_data.gibson_environments_data import GibsonEnvironmentsData


def test_get_data():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_data().keys()) == 665


def test_get_semantic_environments():
    data = GibsonEnvironmentsData()
    assert len(data.get_environments_with_semantics()) == 88