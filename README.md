# Utilities for Gibson Environment

[![BuildTest](https://github.com/micheleantonazzi/gibson-env-utilities/actions/workflows/build-and-publish.yml/badge.svg?branch=main)](https://github.com/micheleantonazzi/gibson-env-utilities/actions/workflows/build-and-publish.yml)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=coverage)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)



[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=alert_status)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=sqale_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=reliability_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=security_rating)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)
[![](https://sonarcloud.io/api/project_badges/measure?project=micheleantonazzi_gibson-env-utilities&metric=vulnerabilities)](https://sonarcloud.io/dashboard/index/micheleantonazzi_gibson-env-utilities)

This Python library offers a series of utilities for using [GibsonEnv](https://github.com/micheleantonazzi/GibsonEnv.git)

## Environments data
*GibsonEnvironmentsData* implements a series of operations to retrieve and use some information about the worlds in the Gibson's dataset.
This information includes:
* the environment's name
* if the environment is semantically annotated
* for each floor:
    * the approximate height of the floor
    * the starting position
    * the starting orientation

The environments' data are organized in a dictionary, as shown below:

```
[environment's name] -> str (dictionary key)
  |_[dataset] -> str (stanford or matterport)
  |_[has_semantics] -> bool
  |_[floors] -> dict
    |_[number] -> int (dictionay key)
      |_[floor_height] -> float
      |_[position] -> list (the starting position x, y, z)
      |_[orientation] -> list (the starting orientation expressed in gradients x, y, z)

```

## Assets utilities
GibsonAssetsUtilities defines useful methods for:
* save and load assets files from disk
* generate floor map starting from a wavefront file

## Config run
*GibsonConfigRun* is a utility which helps users to configure Gibson to perform a simulation run.
This class creates automatically a configuration file used by Gibson Environment to read the simulation parameters.
You can see this class in action in the correspondent examples ([1](examples/launch_gibson_turtlebot.py) and [2](examples/launch_gibson_turtlebot_no_physics.py)).