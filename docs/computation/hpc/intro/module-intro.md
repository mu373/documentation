---
title: Module
sidebar_position: 6
slug: module-intro
---

The ‘modules’ tool is widely used for managing application environments on High-Performance Computing (HPC) systems. This page will provide an overview of ‘modules’, instructions on using them, best practices, use cases, and more.

The module system on the cluster includes many commonly used scientific software packages that you can load into your path when you need them and unload when you no longer need them. In essence, ‘modules’ handle environment variables like PATH and LD_LIBRARY_PATH to avoid conflicts between software applications.


## Basic commands

**Load a module**: This loads the configurations written in the module file.
```sh
module load <module>
```

**Unload a module**: This unloads a specific module file.
```sh
module unload <module>
```
**Unload all modules**: This unloads all loaded modules.
```sh
module purge
```

**Show currently loaded modules**: Used to check which modules are currently active.
```sh
module list
```

**Show module details**
```sh
module show <module>
```

**List all available modules**: Used to check what kinds of modules (or versions) are available in the cluster.
```sh
module avail
```


## Understanding how modules work
Let's take a look at the `discovery` module file, which is loaded a module loaded to Discovery cluster by default. Using the `module show` command, we get something like this. (Note that IP address and port has been modified in the following console output, just for the purpose of explanation.)

```shell-session
$ module show discovery
-------------------------------------------------------------------
/shared/centos7/modulefiles/discovery/2021-10-06:

setenv		 http_proxy http://192.0.2.0:5555
setenv		 https_proxy http://192.0.2.0:5555
setenv		 ftp_proxy http://192.0.2.0:5555
prepend-path	 PATH /shared/centos7/discovery/bin
-------------------------------------------------------------------
```

We can see that it sets three environment variables, in this case specifically for proxy configurations, and adds path to softwares into `PATH`. If we unload this module, the node will not be able to make any external internet access, as Discovery requires the proxies listed above for that purpose.