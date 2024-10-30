---
sidebar_position: 10
slug: vscode
---

# Discovery with VS Code
Want to edit files directory from VSCode? There is a way to do that.

## Install VS Code
VS Code is available for Mac, Windows, and Linux.

https://code.visualstudio.com/

## Setup SSH config
See [here](/docs/computation/unix/ssh#setting-up-ssh-config) for detailed instructions.
For Discovery login node, the configuration in `~/.ssh/config` would be something like
```title="~/.ssh/config"
Host discovery
    HostName login.discovery.neu.edu
    user john
    IdentityFile ~/.ssh/id_ed25519
```

## Add extensions
Go to the "Extensions" tab (icon with blocks) in the activity bar (the bar on the very left). Search for the following extensions and install.
- [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)


## Using computing nodes

### Start a job on computing node
```sh
sbatch -p express job.sh
```

### Setup SSH config for computing node
Computing nodes cannot directly be connected from our local machines, but rather it needs to connect through the Discovery login node. To have setup such connection, we use a specific option in the `~/.ssh/config`.
```title="~/.ssh/config"
 Host c0001
    HostName c0001
    user john
    IdentityFile ~/.ssh/d_ed25519
    ProxyCommand ssh -W %h:%p discovery
```

:::note

Since Slurm allocates you node(s) that are available at that moment, the hostname (e.g., `c0001`) would probably be different for every jobs that you request. This means that you would have to setup a new configuration for different computing nodes.

Or, you could specify a specific node to send the job, using `-w` option in `sbatch`.
```sh
sbatch -p express -w c0001 job.sh
```
:::
