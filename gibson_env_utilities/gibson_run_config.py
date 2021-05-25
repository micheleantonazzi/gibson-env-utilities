import os
import yaml

from gibson_env_utilities.gibson_environments_data import GibsonEnvironmentsData


class GibsonConfigRun:
    def __init__(self):
        self._gibson_environments_data = GibsonEnvironmentsData()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'gibson_config_file.yaml'), mode='r') as config_file:
            self._gibson_config_parameters = yaml.load(config_file)

    def set_environment_name_and_floor(self, environment_name: str, floor: int) -> 'GibsonConfigRun':
        """
        Sets the environment to load.
        This methods automatically sets the starting position and orientation according to the values specified in the environments_data.yaml file.
        :param environment_name: the name of the environment
        :type environment_name: str
        :param floor: the floor where to place the robot
        :return: GibsonConfigClass
        """
        env_data = self._gibson_environments_data.get_environment_data(environment_name=environment_name)
        self._gibson_config_parameters['model_id'] = environment_name
        self._gibson_config_parameters['initial_pos'] = env_data[GibsonEnvironmentsData.KEY_FLOORS][floor][GibsonEnvironmentsData.KEY_POSITION]
        self._gibson_config_parameters['initial_orn'] = env_data[GibsonEnvironmentsData.KEY_FLOORS][floor][GibsonEnvironmentsData.KEY_ORIENTATION]

        return self

    def is_discrete(self, discrete: bool) -> 'GibsonConfigRun':
        """
        Sets the discrete parameters. It mus be True if the simulator is used with the PLAY utility, otherwise it must be False
        :param discrete:
        :return:
        """
        self._gibson_config_parameters['is_discrete'] = discrete
        return self

    def write_to_file(self) -> str:
        """
        Writes the specified configuration in a temporary file and returns its path.
        :return: the file's path which contains the set configuration
        """
        save_path = os.path.join(os.path.dirname(__file__), 'data', 'gibson_config_file_temp.yaml')
        with open(save_path, mode='w') as gibson_config_file_temp:
            yaml.dump(self._gibson_config_parameters, gibson_config_file_temp, default_flow_style=False)

        return save_path