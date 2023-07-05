---
title: "为什么 Flutter 使用 Dart 语言"
date: "2018-11-08"
---

https://hackernoon.com/why-flutter-uses-dart-dd635a054ebf

有语言学家认为人类所使用的语言会影响其思维方式，这个概念在计算机领域是否同样有效？

码农们在不同的编程语言切换时，通常对同样的问题要使用不一样的解决方案。举个极端的例子：计算机学者号召 [消灭 goto 语句](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) 以写出更结构化的代码。不同于 1984 小说中的消灭思想罪balabala（没看懂表达的是什么意思）。

这与 Flutter / Dart 有什么关系？在早期，Flutter 尝试了十来种语言，**最终选择了Dart，理由是它符合我们构建 UI 的方式。**

同时，Dart 语言也是很多开发者喜欢 Flutter 的最大理由。（举 twitter 例）

以下 Dart 特性是 Flutter 所不可或缺的：

- Dart 的AOT(Ahead Of Time:静态提前编译)编译方式，使得编译后代码更快，更可靠。
- Dart 也可以用 JIT (just in time: 运行时编译)编译方式，可在开发阶段提供更高效率（如 Flutter hot reload)
- Dart 可以轻易创建 60 fps 的动画效果。Dart 的对象生成及回收都不需要加锁。
- Dart 不需要额外的语言(如 XML/JSX) 来构造 UI 。
- 开发者会发现 Dart 特别易于上手，因为它具有静态和动态语言都非常相似的特性。

**以下内容摘译**

## Preemptive scheduling, time slicing, and shared resources （抢占式调度，分时，资源共享）

多数编程语言支持多线程并行（Java/Kotlin/Objective-C/Swift)，使用抢占方式来切换线程，每个线程都申请一定的CPU时间分片来执行，时间一到，系统会进行线程切换。一但共享的资源在抢占切换发生时正在更新，会触发条件竞争问题。（**简言之，多线程会出现的共享资源读写问题**）。

balabala…（竞争会产生什么后果，以及用锁来解决会带来什么问题）

**Dart 解决这个问题的方法是使用 `isolate`,不共享内存。如此，可避免大部分的锁。`Isolate`之间通过传递消息通信，与 `Erlang` 的`actor` 或者 web 中的`worker`类似。**

Dart 是单线程的。这意味着，不会出现抢占，替而代之的是主动的让出(yield)CPU，（使用 async/await, Future, Stream）。这样开发者有更多的控制权。可以让重要函数不被打断地完整执行完毕（如动画 ，场景切换）。

当然，如果开发者忘了让出(yield)控制权，后果是其他代码的执行会延后。但这种失误很容易发现和解决（相比于多线程的竞争而言）。

[UI 工具](https://groups.google.com/forum/#!topic/flutter-dev/lKtTQ-45kc4)：新的 Dart tools 可以更方便编辑（IDEA 快捷键 option + enter , VSCode : cmd + . )

[why-native-app-developer-should-take-a-serious-look-at-flutter](https://hackernoon.com/why-native-app-developers-should-take-a-serious-look-at-flutter-e97361a1c073)
