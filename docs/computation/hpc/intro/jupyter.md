---
sidebar_position: 10
slug: jupyter
---

# Jupyter Lab

You can run your own Jupyter Lab for yourself, without depending on the OOD.

## Getting computing nodes {#get-computing-node}
Let's start by getting a computing node allocated. Why computing nodes? As the name tells, the login nodes are designed exclusively for "login" purposes, and thus any computations should be done on computing nodes. Take advantage of the available resources in the computing nodes!

On Discovery, create a new batch file as following. This batch file specifies the options for the computing node, starts `tmux` and keeps the job running until the time limit. `tmux` is a terminal multiplexer that allows you to run use multiple panes and tabs in command line interface, and also keeps the session running in the background even when you close the screen (detach the session).

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
# Using tmux allows using multiple tabs and running multiple things in command line
tmux new -d -s "0"

# By default, the batch job will end if all the jobs inside are complete.
# We use the "sleep" command to keep this job running until the time limit
sleep infinity
```

Once you've created the batch file, let's submit the job. This batch file will request for a computing node with the options we've specified, and if that's accepted by the system, a new tmux session will start up in the allocated node.

```sh
sbatch tmux.sh
```

:::note
If this is your first time using the `sbatch` `squeue` `srun` commands, you can [learn Slurm concepts and commands here](/docs/computation/hpc/intro/slurm).
:::


Let's check that if the batch has been processed properly, using the `squeue` command. If the `ST` column is `R`, it means that the job is running.
```shell-session
$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1234567 express       tmux.sh  john R    00:59:30      1 c0001
```

After confirming that the job is running, you can enter the shell by "attaching" to the tmux session with the `srun` command. This will open up a `tmux` screen. (Job ID is shown in the output of the `squeue` command.)
```sh
srun --jobid=<your_job_id> --pty tmux a
```

Once entering the shell, the prompt would tell you the hostname of the node that you were allocated to. In the following example, you are allocated to node `c0001`. For Discovery, the hostname for computing nodes are `cXXXX` where `XXXX` is a four-digit number.
```shell-session title="Shell prompt in the allocated node"
[john@c0001 ~]$
```

:::tip
Ensure you detach (`<tmux_prefix> d`) when you finish using it instead of killing the shell.  
By default, the tmux prefix is set to `Ctrl-b`. To detatch, you first push `Ctrl-b` first, release the keys, and then type `d`.
:::


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

## Port-forwarding on local machine {#port-forwarding}
Since the Jupyter Lab that you just started works in the remote server (computing node), it is not accessible from the browser on your local device at startup. You have to set up **port-forwarding** so that you have access to what's running on the remote server.

There are multiple ways to do this, but let's stick to the most basic way which is through the `ssh` command.

### Setting up port forward with `ssh` command

:::info
You would be working on your **local device** for this step, not on Discovery!
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
```
#SBATCH --nodelist=c0001
```

Available nodes in a specific partition can be checked using the following command. The nodes with "mixed" or "idle" label are the ones that are available for use.
```shell-session
$ sinfo -p <partition_name> -o "%N %T"
NODELIST STATE
c[0004,0016,0021] drained*
c0100 down*
c[0005,0006-0015,0020,0050-0055,0099] mixed
c[0001-004,0017-0019,0021-0049,0056-0098,0101-0105] idle
```


:::

Once you've prepared a SSH config file, start port forwarding with the following command.

```sh
ssh -L <local_port>:localhost:<remote_port> <remote_hostname>
```

For example if you are forwarding `localhost:8888` on node `c0001` to `localhost:8889` on your local device, the command would be as following.
```sh
ssh -L 8889:localhost:8888 c0001
```

Although the screen you see after running the above command would look exactly the same as the regular `ssh` login, this session is forwarding the ports in the background. Make sure not to close this SSH session while you are using Jupyter.

### Alternatives

Typing in the long `ssh` command everytime to forward ports could be tiring. (Who can remember the order of local ports and remote ports for that command?) In such case, there are multiple alternative methods that does the same thing in user-friendly ways:
- Use [VS Code with Remote SSH extension](/docs/computation/hpc/intro/vscode-jupyter)
    - [Official documentation](https://code.visualstudio.com/docs/editor/port-forwarding)
- Use GUI applications
    - [Core Tunnnel](https://codinn.com/tunnel/) (macOS)
    - [Secure Pipes](https://www.perfect-privacy.com/en/manuals/macos_ssh_securepipes) (macOS)



## Accessing Jupyter Lab from browser {#browser}
If the port-forwarding is working properly, you should finally be able to access Jupyter Lab on your machine. Type in `http://localhost:8889` (or whichever port that you've forwarded to) in the browser.

When the Jupyter asks for a token or a password, run the following in your **allocated node**.
```shell-session
$ jupyter server list

Currently running servers:
http://localhost:8888/?token=TOKEN_IS_PRINTED_HERE :: /home/john
```

Copy and paste the token from the URL and click "Log in."

Voila, you're ready to go!