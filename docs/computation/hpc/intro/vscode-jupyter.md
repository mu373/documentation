---
sidebar_position: 11
slug: vscode-jupyter
---

# Jupyter on VS Code

## Get a computing node
Follow the detailed instructions [here](/docs/computation/hpc/intro/vscode#using-computing-nodes) to get a computing node.

Submit the job to start the tmux session.
```sh
sbatch tmux.sh
```

Attach to the tmux session using the `srun` command. Make sure that you detatch (`<tmux prefix> d`) when you finish using, instead of killing the shell.
```sh
srun --jobid=<your_job_id> --pty tmux a
```
Check for the hostname of the allocated computing node.
```sh
hostname
```

Once you have your SSH configuration set for a computing node, let's connect VS Code to the node.

## Connect from VS Code
Go to the "Remote Explorer" (icon with PC monitor) in the activity bar (the bar on the very left). A panel with list of servers will show up in the left side of the window. The servers listed here are the hosts that you have configured in `~/.ssh/config` file.

Once you have located the server that you would like to connect (could be a login node, or a computing node), click on the arrow button to start a session.

## Install VS Code extensions on the server
Install following extensions on the VS Code running in the server. The install button would say `Install to <server>`. The installation process could take some time to complete.
- [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

