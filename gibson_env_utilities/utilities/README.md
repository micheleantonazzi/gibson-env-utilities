# Gibson utilities

This module offers a lot of useful utilities which facilitate the use of Gibson.

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
