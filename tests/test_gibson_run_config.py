import inspect
import os

import pytest
import yaml
from gibson.envs.mobile_robots_env import TurtlebotNavigateEnv

from gibson_env_utilities.gibson_run_config import GibsonConfigRun, EnvironmentNotSemanticallyAnnotatedException


def test_constructor():
    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='Allensville', floor=0)
    assert 'semantics' not in config.get_parameters()['output']
    assert 'SEMANTICS' not in config.get_parameters()['ui_components']

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='space7', floor=0)
    assert 'semantics' in config.get_parameters()['output']
    assert 'SEMANTICS' in config.get_parameters()['ui_components']

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='house1', floor=0)
    assert 'semantics' in config.get_parameters()['output']
    assert 'SEMANTICS' in config.get_parameters()['ui_components']


def test_get_parameters_and_write_to_file():
    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='Allensville', floor=0)
    config.write_to_file()
    with open(os.path.join(os.path.dirname(inspect.getfile(GibsonConfigRun)), 'data', 'gibson_config_file_temp.yaml'), mode='r') as config_file:
        loaded_parameters = yaml.load(config_file)

    assert loaded_parameters == config.get_parameters()


def test_is_discrete():
    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='Allensville', floor=0).is_discrete(False)

    assert not config.get_parameters()['is_discrete']


def test_remove_semantic():
    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='house1', floor=0).is_discrete(False).remove_semantics()

    assert 'semantics' not in config.get_parameters()['output']
    assert 'SEMANTICS' not in config.get_parameters()['ui_components']


def test_set_semantics_to_random_color():
    with pytest.raises(EnvironmentNotSemanticallyAnnotatedException):
        GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='Allensville', floor=0).set_semantics_to_random_color()

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='house1', floor=0).set_semantics_to_random_color()
    assert config.get_parameters()['semantic_color'] == 1

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='space7', floor=0).set_semantics_to_random_color()
    assert config.get_parameters()['semantic_color'] == 1


def test_set_semantic_label_to_color():
    with pytest.raises(EnvironmentNotSemanticallyAnnotatedException):
        GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='Allensville', floor=0).set_semantic_labels_to_color()

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='house1', floor=0).set_semantic_labels_to_color()
    assert config.get_parameters()['semantic_color'] == 2

    config = GibsonConfigRun(simulation_env=TurtlebotNavigateEnv, world_name='space7', floor=0).set_semantic_labels_to_color()
    assert config.get_parameters()['semantic_color'] == 3

