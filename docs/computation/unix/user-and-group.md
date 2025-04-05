---
title: User and Group
sidebar_position: 3
slug: user-and-group
---

## User

Checking your username
```sh
whoami
```

List all users logged into the server
```sh
who
```

## Groups
Groups in Unix systems are used for multiple purposes, including controlling access to files and directories, and limiting executing of some binaries. A user could be assigned to multiple groups.

In HPC clusters, groups are also used to grant accesses to a specific partition on Slurm, which is the job management software.

Listing groups an user is assigned to.
```sh
groups <username>
```