---
sidebar_position: 10
slug: jupyter
---

# Jupyter Lab

You can run your own Jupyter Lab for yourself, without depending on the OOD.

## Getting computing nodes
Let's start by getting a computing node allocated. On Discovery, create a new batch file as following. This batch file specifies the options for the computing node, starts `tmux` and run it until the time limit.

```bash title="tmux.sh"
#!/bin/bash
#============ Slurm Options ===========
#SBATCH --partition=express              # Set the partition that you have access to.
#SBATCH --mail-user=john@example.com     # Enter your email address for job notification
#SBATCH --mail-type=END                  # Send an email when the job ends
#SBATCH --time=1:00:00                   # Set time limit to 1 hour
#SBATCH --output=/home/john/discovery/slurm/logs/slurm-%j.out # Any stdout will be stored here.
#SBATCH --cpus-per-task=1
#=======================================

# Clear current env/modules
module purge

# Load required module from Discovery (required for internet access)
module load discovery

# Activate conda environment, if necessary
source activate /your/path/to/conda/env

# Start a new tmux session with the name "0"
tmux new -d -s "0"

# By default, the batch job will end if all the jobs inside are complete.
# We use the "sleep" command to keep this job running until the time limit
sleep infinity
```

Once you've created the batch file, let's submit the job. This batch file will request for a computing node, and if it's accepted, start a tmux session that lasts until the time limit you've set.
```sh
sbatch tmux.sh
```

Check that the batch has been processed properly using the `squeue` command. If the `ST` column is `R`, it means that the job is running.
```shell-session
$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1234567 express       tmux.sh  john R    00:59:30      1 c0001
```

After confirming that the job is running, you can enter the shell by attaching to the tmux session with the `srun` command. This will open up a `tmux` screen.
```sh
srun --jobid=<your_job_id> --pty tmux a
```

:::tip
Ensure you detach (`<tmux prefix> d`) when you finish using it instead of killing the shell.  
By default, the tmux prefix is `Ctrl-b`. To detatch, you first push `Ctrl-b` first, release the keys, and then type `d`.
:::

Check for the hostname of the allocated computing node using the following command. For Discovery, the hostname for computing nodes are `cXXXX` where `XXXX` is a four-digit number.
```sh
hostname
```

## Installing Jupyter Lab {#install-jupyter}
Now that we've got a computing node allocated, let's dive in to starting Jupyter Lab. If this is your first time using Jupyter Lab in the conda environment that you are using, you might need to install relevant Python packages first. Skip to the [next step](#start-jupyter) if you already installed Jupyter Lab in the conda environment.

Inside the `tmux` session on the computing node, run the following commands.
```sh
# Make sure that you are in the right conda environment
source activate ~/path/to/your/conda/environemnt
conda install jupyter-lab
```

:::note
Follow [tutorials here](/docs/computation/hpc/intro/conda#conda-create) if you want to create a new `conda` environment.
:::

## Starting Jupyter Lab {#start-jupyter}
After installing `jupyter-lab` in the `conda` environment, let's start the Jupyter Lab. After a while, it should show URLs starting with `http://localhost:<some_port>`.
```sh
jupyter lab --no-browser
```

## Port-forwarding on local machine
Since the Jupyter Lab that you just started works in the remote server (computing node), it is not accessible from the browser on your local device, by default. You have to set up **port-forwarding** so that you have access to what's running on the remote server.

There are multiple ways to do this, but let's stick to the most basic way which is through the `ssh` command.

### Setting up port forward with `ssh` command

:::info
You would be working on your local device for this step, not on Discovery!
:::

<!-- #### Set up SSH config -->
Open your local terminal, and make sure that you have SSH configurations set up for your computing node and the login node. If you have't, add the following lines to `~/.ssh/config` in your local machine.

```txt title="~/.ssh/config"
# Login node
Host discovery
    HostName login.discovery.neu.edu
    user john
    IdentityFile ~/.ssh/id_ed25519

# Computing node: Note that each computing node needs separate configs
Host c0001
   HostName c0001
   user john
   IdentityFile ~/.ssh/id_ed25519
   ProxyCommand ssh -W %h:%p discovery
```

:::tip

Since Slurm allocates you node(s) that are available at that moment, the hostname (e.g., `c0001`) would probably be different for every job that you request. This means you need to set up a new configuration for different computing nodes.

If you want to specify the node for the job, you could add the `SBATCH` option in the batch file. The `c0001` part should point to the available node in your partition.
```sh
#SBATCH --nodelist=c0001
```

:::

Once you've prepared a SSH config file, start port forwarding with the following command.

```sh
ssh -L <local_port>:localhost:<remote_port> <remote_hostname>
```

For example if you are forwarding `localhost:8888` on `c0001` to `localhost:8889` on your local device, the command would be:
```sh
ssh -L 8889:localhost:8888 c0001
```

### Alternatives

Typing in the long-and-hard-to-memorize `ssh` command everytime could be cumbersome for you. In that case, there are multiple alternative methods that does same thing in a user-friendly way:
- Use [VS Code with Remote SSH extension](/docs/computation/hpc/intro/vscode-jupyter)
- Use GUI applications
    - [Core Tunnnel](https://codinn.com/tunnel/) (Mac)



## Access Jupyter Lab from browser
If the port-forwarding is working properly, you should finally be able to access Jupyter Lab on your machine. Type in `http://localhost:8889` (or whichever port that you've forwarded to) in the browser.

Voila, you're ready to go!