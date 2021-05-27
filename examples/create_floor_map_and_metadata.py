from matplotlib import pyplot as plt

from gibson_env_utilities.gibson_assets_utilities import GibsonAssetsUtilities

GibsonAssetsUtilities().create_floor_map(env_name='space7', floor=0, image_size=(1024, 1024), save_to_image=True)
plt.show()