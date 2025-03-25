---
sidebar_position: 8
slug: slurm
tags:
  - Slurm
---

# Slurm

## What is Slurm?

## Types of jobs
- Interactive jobs
- Batch jobs


## Controlling jobs

### Starting an interactive job
```sh
srun --job-name sample-job --time 01:00:00 --pty bash -i
```

### Add a batch job

```sh title="hello.sh"
#!/bin/bash
echo "Hello!"
```

```sh
sbatch -p express hello.sh
```

### List all job queues
```sh
# By default, it lists jobs by all users
squeue

# If you only want to see your jobs, use the -u option with the $USER environment variable.
squeue -u $USER
```

### Cancel a job
```sh
scancel <jobid>
```

## Partition and Nodes

Show all partitions in the cluster.
```sh
scontrol show partition
```

Get list of nodes in a specific partition
```sh
sinfo -p short
```

## Additional resources
- Research Computing, University of Colorado Boulder. Running Applications with Jobs. https://curc.readthedocs.io/en/latest/running-jobs/running-apps-with-jobs.html
- Center for Research Computing, NYU Abu Dhabi. Quick Intro to Job Submission. https://crc-docs.abudhabi.nyu.edu/hpc/jobs/quick_start.html.