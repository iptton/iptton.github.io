---
title: "Flutter-bloc"
date: "2021-12-08"
---

## 使用篇

Flutter BLoC 是基于 BLoC 模式的 flutter 实现，使用了 provider( InheritedWidget 的一个扩充包) 和 Stream 实现相关功能。 API 也较为简单易用：

```dart
// Builder
BlocBuilder<BlocA, BlocAState>(
  condition: (previousState, state){ 
    // 非必选
    // 返回 true 则重新构建 widget，反之不处理。
  }
  bloc: blocA, // 非必选
    builder: (context, BlocAState state){
    // 返回基于 state 的 widget
  }
);

// Provider，用于做依赖注释，在树继承关系中提供唯一一个 Bloc 实例。
// 以下用法，Provider 会关闭 bloc
BlocProvider(
    create(BuildContext context) => BlocA(),
  child: xxx,
);
// 以下用法，Provider 不会关闭 bloc
// 因为 bloc 不是他创建的。
// 这个方法通常用于合建新的 router 时，但需要复用旧 Bloc 。
BlocProvider.value(
    value: BlocProvider.of<BlocA>(context),
  child:xxx,
);

// MultiBlocProvider 多 Bloc 组件
// 从
BlocProvider(
    create: (_) => BlocA(),
    child: BlocProvider(
    create: (_) => BlocB(),
    child:xxx,
  ),  
);
// 变为
MultiBlocProvider(
  providers:[
    BlocProvider(
        create: (_)=> BlocA(),
    ),
    BlocProvider(
        create: (_)=> BlocB(),
    ),
    //...
  ],
  child: xxx
);

// BlocListener
BlocListener<BlocA, BlocState>(
  bloc: BlocA(),// 可选
  condition: (previousState, state){
    // 返回 true 则响应listener，反之不做处理
  }
    listener: (context, state) {
    // 基于状态做一些操作
  },
  child:xxx
);

// MultiBlocListener 
// 与 MultiBlocProvider 类似

// BlocConsumer
// 结合了 BlocBuilder 与 BlocListener 
// api 类似
BlocConsumer<BlocA, BlocState>(
  bloc: BlocA(),// 可选
  listenerWhen: (preState, state){}, // 可选
  buildWhen:(preState, state)(), // 可选
    listener: (context, state) {
    // 可选
  },
  builder: (context, state) {
    return Container();// 
  }
);

// RepositoryProvider
// 用于做依赖注解，提供唯一的 Repository
// 在此树结构以下，可通过 context.repository<Repository>() 获取此单例
RepositoryProvider(
    create: (context) => RepositoryA(),
  child: xxx
);

// MultiRepositoryProvider 功能类似于 MultiBlocProvider
```

## 原理篇

BLoC 模式并不复杂，一张较长大概就能说明， [flutter\_bloc](https://pub.dev/packages/flutter_bloc) 只是众多 BLoC 实现的其中一个，选此插件是因为 Flultter 社区插件质量良莠不一，而这个入选了官方的 Flutter Favorite(应该是编辑推荐榜的意思？)。相对而言，可能会更稳定。

### BLoC 模式

全称 Bussiness Logic Component ，把系统分为 UI组件，业务逻辑组件，数据 三部分，从而分享业务逻辑和UI视图。BLoC 可以促进**可测性**和**重用性**。此模式把响应部分抽象成 Event 和 State 两部分，开发者大部分时间只需要关注 Event 到 State 的转换即可。

![BLoC Pattern](images/bloc_architecture.png)
