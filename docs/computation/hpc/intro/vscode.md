---
sidebar_position: 10
slug: vscode
---

# Discovery with VS Code
Want to edit the files directory from VSCode? There is a way to do that.

## Install VS Code
VS Code is available for Mac, Windows, and Linux.

https://code.visualstudio.com/

## Setup SSH config for login node {#ssh-config-login}
See [here](/docs/computation/unix/ssh#setting-up-ssh-config) for detailed instructions.
For the Discovery login node, the configuration in `~/.ssh/config` would be something like
```title="~/.ssh/config"
Host discovery
    HostName login.discovery.neu.edu
    user john
    IdentityFile ~/.ssh/id_ed25519
```

## Add VS Code extensions
Go to the "Extensions" tab (an icon with blocks) in the activity bar (the bar on the very left). Search for and install the following extensions.
- [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)


## Using computing nodes

### Start a job on the computing node
On Discovery, create a new batch file to start tmux and run it until the time limit.
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

# Keep running this job until the time limit
sleep infinity
```

Submit the job to start the tmux session.
```sh
sbatch tmux.sh
```

You can attach to the tmux session using the `srun` command. Ensure you detach (`<tmux prefix> d`) when you finish using it instead of killing the shell.
```sh
srun --jobid=<your_job_id> --pty tmux a
```

The hostname of the allocated computing node can be checked by the following command. For Discovery, it usually has the name `cXXXX` where `XXXX` is a four-digit number.
```sh
hostname
```

### Setup SSH config for computing node
Computing nodes cannot be directly connected from our local machines; they need to connect through the Discovery login node. We use a specific option in the `~/.ssh/config` to set up such connections. Make sure that you also have the config for `discovery` in the same file [see here](#setup-ssh-config)).
```title="~/.ssh/config"
 Host c0001
    HostName c0001
    user john
    IdentityFile ~/.ssh/d_ed25519
    ProxyCommand ssh -W %h:%p discovery
```

:::note

Since Slurm allocates you node(s) that are available at that moment, the hostname (e.g., `c0001`) would probably be different for every job that you request. This means you need to set up a new configuration for different computing nodes.

If you want to specify the node for the job, you could add the `SBATCH` option in the batch file. The `c0001` part should point to the available node in your partition.
```sh
#SBATCH --nodelist=c0001
```

:::

## Connect from VS Code
Go to the "Remote Explorer" (with a PC monitor icon) in the activity bar (the bar on the very left). A panel with a list of servers will appear on the window's left side. The servers listed here are the hosts you have configured in the `~/.ssh/config` file.

Once you have located the server to which you would like to connect (it could be a login node or a computing node), click the arrow button to start a session.