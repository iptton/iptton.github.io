---
title: "dart 中的 mixin"
date: "2019-02-28"
---

> 本文讨论基于 dart 2.2 环境

学过 C++ 的同学都知道，C++ 允许多重继承，在某些情况下这种能力是非常有用的。而 Dart 语言不支持多重继承，但提供了一个类似的能力：`mixins` 。 mixin 类似于类，但它的定位是：定义某些行为，这些行为可以同时为其他类复用。但这些类又不需要使用多重继承。那它是怎么实现的呢？其实可以通过文档来找答案：官方文档：[Dart 2 Mixin Declarations](https://github.com/dart-lang/language/blob/master/accepted/2.1/super-mixins/feature-specification.md#dart-2-mixin-declarations)

不过，本文想更直观点，从代码一步步找到答案：假设有以下代码 类D继承于 C，同时希望具备 A,B 的能力。正常情况下，A,B,C 应该各有不同的可复用的方法，这里选择ABC都有同一个方法这种情况来验证，**当extend 和 with 所指向的类有方法冲突时，dart 怎么办**

* * *

### 测试1

```dart
mixin A{
    foo(){
        print('A');
    }
}
mixin B{
    foo(){
        print('B');
    }
}
class C{
    foo(){
        print('C');
    }
}
class D extends C with B,A{
//    foo(){
//        print('D');
//    }
// 如果 D 方法里也有 foo 方法，则显示 D.
}
main(){
    D().foo(); // 显示 'A'
}
```

以上代码可以得到两种猜测：

当extend 和 with 所指向的类有方法冲突时

- 仅**保留最右**边的
- **优先调用最右**边的

不管上面是哪个结论其实可以得到一个结论：**父类和mixin类中有方法相同时，右边优先。**子类如果本身也有此方法，则优先使用子类的。

* * *

### 测试2

mixin 还有一个用法，可以指定mixin 只能用于哪些类：

```dart
mixin SomethingOnlyCanBeMixinWithOther on Other{

}
```

上面这个类只能被 mixin 到 Other 类里，其他类要想用则会报错

```dart
class Other with SomethingOnlyCanBeMixinWithOther{} /// 没问题
class AnOther with SomethingOnlyCanBeMixinWithOther{} /// 编译错误
```

新的测试代码，添加 on C, 并在两个 mixin 里添加 super.foo()

```dart
mixin A on C{
    foo(){
        print('A');
        super.foo();
    }
}
mixin B on C{
    foo(){
        print('B');
        super.foo();
    }
}
class C{
    foo(){
        print('C');
    }
}
class D extends C with B,A{
//     foo(){
//         print('D');
//     }
}


main(){
    D().foo(); // 输出 A B C
}
```

为了更直观，特意把 super 放到的 print 后面，输出结果即为执行的顺序。可见在用 `on` 时上一测试中判断2是对的。 而从 super 的调用来看，可以得到这样的一个推论：

**class D 继承了一个类 Ax 而 Ax 继承了一个 Bx ，Bx 继承了 Cx。这些中间的类，是dart 编译期实现（也可能并没真正存在），我们并不能在代码上直接找到 Cx Bx Ax 这些类。**

如果以上推论正确，那其实 mixin 在某种意义上也可以理解为一种**语法糖**。

* * *

### 测试3

on 允许有多个并行，这个好玩了，定义 A 只能应用于同时兼容 C 和 E 的类

```dart
mixin E{
  foo(){
    print("E");
  }
}

mixin A on C,E{ // **********
    foo(){
        print('A');
        super.foo();
    }
}
mixin B on C{
    foo(){
        print('B');
        super.foo();
    }
}
class C{
    foo(){
        print('C');
    }
}
class D extends C with B,A,E{ // ****** 注意顺序
}


main(){
    D().foo();
}
```

以上代码在 dartPad 上执行的错误如下：

```log
Error: '_D&C&B' doesn't implement 'E' so it can't be used with 'A'.
```

'\_D&C&B' 应该就是所生成的**中间类** 了，它想使用 A 时，发现并不满足 A 的约束条件 ： `on C, E` 。所以上面的结论是正确的。

调整一下 with 的顺序 为 B,E,A : 可看到输出为 ：A,E 因为 E 没有依赖，所以语法上无法调用 super（尽管实际上生成了一个中间类 Ex 是有 super 的。）,那到此就断开了。

而顺序为 E,B,A 时输出则为 A,B,E。

由此可见，多个 on 时，需要注意调用链问题，解决问题的方法是尽量用有共同约束的 mixin ，或调用 with 顺序。
