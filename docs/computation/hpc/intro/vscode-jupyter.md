---
sidebar_position: 11
slug: vscode-jupyter
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

## Installing VS Code extensions on the server {#install-vscode-extension}
To use Jupyter on the remotely connected VS Code, you need to install following extensions.

After you've established a VS Code connection to the node, go to the extentions panel. The install button would say `Install to <server>`. 
- [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
- [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

:::tip
The installation process could take some time (possibly more than 10 minutes) to complete. Let it run, and go grab some coffee and cookies!☕🍪
:::

## Start Jupyter Lab in tmux {#start-jupyter}
If you haven't started Jupyter Lab inside `tmux` on the computing node, type in the following command to start. You can use the console in the VS Code, shown in the bottom of the window.
```sh
# On computing node
jupyter lab --no-browser
```

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
