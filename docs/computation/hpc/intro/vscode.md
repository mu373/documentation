---
sidebar_position: 10
slug: vscode
---

# Discovery with VS Code
Want to edit files directory from VSCode? There is a way to do that.

## Install VS Code
VS Code is available for Mac, Windows, and Linux.

https://code.visualstudio.com/

## Setup SSH config for login node {#ssh-config-login}
See [here](/docs/computation/unix/ssh#setting-up-ssh-config) for detailed instructions.
For Discovery login node, the configuration in `~/.ssh/config` would be something like
```title="~/.ssh/config"
Host discovery
    HostName login.discovery.neu.edu
    user john
    IdentityFile ~/.ssh/id_ed25519
```

## Add VS Code extensions
Go to the "Extensions" tab (icon with blocks) in the activity bar (the bar on the very left). Search for the following extensions and install.
- [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)


## Using computing nodes

### Start a job on computing node
On Discovery, create a new batch file to start tmux and run it until the time limit.
```bash title="tmux.sh"
#!/bin/bash
#============ Slurm Options ===========
#SBATCH --partition=express              # Set partition that you have access to.
#SBATCH --mail-user=john@example.com     # Enter your email address for job notification
#SBATCH --mail-type=END                  # Send email when the job ends
#SBATCH --time=1:00:00                   # Set time limit to 1 hour
#SBATCH --output=/home/john/discovery/slurm/logs/slurm-%j.out # Any stdout will be stored here.
#SBATCH --cpus-per-task=1
#=======================================

# Clear current env/modules
module purge

# Load required module from Discovery (required for internet accesss)
module load discovery

# Activate conda environment, if necessary
source activate /your/path/to/conda/env

# Start a new tmux session with name "0"
tmux new -d -s "0"

# Keep running this job until the time limit
sleep infinity
```

Submit the job to start the tmux session.
```sh
sbatch tmux.sh
```

You can attach to the tmux session using the `srun` command. Make sure that you detatch (`<tmux prefix> d`) when you finish using, instead of killing the shell.
```sh
srun --jobid=<your_job_id> --pty tmux a
```

The hostname of the allocated computing node can be checked by the following command. For Discovery, it usually has name `cXXXX` where `XXXX` is a 4 digit number.
```sh
hostname
```

### Setup SSH config for computing node
Computing nodes cannot directly be connected from our local machines, but rather it needs to connect through the Discovery login node. To have setup such connection, we use a specific option in the `~/.ssh/config`. Make sure that you also have the config for `discovery` setup in the same file [see here](#setup-ssh-config)).
```title="~/.ssh/config"
 Host c0001
    HostName c0001
    user john
    IdentityFile ~/.ssh/d_ed25519
    ProxyCommand ssh -W %h:%p discovery
```

:::note

Since Slurm allocates you node(s) that are available at that moment, the hostname (e.g., `c0001`) would probably be different for every jobs that you request. This means that you would have to setup a new configuration for different computing nodes.

If you want to specify the node for the job, you could add the following line the `SBATCH` option in the batch file. `c0001` should be the hostname of the node that is available in the partition that you are using.
```sh
#SBATCH --nodelist=c0001
```

:::

## Connect from VS Code
Go to the "Remote Explorer" (icon with PC monitor) in the activity bar (the bar on the very left). A panel with list of servers will show up in the left side of the window. The servers listed here are the hosts that you have configured in `~/.ssh/config` file.

Once you have located the server that you would like to connect (could be a login node, or a computing node), click on the arrow button to start a session.