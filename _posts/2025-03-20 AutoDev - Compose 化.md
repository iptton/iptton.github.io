---
title: AutoDev - Compose 化
date: 2025-03-20
---


AutoDev 是用 Swing 写的 UI，这个古老的 Java UI 框架极其难用，相比之下，Compose 声明式 UI 可以极大地减少开发心智成本及维护成本，但直接用 Compose Desktop 在 IDEA 上开发是不现实的，因为 material 那套 UI 与 IDEA 格格不入，幸运的是，IDEA 官方也认为 Swing 难用，且它们为 IDEA 的 look and feel 写了一套 UI: [Jewel](https://github.com/JetBrains/jewel)。我们尝试把 AutoDev 的一些 UI 逻辑重构成 Compose 版本。

这个任务的特点：

- 这是一个对人类来说稍为复杂的任务，需要在命令式和声明式中迁移
- 它需要用到 Swing / Compose 这两个广为人知的知识
- 它需要用到 Jewel 这个较少资料的知识