---
title: "学习笔记：《The Art of Readable Code》(1) : Surface-Level Improvement"
date: "2019-08-01"
---

## 1\. Surface-Level Improvement (表面层改进)

良好的命名，良好的注释，整齐的代码格式，我们从这些表面层改进开始。这类改变是比较容易实施的，你可以不做代码重构或修改程序的运行方式，原地( in-place )对它们进行修改，而且修改并不耗时。

这些话题是非常重要的，因为**它们影响你的每一行代码**。尽管每个修改看着都很小，但聚集起来，它们可以对代码给予巨大的贡献。有良好的命名，规范的注释和清晰的空格使用的代码，**肯定** 同时具有良好的可读性。

### 1.1 包装信息到命名中

本章告诉你如何命名

- 选择特殊的单词
- 避免取含义较泛的名字（除非你明确知道什么时候可以用）
- 使用具体命名而非抽象命名
- 用前缀或后缀提供更多信息
- 决定命名的长度
- 使用格式提供额外信息

#### 选择特殊的单词

例：

```pytho
def GetPage(url):
```

`get` 是个很空泛的单词，此命名中并未指出 page 从何而来，是来自本地 cache 还是 db 还是网络？如果是来自网络，那更好的命名是： `fetchPage` 或 `downloadPage` 。

例：

```java
class BinaryTree {
  int Size();
  ...
}
```

以上 `size` 函数我们会认为它返回什么？树的高度？节点个数？还是树所需要的内存空间？这个命名的问题是，它没提供足够的信息，更好的命名是：`height` `numNodes` `memoryBytes`

> 注:原文是C++，但我的习惯是 java/kotlin ，因此写的过程中非源码部分会使用 java 的全名习惯

例：

```java
class Thread {
  void Stop()
}
```

`stop` 这个命名是没问题的，但这取决于函数内做的事情， 给个更特殊的命名也许会更帖合实际，如：如果它执行的是一个很重的不可撤回的操作，那用 `kill` 会更好，如果有对应的 `resume` 操作，那`pause` 会更好。

#### 避免取含义较泛的名字

`tmp` `retval` 这类命名通常是不不负责的做法，它表示"我想不出一个名字来"。相对而言，使用一个能表达其内容含义的启会更好。

##### retval

如以下 JavaScript 代码:

```javascript
var euclidean_norm = function (v) {
  var retval = 0.0
  for (var i = 0; i < v.length; i += 1){
    retval += v[i] * v[i];
  }
  return Math.sqrt(retval);
}
```

这里使用 `retval` 这个临时命名，它只有一个含义“我是一个返回值”，但并没表明这个返回值是什么。

更好的作法是：`sum_squares`.

> 建议：`retval` 没带任何信息，应避免使用

##### tmp

又如以下代码：

```java
if (right < left) {
  tmp = right;
  right = left;
  left = tmp;
}
```

此例中 `tmp` 是没问题的，这个变量的唯一作用就是`临时(temporary)`存储，它的生存范围也就只在几行之内，不会被传到其他地方去。但以下代码则不同：

```java
String tmp = user.name();
tmp += " " + user.phone_number();
tmp += " " + user.email();
template.set("user_info", tmp)
```

尽管这个变量只有一个很短的生命周期，但`临时存储`并不是它最重要的使用，此时，使用 `user_info` 会更好。

而下例中，则是个适当的命名：

```java
tmp_file = tempfile.NamedTemporaryFile();
...
saveData(tmp_file)
```

因为我们用的是 `tmp_file` 而非 `tmp` ，已经指明这是一个临时文件(temporary file)。如果只用 `tmp` 那将是非常难理解的。

> 建议：`tmp` 只应在小生存范围且临时存储的场景

##### 循环遍历变量

i , j 通常用于循环遍历变量

> 本节建议使用 ci mi ui 等表示 clubIndex memberIndex userIndex ，个人不同意，使用长点命名更好。

##### 审判含义较泛的命名

如你所见，有时泛泛的命名是有必要的。

> 建议：如果需要使用含义较泛的命名，要有充分的理由

通常情况下，使用宽泛含义的命名都是源于懒。这很好理解，当你没有一个好的想法时，随便用个 `foo` 什么的命名当然是最快的，但**如果你养成习惯多想几秒使用一个好的命名，你的命名能力会很快形成"肌肉记忆"。**

#### 使用具体命名而非抽象命名

命名变量，函数或其他元素时，使用具体的命名会比抽象的命名要好。

例如：你有一个内部方法 `ServerCanStart()`用于表示 TPC/IP 端口是否可监听，这个命名一定程度上是抽象的，相比之下，用 `CanListenOnPort()` 会更具体些，这个命名直接告诉使用者它做的是什么。

**例：DISALLOW\_EVIL\_CONTRUCTORS**

> 在 C++ 基础的讨论，略。建议是用 DISALLOW\_COPY\_AND\_ASSIGN

**例：—run\_locally**

本地运行不关注性能，会打 log 等，但这个命名会带来些问题：

- 团队新人不能很快知道它的作用
- 如果 run\_localy 的差异只是打log ，那也许我们有时会需要在服务器上加这个参数，那此时就显得很诡异了
- 有时我们需要在本地进行性能测试，因此在本地跑时，又要把 run\_locally 移除

出这个问题的原因是 run\_locally 是在某些特殊场景时才使用，相比而言 —extra\_logging 会更直观。

> 译注：其实原文还有大段论述，不译了，个人认为这个参数不合适的原因是：在本地跑的情况下，有N种需求，也就是说存在很多种 run\_locally 的情况，一个参数是无法满足所有需求的，总会有些场景下这个名词所做的事与别人的理解不一致，那就**名不符实**了。

#### 用前缀或后缀提供更多信息

与`String id; // example: "af84ef845cd8"` 比使用 `hex_id` 会更可读

**例：有单位的值**

```javascript
var start = (new Date()).getTime();// top of the page
...
var elapsed = (new Date()).getTime() - start; // bottom of the page
document.writeln("Load time was: " + elapsed + " seconds");
```

以上代码没有显而易见的错误，但它是有问题的。因为 getTime 方法获取的是毫秒 (millisecond)。 而如果用一个更明显的变量名， 这个错误就很容易被发现了：

```javascript
var start_ms = (new Date()).getTime() // start_ms 表明用 ms 为单位
```

**对重要属性进行编码**

| 场景 | 变量名 | 更好的变量名 |
| --- | --- | --- |
| 后续可被加密的密码 | password | plaintext\_password |
| 用户提供的未进行转义的评论 | comment | unescaped\_comment |
| 被转为 UTF8 的 html | html | html\_utf8 |
| 已经被 url 编码的输入的数据 | data | data\_urlenc (译注：enc 这个缩写并不好) |

我们所说的是 `HUNGARIAN NOTATION(匈牙利命法)`吗？

匈牙利命法是一种被微软广泛使用的命名方式，它对“类型”做了些编码缩写：

| Name | Meaning |
| --- | --- |
| pLast | 指向最后（ **last**）一个元素的指针（**p**ointer） |
| pszBuffer | 指向一个以0结尾（**z**ero）字符串(**s**tring)的指针 |
| cch | 字符(**ch**arcters)的数量(**c**ount) |
| mpcopx | 一个**m**ap结构，key类型为：**p**ointer,指向一个颜色(**co**lor)，value类型为：**p**ointer,指向一个 **x**\-axis x轴 |

确实，他们都通过前缀提供了更多 信息，但是它是一个更正式或严格限定范围的体系，只用于特殊的属性。

我们在这节所主张的是一个适用范围更宽且更不正式的系统： identify any crucial attributes of a variable, and encode them legibly, if they’re needed at all. You might call it “English Notation.” 给变量名赋予其必须的重要属性，这也许可称之为英语命名法

#### 决定命名长度

在命名时，有个显而易见的约束是，名字不能太长。没人想读到这样一个变量：

```kotlin
newNavigationControllerWrappingViewControllerForDataSourceOfClass
```

越长的命名越难被记住，且会占用更多的屏幕空间甚至会导致折行的出现。

而短的命名，又容易陷入另一个极端，使用单个词或字母来命名。

本节给出一些相关的指引

**短命名适用于小生命周期**

当我们出去短途旅行时，通常只需要很少的行李，同理，一个生命周期很短的标志符（identefier）,也不需要带过多的信息，因为，其他信息（如：它的类型，初始值，何时被销毁等）你可以快速在上下文看到。

```c
if (debug) {
  map<string, int> m;
  lookUpNamesNumbers(&m);
  print(m);
}
```

> 译注，尽管能快速在上下文获得相关信息，但我依然不觉得单个字母的命名是合适的，因为“生命周期”太容易变化，可能这一时刻写的变量只在几行中有效，但过几天，这些代码就变成了几十行，此时 m 将成为一个阅读障碍。别寄望于后来者重构修改。

**打出长变量不再是问题**

有赖于 IDE 的各种自动补全功能。略

**缩写与简写**

通常我们会借用缩写或简写来减少命名长度，如： `BEManager` 表示 `BackEndManager` ，但是这种缩写带来的收益抵得过其带来的潜在冲突吗？

在我们的项目经验中，项目级别的简写并不靠谱，它会给新加入项目的同事带来理解上的成本，甚至对原作者来说，假以时日，让他回头再看，他也会遇到同样的问题，不理解这个缩写表示什么。

**扔掉不需要的单词**

如 `convertToString()` 可写成 `toString()` ，`doServerLoop` 可写成 `serverLoop` ，他们表达的意识依然清晰。

**使用格式来明确含义**

使用下划线，点或大写等格式也有助于提供信息，如：

```c
static const int kMaxOpenFiles = 100;

class LogReader {
  public:
    void OpenFile(string local_file);

  private:
    int offset_;
    DISALLOW_COPY_AND_ASSIGN(LogReader);
}
```

以上例子：全大小表示宏，全小写表示成员变量，后缀下划线表示私有变量等。

**其他格式方面的约定**

格式方面的约定，应参考项目所使用的语言而定。（略）

**小结**

本章只有一个主题：把信息包装到命名中。(略)
