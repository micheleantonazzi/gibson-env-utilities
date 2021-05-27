from matplotlib import pyplot as plt

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities

GibsonAssetsUtilities().create_floor_map(env_name='house1', floor=0, image_size=(640, 480), save_to_image=True)
plt.show()