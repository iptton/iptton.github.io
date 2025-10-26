---
title: "Facebook  flux 学习"
date: "2019-02-27"
---

https://github.com/facebook/flux/tree/master/examples/flux-concepts

Flux 是一种管理数据流的模式，它最重要的理念是，数据流是单向的。

Flux 包含以下模块：

- Dispatcher
- Store
- Action
- View

**Dispatcher**

dispatcher 接收事件并派发给注册了的 store 。**每个 store 都会收到所有 action**，Dispatcher 应该是每个应用仅有一个。

例：

1. 用户输入标题按下回车
2. view 获取此事件后**dispatches(派发)**一个"add-todo" action，action中带有 title 。
3. **所有 store** 收到此事件

**Store**

Store 在应用中负责保存数据。 Store 必须到 Dispatcher 中注册以便接收 action 。**Store 中的数据仅当响应 action 时才可改变** 。Store 不应该存在任何公开的 setter 方法，只能有 getter 。Store 自己决定它要响应哪些 action 。\*\*Store 的数据发生变化时，必须派发一个 event \*\*。每个应用会有多个 Store。

例

1. Store 接收到 "add-todo" action
2. Store 判断这是个和自己相关的action，把 action 中包含的数据添加到自己的数据里。
3. 派发一个 “change" event 。

> 译注：action 与 event 的区别是什么？

**Action**

Action 定义你的应用中的内部 API 。它捕获你应用中所有的交互行为。它们是个有 type 字段及其他数据的简单对象(译注：这个是具体实现了吧，好像不需要约定一定要用 type，而是应该据语言特性来决定 )

Action 应该是具有语义且对所发生的事具有描述性的。但它不应该过多描述行为的细节，如"delete-user" 会比 "delete-user-id","delete-user-data","refresh-credentials"（或其他的过程描述） 要好。

例：

1. 用户点击"delete" 按钮时，以下 action 被派发：
    
    ```json
    { type: 'delete-todo', todoID: '1234'}
    ```
    

**View**

数据从 store 被派发到 view, view层你可以使用任意框架，**如果某个 View 需要使用某个 Store 的数据，那它必须也订阅其 change 事件**。如此，当 store 发出 change 事件时，它就能获取并重新渲染了。

例：

1. 主 View 订阅了 TodoStore
2. 它获取 TodoStore 的数据以只读形式保存并渲染之等待用户操作
3. 当用户输入新的 Todo 并回车时，view 通过 Dispatcher 派发了一个 action。
4. 所有 Store 都收到了此 Action
5. TodoStore 处理了此 Action ，添加一个新的 Todo 项到其数据中，然后派发了一个 change event。
6. 主 View 接收到这个 change event，然后重新从 TodoStore 获取数据并沉浸之。

**数据流**

以上可以简述为三步：

1. View 通过 Dispatcher 派发 action
2. Dispatcher 把 action 派发给所有 Store
3. Store 发送数据给 View (译注：疑问，发送数据 ？不是View主动获取？）

![](images/flux-simple-f8-diagram-with-client-action-1300w.png)
