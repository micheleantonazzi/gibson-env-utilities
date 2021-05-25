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

        # Remove semantics if the environment is not semantically annotated
        if not env_data[GibsonEnvironmentsData.KEY_HAS_SEMANTICS]:
            self.remove_semantics()
        else:
            if env_data[GibsonEnvironmentsData.KEY_DATASET] == 'stanford':
                self._gibson_config_parameters['semantic_source'] = 1
                self._gibson_config_parameters['semantic_color'] = 3
            elif env_data[GibsonEnvironmentsData.KEY_DATASET] == 'matterport':
                self._gibson_config_parameters['semantic_source'] = 2
                self._gibson_config_parameters['semantic_color'] = 2

        return self

    def is_discrete(self, discrete: bool) -> 'GibsonConfigRun':
        """
        Sets the discrete parameters. It must be True if the simulator is used with the PLAY utility, otherwise it must be False.
        :param discrete: the paramater value
        :return: GibsonConfigRun
        """
        self._gibson_config_parameters['is_discrete'] = discrete
        return self

    def remove_semantics(self) -> 'GibsonConfigRun':
        """
        If an environment is semantically annotated, the semantic data are automatically synthesized and shown.
        This method tells Gibson not to produce semantic data.
        :return:
        """
        self._gibson_config_parameters['output'] = ['nonviz_sensor', 'rgb_filled', 'depth']
        self._gibson_config_parameters['ui_components'] = ['RGB_FILLED', 'DEPTH']
        self._gibson_config_parameters['ui_num'] = 2
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