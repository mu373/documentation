---
title: Custom module
sidebar_position: 7
slug: custom-module
---

Once you have installed a software for yourself, you can use the `module` tool to control the usage of the software. The advantage of not directly adding binary paths to `PATH` is that you have control to deciding when to load the software to the environment.

## Setting up a custom module directory

Custom module files can be created and stored anywhere, but let's use the `~/discovery/modulefile/` directory for here.

```sh
# If you don't have ~/discovery/modulefile/ directory
mkdir -p ~/discovery/modulefile
```

Add this to your shell configuration file, i.e., `.bashrc`. This tells the `module` command that your custom module files are stored at the specific directory.
```sh
module use --append ~/discovery/modulefile
```

## Making a custom module file

Once you've created a directory to store custom modules, let's add one by making a new modulefile at `~/discovery/modulefiles/your_software_name/your_version`.

The following is an example for loading mamba, that I have separately installed. (You need to install the software manually to be able to run commands like `mamba install pandas`!)

```txt title="Modulefile for mamba:1.5.9"
#%Module

module-whatis "Loads Mamba 1.5.9 module.

mamba is a reimplementation of the conda package manager in C++.
mamba version: 1.5.9

To load the module, type:
module load ~/discovery/modulefiles/mamba/1.5.9

To activate the base environment, type:
source activate <env_path>

Note - make sure to deactivate any existing conda environments in your path before loading this module. Check your ~/.bashrc for any initialization scripts, and remove them.

To create a virtual environmnet, follow instructions:
https://rc-docs.northeastern.edu/en/latest/software/conda.html#creating-a-conda-virtual-environment-with-anaconda
"

conflict         mamba
prepend-path     PATH ~/miniforge3/bin
prepend-path     PATH ~/miniforge3/sbin
prepend-path     MANPATH ~/miniforge3/man
prepend-path     MANPATH ~/miniforge3/share/man
prepend-path     LD_LIBRARY_PATH ~/miniforge3/lib
prepend-path     CPATH ~/miniforge3/include
prepend-path     LIBRARY_PATH ~/miniforge3/lib
```