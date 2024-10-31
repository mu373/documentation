---
sidebar_position: 5
slug: ssh
---

# Remote Access with SSH

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

Instead of authenticating by password, we can also use public key authentication to identify ourselves using the private key.
```sh
ssh john@server1.example.com -i ~/.ssh/id_ed25519
```
The `-i` flag is for "identity file," and we pass the path for the private key following it. The path could depend on the file name of the private key that you are using.

## Setting up SSH config

If there is a server that you access regularly, you could use a predefined configuration file instead of typing in the password, user name, hostname, and the path to keys every time. We use the `~/.ssh/config` file to store such SSH configurations.

Let's first ensure that we have the `~/.ssh/` directory and that it is accessible only by yourself.
```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Now, we make a new configuration file.
```sh
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

Using a text editor you prefer, write configurations in the following manner.
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

## Portforwarding


## Additional resources
- Missing Semester. "Command-line environment". https://missing.csail.mit.edu/2020/command-line/.