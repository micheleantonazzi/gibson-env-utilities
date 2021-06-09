import cv2
import numpy as np
from gibson.envs.no_physiscs_env import TurtlebotNavigateNoPhysicsEnv
import argparse

from gibson_env_utilities.gibson_run_config import GibsonConfigRun
from gibson_env_utilities.voronoi_graph_generator import VoronoiGraphGenerator

config_file = GibsonConfigRun(simulation_env=TurtlebotNavigateNoPhysicsEnv, world_name='house1', floor=0) \
    .is_discrete(False).remove_semantics().write_to_file()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=config_file)
    args = parser.parse_args()

    # Get positions using voronoi graph
    voronoi_graph_generator = VoronoiGraphGenerator(env_name='house1', floor=0)
    voronoi_graph_generator.generate_voronoi_bitmap(save_to_file=False)
    graph = voronoi_graph_generator.get_voronoi_graph()
    positions = graph.get_real_position(0.10)
    house1_map = voronoi_graph_generator.get_map()
    for position in positions:
        house1_map[position.to_img_index()] = 127
    cv2.imshow('map with selected positions', house1_map)
    cv2.waitKey()

    env = TurtlebotNavigateNoPhysicsEnv(config=args.config)
    env.reset()
    env.robot.set_position([0, 0, 0])

    for position in positions:
        # Remember to call env.step before every robot position change
        env.step([0.0, 0.0])
        x, y = position.to_real_point()
        env.robot.set_position([x, y, 0.2])

        for _ in range(5):
            env.step([0.0, 0.0])
            env.robot.turn_right(delta=0.1)
