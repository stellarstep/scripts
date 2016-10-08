<img src="https://raw.githubusercontent.com/metasmile/git-subfile/master/icon.png?v=1" width="50%">

[![Tasks in Ready](https://badge.waffle.io/metasmile/git-subfile.svg?label=ready&title=Tasks in Ready)](http://waffle.io/metasmile/git-subfile)

git-subfile is safe, fast and strong way to work with sub repositories. This git extension finally will synchronize and automatically resolve git working between specific path in main repo and other repositories.

``
path/in/your/MainRepo <- [synchronization] -> ~/Documents/MySubRepo
``

Write, and Read them. That's all. Just simplify complex and annoying sucking subtree work via file-only operations safely. Yes, this is NOT a subtree extension. And I extremely hate subtree and also submodule.

# Install

```
$ (sudo) make install
```

# Usage

```
usage: git subfile <command> [params ...]

commands:
    write <relative path of target in current repo> <absolute path for original repo>
    read <relative path of target in current repo> <absolute path for original repo>
```

At first just clone your target sub repo. This will NOT be used as subtree!
Currently, you have 2 repo. One is main project repo, another one is sub repo that will be cloned.

```
$ git clone https://github.com/metasmile/MySubRepo.git
```

So you can have 2~n repos.
```
~/Documents/MyProjectRepo
~/Documents/MySubRepo1
...
~/Documents/MySubRepoN
```

## write

This command will commit working contents of specific path in your main project repo to sub repo. And then it automatically performs git's general committing works with "stash" and "commit".
```
~/Documents/MyProjectRepo$ git subfile write path/in/your/MainRepo ~/Documents/MySubRepo
```

## read

This command will read(yes, read files. that's all) all content from sub repo to main repo's specific path. And then it automatically performs git's general pulling works with "stash", "pull" and "commit".

```
~/Documents/MyProjectRepo$ git subfile read path/in/your/MainRepo ~/Documents/MySubRepo
```
