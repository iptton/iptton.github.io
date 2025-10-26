---
title: "dart: final static const"
date: "2018-10-29"
---

the differences between final/static/const in dart lang(flutter):

- final : means a variable has **only one time to be assigned** the value , not meaing the value's unmutable, but meaning the variable cannot assign an other value again.
- static : likes JAVA , meaning a **member of the class** but not any instances of it.
- const : meaning the **value ( not any variable)** and can provide better performance at runtime (especially in a listview)

ref: [const-static-final](https://news.dartlang.org/2012/06/const-static-final-oh-my.html)
