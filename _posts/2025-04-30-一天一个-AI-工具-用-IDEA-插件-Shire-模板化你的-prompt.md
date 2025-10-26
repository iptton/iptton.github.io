---
title: "一天一个 Ai 工具 用 Idea 插件 Shire 模板化你的 Prompt"
date: "2025-04-30"
---

Shire 是一个开源的 AI 编程插件(语言)。作者也有一篇介绍： [Shire 编码智能体语言：打造你的专属 AI 编程助手](https://cloud.tencent.com.cn/developer/article/2437687)。这是一个（几乎只）对程序员友好的工具，官方有更详细的介绍：[https://shire.phodal.com/](https://shire.phodal.com/)。通过本文可以大致了解用它可以做什么。


## 安装插件

这是一款运行于 Jetbrains IDE 的插件，需先安装：

![[Pasted image 20250430133449.png]]

## 设置 LLM Key

使用 `Shire` 需提供 LLM key，打开系统设置，搜索 `shire` 

![[Pasted image 20250430143756.png]]
填入你所申请的 LLM key 和参数之后才可用（这个 key 通常是需要购买的， 各 LLM 平台都会提供）

填完所需的 key 后，应用设置后可点"Test LLM Connection" 验证是否正确。

## 使用 Shire 对选中的内容进行 Review

在项目中新建一个文件 : `review.shire`，内容如下：

```
---  
name: "review"  
description: "review selected code"  
interaction: RightPanel  
actionLocation: ContextMenu  
---  
  
你是一个友好的专业程序员，请帮我 review 以下代码，从可读性，逻辑正确性等角度提出建议

$selection
```

打开编辑器，**选中**你需要 AI 帮你 review 的文件内容，然后按**右键菜单**，选择我们指定的 name: "review"

![[Pasted image 20250430144735.png]]

查看右侧工具栏，可以看到 IDE 向 LLM 发送了一个请求
![[Pasted image 20250430144957.png]]
(忽略上面的一些排版错误，这是一个开源项目，有意修改可直接贡献）

## 小结

Shire 可以结合  IDE  的右键菜单，文本选中等 IDE 环境，完成 prompt 的内容的组合及返回结果的处理。一个 Shire 文件就是一个 Agent，Shire 还提供了一次 LLM 调用的不同生命周期的处理逻辑插入，在不同生命周期可以执行调用其他 Agent 的能力，**理论上，对 Shire 再扩展可以实现一个完整的 AI 代码助手。**

----
劳动节快乐!