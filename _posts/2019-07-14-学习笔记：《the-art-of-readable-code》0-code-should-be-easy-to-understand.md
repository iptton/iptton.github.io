---
title: "学习笔记：《The Art of Readable Code》(0) : code should be easy to understand"
date: "2019-07-14"
---

KEY IDEA:

**代码应该易于理解**

* * *

这是我们在写代码时最重要的指引原则。

### 如何让代码变得“更好”？

多数程序员做出编码决策时都是依据直觉。

```c++ 
for (Node *node = list->head; node != NULL; node = node->next) Print(node-data);
```

会比以下代码要好：

```c++ 
Node \*node = list->head; if (node == NULL) return;
while (node->next != NULL) { Print(node->data); node = node->next; } if (node != NULL) Print(node->data)
```

以上两段代码实现功能是一致的，但是，很多时间，选择是比较艰难的。如

```c++ 
return exponent >= 0 ? mantissa \* (1 << exponent) : mantissa / (1 << -exponent);
```

可读性明显要差于

```c++ 
if (exponent >= 0){ return mantissa \* (1 << exponent); } else { return mantissa \* (1 << -exponent); }
```

第一段代码更紧凑，但第二段代码会更友善。哪种标准更重要？或者说，你要如何决定用哪种方式来编码？

### 代码可读性的基本原则

> 代码应该以其他人阅读理解的时间最小化的方式来组织 ( Code should be written to minimize the time it would take for someone else to understand it)

此处**理解**一词我们有非常高的标准：**完全理解** 你的代码，指的是他能够对代码进行修改，查BUG，以及它是如何与你的其他代码进行交互的。

也许你会说：谁在乎别人能不能读懂它？这些代码只有我自己在用！但是就算这是个个人项目，增强代码可读性也是件值得做的事。原因是：

- “别人”可能指的是六个月后的你自己，那时的你对这些代码可能已经很不熟悉了；
- 或者，你永远不知道会不会有别人加入你的项目中；
- 或者，你的“一次性”代码，可能会在别的项目中被使用。

### 简短就意味着更好吗？

一般而言，用更简短的代码来解决同样的问题更好。读懂 五千行代码的时间，一般要比两千行要少。

但是更少的行数并不总意味着更好：

```c++ 
assert((!(bucket = FineBucket(key))) || !bucket->IsOccupied());
```

与以下代码相比：

```c++
bucket = FindBucket(key); if (bucket != null) assert(!bucket->IsOccupied());
```

要花更多时间理解。

类似的，可以用一行注释就能让你的代码能被快速理解：

`c++
 // Fast version of " hash = (65599 * hash) +c" 
 hash = (hash << 6) + (hash << 16) - hash - c;
 ```

所以，相比于写更简短的代码这个目标，写出最小化理解时间的代码这个目标更好。

### Time-Till-Understanding 原则与其他原则冲突吗？

也许你会有疑问，这个原则会不会与代码执行效率，代码结构或代码易测性等相冲突？

我们的经验是，它们通常互不干扰。甚至在特殊领域的高度优化的代码里，依然有办法写出高可读性的代码。而通常具可读性的代码，同时也会带来更良好的架构及更好的可测性。

本书其他部分讨论如何在不同情况下实现“易读”。不过需要记住的是，当你产生疑问时，可读性的基本原则优先于其他所有规则。而且，有些程序员会难以抵制把代码优化到极致的欲望，这种情况下，只需要退一步自问一句：这些代码现在是否容易理解？如果答案是“是”，那也许可以继续写其他代码了。

### 困难部分

思考其他人怎么理解你的代码，确实需要持续地投入额外的时间，相比之前，你需要在编码之前投入一定的思考才能达到目标。

但是，如果你能达到这个目标，我们确信，你会变成一个更好的程序员，写出更少的 BUG，对自己的工作更加自豪，且写出更受周围同事的欢迎的代码！
