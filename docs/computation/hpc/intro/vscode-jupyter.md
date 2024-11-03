---
sidebar_position: 11
slug: vscode-jupyter
---

# Jupyter on VS Code

## Introduction
In the previous sections, we've learend how to start Jupyter Lab on Discovery computing node and how to connect those nodes from VS Code. If you haven't, follow the following tutorials:
- [Starting a Jupyter Lab on computing node](/docs/computation/hpc/intro/jupyter)
- [Connecting VS Code to Discovery](/docs/computation/hpc/intro/vscode)

Now, you can even **use Jupyter directly from VS Code**, which offers more powerful editing experience than on browsers.

## Reasons to use Jupyter from VS Code
Why would I care to use Jupyter from VS Code when it can be accessed from any browser?
<!-- 
## Connect from VS Code
Go to the "Remote Explorer" (icon with PC monitor) in the activity bar (the bar on the very left). A panel with list of servers will show up in the left side of the window. The servers listed here are the hosts that you have configured in `~/.ssh/config` file.

Once you have located the server that you would like to connect (could be a login node, or a computing node), click on the arrow button to start a session. -->

## Installing VS Code extensions on the server
To use Jupyter on the remotely connected VS Code, you need to install following extensions.

After you've established a VS Code connection to the node, go to the extentions panel. The install button would say `Install to <server>`. 
- [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

:::tip
The installation process could take some time (could take more than 10 minutes) to complete. Let it run, and go grab some coffee and cookies!
:::