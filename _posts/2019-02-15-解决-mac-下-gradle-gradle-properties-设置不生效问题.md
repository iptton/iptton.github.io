---
title: "解决 mac 下 ~/.gradle/gradle.properties 设置不生效问题"
date: "2019-02-15"
---

https://stackoverflow.com/questions/28289172/gradle-gradle-properties-file-not-being-read

由于要翻墙才能访问，所以在 ~/.gradle/ 目录下写了个 gradle.properties 文件，但是每次都还需要到具体的项目下个性gradle.properties，一度怀疑是 mac 下无效，今天尝试 google 了下，**面向 stackoverfow 编程** 大法好！

原来原因是gradle默认放在 $USER\_HOME/.gradle 上，而 mac 自身只设了 $HOME ，所以解决方法有两个：

a. 在~/.bash\_profile 下增加 GRADLE\_USER\_HOME 变量

```shell
export GRADLE_USER_HOME=/Users/xxx/.gradle
```

b.使用gradle 默认目录，只需要增加 USER\_HOME 变量，指向 $HOME 即可

```shell
export USER_HOME=$HOME
```

二选一，修改完后，运行

```shell
source ~/.bash_profile
```

或重启shell.
