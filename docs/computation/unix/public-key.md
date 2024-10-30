---
sidebar_position: 4
slug: public-key
---

# Public key

## What is private/public key?


## Creating a key pair
```sh
ssh-keygen -t ed25519 -C "mail@example.com"
```

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