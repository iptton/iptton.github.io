---
title: "Dart2.6 新特性： Static Extension Funtion"
date: "2019-12-02"
---

扩展函数在 Kotlin 中是使用非常广泛且非常受欢迎的一个特性。今天在看 dart 源码时看到这样一个语法：

```dart
extension Where<T> on Stream<T> {
  Stream<S> whereType<S>() => transform(_WhereType<S>());
  ...
}
```

印象中，dart 以前没这功能的，一查原来是[从 2.6 开始添加的新特性](https://github.com/dart-lang/language/blob/master/accepted/2.6/static-extension-members/feature-specification.md)，在 flutter stable channel 上还没有的新特性。官方设计文档不仅说明了此特性的使用方法，还详细介绍了添加这个特性背后的原因。

### 添加特性的原因

- 更具可读性

```dart
// 假设 doStuff doOtherStuff doOtherOtherStuff 都不是 thing 的原类方法
// 那通常我们的做法是在原类中添加新方法，但是如果没有此类的修改权限
// 那只能写 Helper 函数，在参数中传递 thing 的方式来实现了
doOtherOtherStuff(
  doOtherStuff(
    doStuff(thing)
  )
);

// 与上面的写法比，以下使用了 extension 的写法会更具可读性
// 译注：新的写法，函数执行顺序与其出现的顺序是一致的。
//      旧写法如果需要把执行顺序写得和出现顺序一致，则需要很多临时变量
thing.doStuff().doOtherStuff().doOtherOtherStuff();
```

- 使方法更易于被发现
    
    对 IDE 来说，扩展函数只需要 . 即可自动提示，而 helper 函数是没有这种便利的。
    

正是基于可读性和易被发现性这两个理由，dart 添加了 extension method 特性。允许你为已存在的类型添加函数。但是这些方法将是静态方法而非虚方法，这意味着，只能在指定的类型上调用这些 extension 方法，而在其子类中是无法调用的。

### 使用方法

语法：

```dart
extension MyFancyList<T> on List<T> {
  int getdoubleLength => this.length * 2;
  List<T> operator-() => this.reversed.toList();
  List<List<T>> split(int at) =>
    <List<T>>[ this.sublist(0,at), this.sublist(at) ];
  List<T> mapTotList<R>(R Function(T) convert) => this.map(convert).toList();
}
```

更准确点，其语法为：

```garmer
<extensionDeclaration> ::=
    <metadata> `extension'<identifier>? <typeParameters>? `on' <type> `{'
        (<metadata> <classMemberDefinition>)*
    `}'

<topLevelDefinition> ::= ...
    | <extensionDeclaration>
```

### 方法冲突

dart 允许你写与类型相同签名的扩展函数，之所以允许存在这种同名函数，是因为当一个类已经有某个扩展函数时，不希望在用户为类型自身添加同名函数时，出现编译时错误。那么，当扩展方法与原类型有同样签名时，会出现什么事？ 1. **同签名的方法将不可以以常规调用方式调用**。 2. **而在扩展内，`this.method` 与 `method` 不一定是同一效果的，在有冲突的情况下，后者会调用扩展本身的函数，前者会调用对象原方法**。

```dart
class A{
  void a(){// :0
    print("A:a");
  }
}

extension AE on A{
  void a(){ // :1
    print("extension:a");
  }

  void b(){
    a();  // 调用扩展本身的方法 :1
    this.a(); // 调用对象原方法 :0
  }
}

void main() {
  var a = A();
  a.a();// 调用 :0
  a.b();
}
```
