---
title: Managing resources
sidebar_position: 10
slug: resource
---

## Computing resource

### Realtime CPU, RAM usage
To check for the realtime usage of CPU, memory by users and processes, you can use `htop`.
```sh
htop
```

### GPU
If you are using a NVIDIA GPU and want to check the status of it, you can use `nvidia-smi`. "SMI" stands for System Management Interface.
```sh
nvidia-smi
```

## Processes

### Listing processes
To list all processes that are running under your username, we use `ps` command. The `aux` option is the combination of three flags, `a`, `u`, and `x`.
```sh
ps aux
```

You ca

### Kill process
You can kill your process using the `kill` command.
```sh
kill <process_id>
```


## Directory file size
To check for the total file size of a specific directory,
```sh
du -d 1 -h
```

- `-d`: Depth of the tree structure that you want to calculate the file size of. If you set `-d 0` (which is equivalent to `-s`), it will show the total file size of the current directory. 
- `-h`: Shows file size in human readable units, such as MB and GB.

## Uptime
```sh
uptime
```