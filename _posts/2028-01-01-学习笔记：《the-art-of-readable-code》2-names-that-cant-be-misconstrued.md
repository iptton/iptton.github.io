---
title: "学习笔记：《The Art of Readable Code》(2) : Names That Can’t Be Misconstrued"
date: "2019-08-02"
---

## 2\. 不会被误解的命名

上一章中，我们讨论了如何把信息包装到命名中，而这一章，我们将聚集于另一个话题：关注那些容易被误解的命名。

> 关键：问下自己“这个命名会不会被别人理解成其他意思”

例：

```kotlin
val result = Database.all_objects.filter("year <= 2011")
```

上例很难通过名字判断是要过滤掉符合条件的，还是保留符合条件的对象。更好的命名是 `select(condition)` 或 `exclude(condition)`

例：

```python
# Cuts off the end of the text, and appends "..."
def Clip(text, length):
  ...
```

length 有两种理解：移除 length 长度的字符 或 保留 length 长度的字符。更好的命名是：`truncate(text,length)`

> 译注：感觉后者同样解决不了问题，对非英语母语的程序员来说…两个单词的含义其实分不了那么清

**对限制，明确使用 min 或 max**

`CART_TOO_BIG_LIMIT` 不如 `MAX_ITEMS_IN_CART`

表示限制时，使用 max\_ min\_ 前缀会更清晰。

\*\*对后闭范围（即后一数字是包含在内的情况），使用 first , last \*\*

**对后开范围（即后一数字不包含在内的情况），使用 begin, end**

**bool 命名**

布尔命名，一般以 is has can should 开头

另外，避免使用否定词如 disable\_ssl 不是一个好命名，用 enable\_ssl 或 use\_ssl 会更好理解。

**符合使用者预期**

有些词语，使用者是有刻板固定的理解的，避免使用含义与之冲突的命名。

例： getXXX()

getXXX 一般不应该做耗时操作，如果有耗时操作，则应该使用动词，如 computeXXX 来提醒使用者这是一个计算过程。

例: list::size() C++ 标准库的一个函数，以下代码产生了一个让我们非常难找到根源的让服务器变慢的bug：

\`\`\`c++ void ShrinkList(list& list, int max\_size) { while (list.size() > max\_size) { FreeNode(list.back()); list.pop\_back(); } }

````
这段代码的问题是， list:size() 的时间复杂度是 O(n) ，它会逐个节点遍历列表。因此， StrikeList 函数是时间复杂度就变成了n平方。

但是这代码是“正确”的，它甚至通过了所有单元测试。然而，如果使用百万个数据来跑，那这函数运行需要超过一个小时。

也许你会说：“这是调用者的问题，你应该更认真地阅读文档“，但在本例中，size() 方法的时间竟然不是常量级的，这是另人意外的，因为 C++ 中其他所有的容器 size 方法都是常量时间。

如果把 `size` 换成 `countSize` 或 `countElement` 那类似的错误会少些，标准库的开发者也许是出于与其他容易使用同类命名的考虑才如此做，但由于他们这个做法，导致了很多开发者容易犯这个错误。幸运的是，最新的标准库上，`size` 方法的时间复杂度已经是 o(1) 了。

> 小插曲： Wizard。
>
> 本书的一位作者，在安装  OpenBSD 时，进行到了磁盘格式化这一步，界面上显示了一个非常复杂的操作菜单，其中一项为“Wizard mode" ，他非常愉快地选择了这个选项，然而让他诧异的是，他竟然进入了一个命令行界面且没任何指引退出当前模式。显然： Wizard 这里表示的是“专家”，而非“引导”。

**如何在多个候选命名中选择**

通常在得到一个适当的命名之前，你会先有几个选项，在你脑中会对其进行思考评价最后做出决定。这里针对一个场景来模拟这个思考评价的过程：

某网站需要通过实验验证不同的页面改变对业务的影响，实验的配置如下：

```json
{
  experimentid: 100,
  description: '文本大小提高到 14pt',
  traffic_fraction: 5%,
  ...
}
````

每个配置都大约有 15对 属性/值 ，不幸的是，当你要建立新的配置时，你可能只需要改其中极少的某几项，那剩余的部分，你将要C&P ：

```json
{
  experimentid: 101,
  description: '文本大小提高到 13pt',
  ...// 其他不需要变的配置项
}
```

假设我们希望通过提供一个可复用的配置来解决这个问题，那可能会是这样的结果：

```json
{
  experimentid: 101,
  the_other_experiment_id_I_want_to_reuse: 100
  description: '文本大小提高到 13pt'
  // 其他有别于100配置的选项
}
```

ok , 现在问题来了，`the_other_experiment_id_I_want_to_reuse(复用另一id的配置)` 这个项该取个什么名字？

我们可以很快得到几个选项：

- template
- reuse
- copy
- inherit

以上几个名字对 **我们** 来说都是合适的，然而，我们还必须要想的是， 某天有个不了解这个功能的同学来读我们代码时，这个命名对他意味着什么。我们逐个分析一下：

1. template

template 有两个问题：1） 它没表明它**是**一个模板，还是它**在使用**另一个模板 2) template 一般意味抽象的事物，在使用前必须要先做必要的填充（a “template” is often something _abstract_ that must be “filled in” before it is _concrete_），会有人认为一个 template 配置不是完整真实的配置项。因此， template 在此处使用过于模糊。

2. reuse

reuse 是个合适的单词，但是一旦写下来，这个配置可以被误读成：重复使用执行 100 次，而非复用id为100 的配置。改成 reuse\_id 会有帮助，但依然可能会让使用者有这样的误读：100 是给别人重用时用的 id 。

3. copy

copy 是个好词，但同样，copy: 100 看起来像是说“复制这个配置100次”或”这是这个配置被复制的第100次“。如果要更清晰点表明“复制另一个配置”，那使用 `copy_experiment` 也许是目前最好的命名。

4. inherit

inherit ，继承，对程序员来说是非常熟悉的。对于类，inerit 意味着继承父类的所有方法和属性。即使是在现实生活中，从亲戚继承财产，你也能清晰的了解它表达的意思。

不过，加个 from 也许可以让它更清晰表达是 **从**其他配置继承而来。再进一步优化，我们可以从 `inherit_from` 改到： `inherit_from_experiment_id` 。

至此，copy\_experiment 和 inherit\_from\_experiment\_id 是最好的两个命名。因为它们描述清晰且产生误解的机率会更少。

**小结**

（略）
