---
title: "Flutter By Example : BuildContext 类"
date: "2019-01-07"
---

[Flutter-By-Example：BuildContext 类](https://flutterbyexample.com/build-context-class)

此章最后没译，自己看源码注释总结了。

## BuildContext 类

简言之， BuildContext 是：

- `widget`在树中的位置
- 众多 widget 中包含的一个 widget ，就像被包含于html内的某个div:

<

div < div > .html> - 在 flutter 中，所有 widget 都会最终调用到 build.call - 直到某个widget 返回了某样东西，或者尺寸之类。

* * *

**以上为译文，翻译过程中有疑问直接看源码注释了，发现看完已经差不多，不过始终多谢作者给的题目**

> 译注，这章的一些说法似乎不太对，比如说所有东西都是 widget ，所有widget 最终都会调用到 build 方法，所有 widget 都有一个 override 的 build 方法。似乎都不对。 查看下 BuildContext 类的注释：
> 
> - A handle to the location of a widget in the widget tree
>     
> - 在 StatelessWidget.build 和 State 中使用
>     
> - 每个 widget 都有其自己的 BuildContext 其来自于其父 widget 的 statelessWidget.build 或 State.build 方法（或者来自 RenderObjectWidgets 的父类）
>     
> - 所以 widget 中的 BuildContext 不一定都是一样的，因此有可能会出现一些意外情况，如下例：
>     
> - ```dart
>     @override
>     Widget build(BuildContext contextOuter){
>       return Scaffold(
>           body:Builder(build:(buildContext contextInner){
>               Scaffold.of(contextInner)
>                   .showSnackBar(SnackBar(
>                         content:Text('正常显示')
>                    )
>               );
>               Scaffold.of(contextOuter)
>                   .showSnackBar(
>                       SnackBar(
>                           content:Text('出错')
>                       )
>                   )
>               );
>           })
>       );
>     }
>     ```
>     
> - BuildContext 会因为在树中的位置变化而不同，依赖于 BuildContxt 的函数，每次调用都不的结果都不应该做缓存。
>     
> - BuildContext 对象实质上就是 Element 对象，使用 BuildContext 接口是为了避免（discourage 不鼓励）直接生成 Element 对象。
>     
> 
> 可以理解 xx.of(context) 的作用为：找widget树上父节点中类型为 xxx 的对 源码中可看到 context. inheritFromWidgetOfExactType，同时，InheriteWidget 的创建目的就是为了能高效在 widget 树中找到某个类型的实例。
