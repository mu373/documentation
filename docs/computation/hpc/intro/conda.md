---
sidebar_position: 8
slug: conda
---

# Conda

## What is Anaconda?


## Using anaconda in Discovery
Let's first check if the `conda` itself is loaded. By default, anaconda is not usually loaded on Discovery. 
```sh
module list
```

If it doesn't list something like `anaconda3/2022.05`, you would first have to load the `anaconda3` module.
```sh
module load anaconda3/2022.05
```

Now, `conda` command should be ready to use.
```shell-session
$ conda
usage: conda [-h] [-V] command ...

conda is a tool for managing and deploying applications, environments and packages.

Options:

positional arguments:
  command
    clean        Remove unused packages and caches.
    compare      Compare packages between conda environments.
    config       Modify configuration values in .condarc. This is modeled after the git config command.
                 Writes to the user .condarc file (/home/ueda.m/.condarc) by default.
    create       Create a new conda environment from a list of specified packages.
    info         Display information about current conda install.
    init         Initialize conda for shell interaction. [Experimental]
    install      Installs a list of packages into a specified conda environment.
    list         List linked packages in a conda environment.
    package      Low-level conda package utility. (EXPERIMENTAL)
    remove       Remove a list of packages from a specified conda environment.
    uninstall    Alias for conda remove.
    run          Run an executable in a conda environment.
    search       Search for packages and display associated information. The input is a MatchSpec, a
                 query language for conda packages. See examples below.
    update       Updates conda packages to the latest compatible version.
    upgrade      Alias for conda update.
```
## Commands for conda

### Create a new conda environment {#conda-create}
This command will create a new conda environment at a specified location, with Python 3.12.
```sh
conda create --prefix ~/your/path/to/conda/environment/newproject python=3.12
```

### Activate an environment
Whenever you want to use the conda environment, you would have to "activate" it.
In Discovery, use `source activate` instead of `conda activate`.
```sh
source activate ~/your/path/to/conda/environment/newproject
```

### Intall packages to an environment
```sh
# After activating an environment
conda install networkx numpy matplotlib scipy
```

### Show list of packages installed in the current environment
```sh
conda list
```