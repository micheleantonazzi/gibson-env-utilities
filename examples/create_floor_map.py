from matplotlib import pyplot as plt

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities

GibsonAssetsUtilities().create_floor_map(environment_name='house1', floor=0, save_to_image=False)
plt.show()