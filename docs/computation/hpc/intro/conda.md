---
sidebar_position: 8
slug: conda
tags:
  - conda
---

# Anaconda

## What is Anaconda? {#about}

[Anaconda](https://www.anaconda.com/download) is a Python and R distribution, primarily designed for data science and scientific computing. It comes with popular packages―i.e.,  NumPy, pandas, and matplotlib―pre-installed, so it works "out of the box" without complex configurations.

[conda](https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html) is an open-source package and environment manager that comes with Anaconda. 
- As a **package manager**, it resolves dependencies, downloads, installs, and updates Python packages
- As an **environment manager**, it allows you to **create an isolated "virtual environment"** for projects. The advantage of using an virtual environment is that you can have different packages and versions of them for each project without affecting other projects or the entire system. For example, you can have Python 3.6 and NumPy v1.1 for one project and Python 3.12 and NumPy v2.1 for an another project.

:::note
There is a faster alternative to conda called **mamba**, which is an reimplementation of conda in C++. It offers faster downloads and dependency resolving while retaining compatibility to conda. While it is not available on Discovery by default, you can use it by installing it by yourself. [See here](https://github.com/mamba-org/mamba) for more information on mamba.
:::


## Using conda in Discovery {#discovery}

### Anaconda is not loaded by default
By default, the `conda` command is not accessible at the initial state when the users login to their shell.

```shell-session
$ conda
bash: conda: command not found
```

You can confirm that the `anaconda3` module, which includes `conda` command, is not yet loaded by printing the list of loaded modules. The only default module loaded is the `discovery` module.
```shell-session
$ module list
Currently Loaded Modulefiles:
  1) discovery/2021-10-06
```

### Loading Anaconda module {#load-module}
To use `conda` command, load the `anaconda3` module as follows. `/2022.05` specifies the version of the software.
```sh
module load anaconda3/2022.05
```

After loading, the `conda` command should now be ready to use.
```shell-session
$ module list
Currently Loaded Modulefiles:
  1) discovery/2021-10-06   2) anaconda3/2022.05
```
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


## `conda` commands {#commands}

Here are some of the frequently used commands for `conda`.

### Creating a new conda environment {#conda-create}
This command will create a new conda environment at a specified location, with Python 3.12.
```sh
conda create --name newproject --prefix ~/your/path/to/conda/environment/newproject python=3.12
```

### Activating an environment {#conda-activate}
Whenever you want to use the conda environment, you would have to "activate" it.
In Discovery, use `source activate` instead of `conda activate`.
```sh
source activate ~/your/path/to/conda/environment/newproject
```

### Installing packages to an environment {#conda-install}
```sh
# After activating an conda environment
conda install networkx numpy matplotlib scipy
```

### Showing list of packages installed in the current environment {#conda-list}
```sh
conda list
```

### Showing list of environments {#conda-env-list}
```sh
conda env list
```

### Importing and exporting an environment {#conda-env-export}
You can share the virtual environment with other people, so that they can reproduce the same environment for running your codes.
```sh
# Export
conda env export -p ~/your/path/to/conda/environment/foo > conda_env_foo.yml

# Import (Create a new environment from YAML)
conda env create -f=conda_env_foo.yml
```


:::tip
Here's the [official cheatsheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) of conda.
:::