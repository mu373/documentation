---
title: Basic commands
sidebar_position: 1
slug: commands
---

### cd
`cd`: Moving around in file system
```sh
cd ~/
cd /var/log
```

### ls
```sh
ls
ls -a
ls -h
ls -l
```

### pwd
```sh
pwd
```

### mkdir
```sh
mkdir foo
mkdir -p foo/bar/
```

### cat
`cat`: Print the entire text file in standard output.
```sh
cat memo.txt
```

If you pass multiple files, it will provide concatinated standard output. (This is the intended usage of `cat`!)
```sh
cat memo1.txt memo2.txt > memo-all.txt
```

### less
If you have a long text file, you should consider using `less` instead of `cat`. `less` is a pager progam that lets you see the contents of a text file, allowing you to navigate through the file using `vi`-like shortcuts (e.g., `j` for down, `k` for up.)
```sh
less memo.txt
```

### hostname
If you are working with multiple devices, for example with your local machine and a remote server, you might lose track of which device you are accessing. The `hostname` command gives you the name of the machine you are currently accessing.
```sh
hostname
```