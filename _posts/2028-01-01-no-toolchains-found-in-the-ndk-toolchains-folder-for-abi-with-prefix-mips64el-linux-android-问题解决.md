---
title: "No toolchains found in the NDK toolchains folder for ABI with prefix: mips64el-linux-android 问题的解决"
date: "2019-02-13"
---

这个问题的解决方案很多人给出的是从网上上载缺失的bundle 放到指定的 NDK 目录。一开始我也是这样操作，但后来想想不太对，已经相对成熟的NDK出现这样的问题不太正常，继续google 发现这个：

> If you are using NDK >= 18 you have to update your android gradle plugin to >=3.1.x See the Known Issues section: https://android.googlesource.com/platform/ndk/+/ndk-release-r18/CHANGELOG.md This version of the NDK is incompatible with the Android Gradle plugin version 3.0 or older. If you see an error like No toolchains found in the NDK toolchains folder for ABI with prefix: mips64el-linux-android, update your project file to use plugin version 3.1 or newer. You will also need to upgrade to Android Studio 3.1 or newer.

也就是说 NDK 升级到18后，gradle plugin需要使用 3.1 以上，Android studio 需更新到3.1以上。

因此，在 IDEA 的项目上，只需要在根目录的 build.gradle:

```groovy
buildscript {
    ...
    dependencies {
        classpath 'com.android.tools.build:gradle:3.3.1'
        ...
    }
```
