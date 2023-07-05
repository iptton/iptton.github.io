---
title: "retrieve value from TextField"
date: "2018-10-29"
---

doing a demo to retrieve value from a input dialog. found the implementation including at least two key class:`TextEditingController` & `TextField` . you cannot get value from TextField directly (that famillar in Android) but can only access the value/event from TextEditingController.

Flutter has divided the view and controller strictly. that is nice!

```dart
const TextField(
    // the controller better define at class scope 
    // but not in this anonymouse closure, 
    // becuase you need to do get the value from that.
    controller:_controller, 
    hintText:'I am hint',
    text:'I am default text'
);
```

**important : you must dispose controller manually after using it**

```dart
  @override
  void dispose() {
    textEditingController.dispose();
    super.dispose();
  }
```
