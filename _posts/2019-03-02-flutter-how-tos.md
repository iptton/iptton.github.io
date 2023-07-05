---
title: "Flutter how-tos"
date: "2019-03-02"
---

按钮根据用户不同的触摸显示不同图片是很常见的需求，Android 上通常可以用 Selector 来定义不同的点击态下的图片，那在 flutter 上要怎么实现呢？我们知道 Flutter 有个非常好用的 InkWell 组件，但是直接用 InkWell 显示图片，会发现图片上并没有点按的墨水效果。

```dart
InkWell(
 onTap: (){}, // 必须写 onTap 否则一定没有点按效果。
 child: Image.asset('images/icon.png'),
),
```

点进 `InkWell`源码看

```dart
/// ## Troubleshooting
///
/// ### The ink splashes aren't visible!
///
/// If there is an opaque graphic, e.g. painted using a [Container], [Image], or
/// [DecoratedBox], between the [Material] widget and the [InkResponse] widget,
/// then the splash won't be visible because it will be under the opaque graphic.
/// This is because ink splashes draw on the underlying [Material] itself, as
/// if the ink was spreading inside the material.
```

简单翻译下就是，InkWell 里的 child widget 如果有非透明图像(如设置了不透明背影色的 Container，Image, DecoratedBox 等)，则墨水效果无法显示。 因为这个效果是在child 的底下显示的。怎么办？给 child 设置一个半透明？

```dart
InkWell(
 onTap: (){}, // 必须写 onTap 否则一定没有点按效果。
 child: Opacity(child:Image.asset('images/icon.png'),opacity:0.5,),
),
```

效果是出来了，但是图片是半透明的，显然不是我们要的结果。继续看源码：

```dart
/// The [Ink] widget can be used as a replacement for [Image], [Container], or
/// [DecoratedBox] to ensure that the image or decoration also paints in the
/// [Material] itself, below the ink.
```

使用 Ink 可以避开这个问题，让图片在 Material 这一层进行绘制。

```dart
/// A convenience widget for drawing images and other decorations on [Material]
/// widgets, so that [InkWell] and [InkResponse] splashes will render over them.
```

Ink 实现的目的就是为了解决以上问题。 例：

```dart
Ink.image(
    image: AssetImage('images/tab_mine_debug.png'),
    width: 50,
    height" 50,
    fit: BoxFit.contain,
    child: InkWell(
      onTap: (){},
      //customBorder: customBorder: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(25))),
      borderRadius: BorderRadius.all(Radius.circular(25)), // 用这个来决定 墨水效果的形状，customBorder
      // 需要圆形可直接设置 customBorder: CircleBorder(), 即可
      //child: Container(color:Colors.red),// 注意，同样的理由，这个 child 是不可以有非透明元素存在的！
    ),
  ),
```

这个明显不是很好的方案，因为图片其实是一个 decoration ，装饰，因为这个接口设计得不够**直觉**。（有点类似css里的 backgroundImage ）。

继续搜索，发现 Pub 上有个 plugin 实现了这个功能: [ImageInkWell](https://pub.dartlang.org/packages/image_ink_well) 阅读下源码，发现代码也比较简单，下例为圆形按钮的实现，但它的实现方法不是用 Ink ，而是使用 Container 为外层设置 decoration ，内部点击使用了 FlatButton。按官方的建议，如果仅是为了使用 InkWell 效果不建议用 FlatButton ，因为里面的英文是全大写的（符合 Material 设计 ）。

```dart
  //var size = 36.0;
  Container(
    width: size,
    height: size,
    decoration: BoxDecoration(
      image: DecorationImage(image: AssetImage('images/icon_go.png')),
    ),
    child: FlatButton(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(size / 2),
      ),
      onPressed: onWechatLogin,
    ),
  );
```

这个插件的调用方式：

```dart
// rectangle image inkwell
ImageInkWell(
  onPressed: () {
    print('onPressed');
  },
  width: 300,
  height: 180,
  image: NetworkImage(
      'https://images.unsplash.com/photo-1547651196-4bd31258de69?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'),
  splashColor: Color(0x32ff0000),
)

// rounded rectangle image inkwell
RoundedRectangleImageInkWell(
  onPressed: () {
    print('onPressed');
  },
  width: 300,
  height: 150,
  borderRadius: BorderRadius.only(
      topLeft: const Radius.circular(20),
      topRight: const Radius.circular(20),
      bottomLeft: const Radius.circular(20)),
  image: NetworkImage(
      'https://images.unsplash.com/photo-1547332184-070705bccbd3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'),
)

// circle image inkwell
CircleImageInkWell(
  onPressed: () {
    print('onPressed');
  },
  size: 200,
  image: NetworkImage(
      'https://images.unsplash.com/photo-1547651619-238e04d07889?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'),
  splashColor: Colors.white24,
)
```
