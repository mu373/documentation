---
sidebar_position: 4
slug: public-key
---

# Public key

## What is private/public key?


## Creating a key pair
```sh
cd ~/.ssh
ssh-keygen -t ed25519 -C "mail@example.com"
```

Here's the descriptions of the options provided to the command.
- `-t`: Type of key to create
    - By "type", it means cryptographic algorithms, such as `ecdsa`, `ed25519`, and `rsa`. As of 2024, `ed25519` is the preferred cryptographic algorithm to generate keys to ensure security.
- `-C`: Comment for the key
    - It is a common practice to put our emails here to identify our keys, but any texts could be written here.

Proceed by pushing the `return` key. Usually, you won't need to setup a passphrase. The final output would look something like this.

```shell-session
$ ssh-keygen -t ed25519 -C "mail@example.com"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/Users/john/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/john/.ssh/id_ed25519
Your public key has been saved in /Users/john/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:3MPdSlN9Pj+KKZZMtsK/f6O/5GWLi1m/HDRQNIF/D4M mail@example.com
The key's randomart image is:
+--[ED25519 256]--+
|              o=.|
|             ....|
|             oo o|
|       . o .Eo+oo|
|        S + + .*+|
|         o o o. =|
|      . + o .o =.|
|       o *  OoB +|
|        +o+B+B+=.|
+----[SHA256]-----+

```

Let's check what's inside a public key.
```shell-session
$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDOYfZ33zaFZDws4FwLxNAxRqBykbGXM1H6QjglfJXPE mail@example.com
```

:::info
As the name tells, **public keys can be public**. You can publish it on key servers, your websites, email it to a friend. But **NEVER share or publish the private key***, as will compromise the security.
:::


## Useful commands for private/public key pairs

Change the SSH key comment
```sh
ssh-keygen -c -C "my new comment" -f ~/.ssh/id_ed25519
```

Change passphrase
```sh
ssh-keygen -f id_ed25519 -p
```

Regenerate public key from private key
```sh
ssh-keygen -y -f id_ed25519 > id_ed25519.pub
```

Check fingerprint of the public key
```sh
ssh-keygen -l -f id_ed25519.pub
```