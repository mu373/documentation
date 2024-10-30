---
sidebar_position: 7
slug: custom-module
---

# Custom module

Once you have installed a software for yourself, you can use `module` to control the usage of the software. The advantage of not directly adding binary paths to PATH is that you have control to when to make the software available.

## Setting up custom module path

We can create custom modules 
It can be stored anywhere, but let's use the `~/discovery/modulefile/` directory for here.

```sh
# If you don't have ~/discovery/modulefile/ directory
mkdir -p ~/discovery/modulefile
```

Add this to your shell configuration file, i.e., `.bashrc`. This tells the `module` that your custom module files are stored at the specific directory.
```sh
module use --append ~/discovery/modulefile
```

## Making Module file
Make a modulefile at path `~/discovery/modulefiles/your_software_name/your_version`.

```txt title="Modulefile for mamba:1.5.9"
#%Module

module-whatis "Loads Mamba 1.5.9 module.

mamba is a reimplementation of the conda package manager in C++.
mamba version: 1.5.9
Source description from: https://spack.io/

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