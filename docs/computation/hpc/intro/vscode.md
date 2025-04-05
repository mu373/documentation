---
title: Discovery with VS Code
sidebar_position: 10
slug: vscode
tags:
  - Jupyter
---

Want to edit files directly from VSCode? There is a way to do that.


## Introduction to VS Code
VS Code is a source code editor developed by Microsoft. Not only that it has powerful editing capabilities including IntelliSense code completion and debugging, it can be customized by installing third-party extensions, allowing the users to boost their developer experiences. It is an Electron based application, meaning that it is built based on the web technologies such as JavaScript and Node.js. You can read more on the [VS Code official documentation](https://code.visualstudio.com/docs/editor/whyvscode).

## Installing VS Code
VS Code is available for Mac, Windows, and Linux.

https://code.visualstudio.com/

## Setting up SSH config for login node {#ssh-config-login}
See [here](/docs/computation/unix/ssh#setting-up-ssh-config) for detailed instructions.
For the Discovery login node, the configuration in `~/.ssh/config` would be something like
```title="~/.ssh/config"
Host discovery
    HostName login.discovery.neu.edu
    user john
    IdentityFile ~/.ssh/id_ed25519
```

## Installing extensions on VS Code {#extension}
Go to the "Extensions" tab (an icon with blocks) in the activity bar (the bar on the very left). Search for and install the following extensions.
- [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)


## Connecting from VS Code {#connect}
Go to the "Remote Explorer" (with a PC monitor icon) in the activity bar (the bar on the very left). A panel with a list of servers will appear on the window's left side. The servers listed here are the hosts you have configured in the `~/.ssh/config` file.

Once you have located the server to which you would like to connect (it could be a login node or a computing node), click the arrow button to start a session.