from matplotlib import pyplot as plt

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities

GibsonAssetsUtilities().create_floor_map(env_name='house80', floor=0, image_size='auto', save_to_file=False)
plt.show()