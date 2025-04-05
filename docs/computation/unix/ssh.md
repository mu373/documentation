---
title: Remote Access with SSH
sidebar_position: 5
slug: ssh
tags:
  - SSH
---

When you are working on your local machine, the shell starts up just by opening a new terminal window without asking for authentication. How can we access the shell on a remote server, just as we do on the local machine? This is where SSH (Secure Shell) comes in.

**SSH is a protocol for securely accessing remote servers**, and we use it with the `ssh` command.

## Getting started

Let's check that we have an SSH client installed on our devices. If you type in `ssh` in the terminal, you should get an output like this.
```sh
$ ssh
usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface]
           [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
           [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
           [-i identity_file] [-J [user@]host[:port]] [-L address]
           [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
           [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
           [-w local_tun[:remote_tun]] destination [command]
```

To `ssh` into a server, we type in a command like this. Here, we are telling that our username on the target server `server1.example.com` is `john`. If the username and hostname are correct, the server would typically respond by asking for your password on the server.
```sh
ssh john@server1.example.com
```

## SSH with public key authentication (optional)
This step is optional, only if you want to access the server using public key authentication.

### Generating SSH keypairs
Let's check if you already have a SSH key in your local device.
```sh
cd ~/.ssh
ls -al
```

If you can't find files that is named something like `id_ed25519`, you'll need to generate a new SSH keypair. [See here](/docs/computation/unix/public-key) for detailed instructions on how to generate a SSH key-pair.

Let's first ensure that we have the `~/.ssh/` directory and that it is accessible only by yourself.
```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

```sh
cd ~/.ssh
ssh-keygen -t ed25519 -C "mail@example.com"
```

### Adding your key to the server
```sh
# In your local device
cd ~/.ssh

# Let's check the contents of the public key
cat id_ed25519.pub

# Copy the public key to the server
scp id_ed25519.pub john@server1.example.com:~/.ssh/
```

```sh
# In the remote server
# Register the public key as "authorized key"
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```

Now that we've registered our public key to the server, we can use public key authentication to identify ourselves, instead of authenticating by password, 
```sh
ssh john@server1.example.com -i ~/.ssh/id_ed25519
```

The `-i` flag is for "identity file," and we pass the path for the private key following it. The path could depend on the file name of the private key that you are using.


## Setting up SSH config

If there is a server that you access regularly, you could use a predefined configuration file instead of typing in the password, user name, hostname, and the path to keys every time. We use the `~/.ssh/config` file to store such SSH configurations.

Let's make a new configuration file.
```sh
cd ~/.ssh
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

Using a text editor you prefer, write configurations in the following manner. The `IdentityFile` line is optional, only required if you want to use public key authentication.
```txt title="~/.ssh/config"
Host server1
    HostName server1.example.com
    Port 1111
    User john
    IdentityFile ~/.ssh/id_ed25519

Host lily
    HostName lily.example.com
    Port 2222
    User john
    IdentityFile ~/.ssh/id_ed25519

# It can also take wildcards
Host *.foo.example.com
    IdentityFile ~/.ssh/id_ed25519

```

Now, you can access a server just in a single line.
```sh
ssh server1
```

Since the SSH client reads the predefined configuration file for alias `server1`, the above command is equivalent to running the following code.
```sh
ssh john@server1.example.com -p 1111 -i ~/.ssh/id_ed25519
```

## Port forwarding
Let's say that you have started Jupyter Lab on the remote server, and it is available at `http://localhost:8888` on the server. How can we access this Jupyter Lab from a browser on our local device? By default, you cannot access it even if you type in that URL on your device. It's running at the `localhost` on the remote server, not your local device.

**Port forwarding** is the solution for such cases. As the term tells by itself, **we forward the ports on remote servers to ports on our devices**, so that `http://localhost:8888` (or any other ports) on local devices points to what's available on the server. The connection is provided by SSH, which means that everything that is transferred is encrypted using cryptographic algorithms.



## Additional resources
- Missing Semester. "Command-line environment". https://missing.csail.mit.edu/2020/command-line/.