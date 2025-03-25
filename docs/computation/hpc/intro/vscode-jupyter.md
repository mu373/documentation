---
sidebar_position: 11
slug: vscode-jupyter
tags:
  - Jupyter
  - VSCode
---

# Jupyter on VS Code

## Introduction {#intro}
In the previous sections, we've learned how to start Jupyter Lab on Discovery computing node and how to connect those nodes from VS Code. If you haven't, you can follow the following tutorials:
- [Starting a Jupyter Lab on computing node](/docs/computation/hpc/intro/jupyter)
- [Connecting VS Code to Discovery](/docs/computation/hpc/intro/vscode)

Now, **you can even use Jupyter directly from VS Code**, which offers more powerful editing experience than in browsers.

## Reasons to use Jupyter from VS Code {#why}
Why would I care to use Jupyter from VS Code when it can be accessed from any browser?
<!-- 
## Connect from VS Code
Go to the "Remote Explorer" (icon with PC monitor) in the activity bar (the bar on the very left). A panel with list of servers will show up in the left side of the window. The servers listed here are the hosts that you have configured in `~/.ssh/config` file.

Once you have located the server that you would like to connect (could be a login node, or a computing node), click on the arrow button to start a session. -->


## Before we start

### Starting Jupyter Lab
Make sure that your job for tmux and Jupyter is already running in the computing node. You can check this  using the `squeue` command. If the `ST` column is `R`, it means that the job is running.
```shell-session
$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1234567 express       tmux.sh  john R    00:59:30      1 c0001
```

If you haven't follow the steps from [here](/docs/computation/hpc/intro/jupyter).

### Setting up SSH config for computing node
Once you have launched tmux and Jupyter in the computing node, let's connect VS Code to it. Skip to the next step if you have already completed this.

Open your local terminal, and make sure that you have SSH configurations set up for your computing node and the login node. If you have't, add the following lines to `~/.ssh/config` in your local machine. [See this page](/docs/computation/unix/ssh) for detailed explanations on setting up and using SSH.

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

:::info
If you're trying to connect to the computing node, you have to use public key authentication (SSH key authentication), instead of the password. If you haven't set this up yet, follow the [instructions here](/docs/computation/unix/ssh).
:::

:::tip

Since Slurm allocates you node(s) that are available at that moment, the hostname (e.g., `c0001`) would probably be different for every job that you request. This means you need to set up a new configuration for different computing nodes.

If you want to specify the node for the job, you could add the `--nodelist` option in the batch file. The `c0001` part should point to the available node in your partition.
```
#SBATCH --nodelist=c0001
```

Available nodes in a specific partition can be checked using the following command. The nodes with "mixed" or "idle" label are the ones that are available for use.
```shell-session
$ sinfo -p <partition_name> -o "%N %T"
NODELIST STATE
c[0004,0016,0021] drained*
c0100 down*
c[0005-0015,0020,0050-0055,0099] mixed
c[0001-003,0017-0019,0022-0049,0056-0098,0101-0105] idle
```


:::


### Connecting VS Code to computing node
Go to the "Remote Explorer" (with a PC monitor icon) in the activity bar (the bar on the very left). A panel with a list of servers will appear on the window's left side. The servers listed here are the hosts you have configured in the `~/.ssh/config` file.


## Installing VS Code extensions on the server {#install-vscode-extension}
Once you've established a VS Code connection to the node, let's setup the configuration on the server.

Go to the extentions panel in the left, and install the following extensions. The install button would say `Install to <server>`. 
- [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

:::tip
Make sure that you are **working on the remote server (computing node)**, not in the local environment on your local machine. The installation process on the server could take some time (possibly more than 10 minutes) to complete. Let it run, and go grab some coffee and cookies!☕🍪
:::

## Opening the notebook in VS Code {#open-notebook}
Using the filer in the "Explorer" pane, locate your Jupyter notebook file  (a file with extension `.ipynb`) that you would like to open.

Alternatively, you could create a new Jupyter notebook from scratch in VS Code.
- Press `Command + Shift + P` to open the Command Palette
- Start typing in "create jupyter"
- From the suggested lists, select "Create: New Jupyter Notebook"

## Connecting to Jupyter Lab {#kernel}
While it is possible to directly select interpreters, we will choose to connect to an existing Jupyter Lab session here. This is because connecting to a separate Jupyter Lab allows the kernels to be running, even when we close the connection or close VS Code.

- Click on "Select Kernel"
- Click "Existing Jupyter Server..."
- Paste the Jupyter URL ( `http://localhost:<some_port>`). If you've lost the URL, `jupyter server list` will show you the same URL.


## Adding kernels to Jupyter {#add-kernel}
```sh
# Activate the conda environment that you want to install a kernel
source activate ~/your/path/to/conda/environment/project1

# Make sure that Jupyter is installed in this conda environment
conda install jupyter -y

# Install the kernel. Run this inside the conda environment you want to add the kernel to.
ipython kernel install --name project1 --display-name="Python 3 (project1)" --prefix="/home/$USER/.local/"
```