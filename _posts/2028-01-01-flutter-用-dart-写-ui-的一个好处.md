---
title: "Flutter 用 dart 写 UI 的一个好处"
date: "2019-03-20"
---

重新用 Android 原生 xml + java 模式写写代码，才能发现 flutter 用 dart 来实现 UI 的好处是什么。

举个栗子： 如果需要写一个和 flutter 内置的 Chip 组件一样的效果，Android 中的实现方式有： 写个 shape ，然后调用方在具体的 TextView::setBackgroundDrawable 。看起来挺好用的。 然而，想深一层，如果产品说还要有不同的圆角，不同的颜色，有border，无border等等等等的 Chip ，怎么办？ 基于 xml + java 的方法，只能不停地写 xml 。 而本质上这些 xml 只是某个属性不同，这些事一般我们都是通过封装接口来做，然后 xml 并没这能力...

ok : 如果 xml + java 不能解决复用问题，那是不是可以全用 java 写呢，当然可以，只是，android 提供了 xml + java 的方式，而 xml + java 的方式会比写 java 要快很多，导致很多人优先考虑这种方式 。所以问题来了，用 java 写的可复用代码，可能根本不会有人去用...
