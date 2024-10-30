---
sidebar_position: 8
slug: conda
---

# Conda

## Activating conda itself in Discovery
Let's first check if the `conda` itself is loaded.
```sh
module list
```
If it doesn't list something like `anaconda3/2022.05`, you would first have to load the `anaconda3` module.
```sh
module load anaconda3/2022.05
```


## Creating a new conda environment
```sh
conda create --prefix ~/your/path/to/conda/environment/newproject python=3.12
```

## Activating an environment
In Discovery, you need to use `source activate` instead of `conda activate`.
```sh
source activate ~/your/path/to/conda/environment/newproject
```

## Installing packages to an environment
```sh
# After activating an environment
conda install networkx numpy matplotlib scipy
```

## Show list of packages installed in the current environment
```sh
conda list
```