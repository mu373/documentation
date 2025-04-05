---
title: Shell
sidebar_position: 1
slug: shell
---

## Various types of shell
bash, zsh

## Setting up configuration file
```sh
vim ~/.bashrc
```

## Alias
```sh title="~/.bashrc"
alias ll="ls -l"
```

## Shell scripts

A `for` loop in bash allows you to iterate over a series of values. Here is an example in bash.

```bash
for i in {1..5}
do
    echo "Count: $i"
done
```

This script will output:
```
Count: 1
Count: 2
Count: 3
Count: 4
Count: 5
```