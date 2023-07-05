---
title: "Flutter 1.12 前生成的旧 Android 项目迁移指引"
date: "2021-05-21"
---

通过 flutter create 会生成 Android 模板文件，新旧版本通常会有些不同，本文信息来自官方 wiki : [Upgrading pre 1.12 Android projects](https://github.com/flutter/flutter/wiki/Upgrading-pre-1.12-Android-projects)

**本文所说的变动，不会马上影响现存的纯 flutter 项目，在可见的未来仍旧会正常工作。（但编译时会有个烦人的提示）**

但新的 Android 模板会封装了[新的 Android 插件开发 API](https://flutter.dev/docs/development/packages-and-plugins/plugin-api-migration)，如果旧的插件需要使用新 API，则需要做迁移。

## 纯 Flutter 项目的迁移

### 如未对 Android目录做任何修改，使用方法 a, 如对 Android 目录手动有做过修改，参考方法 b。

1.a. 移除 android/app/src/main/java/your/package/name/MainActivity.java 类内容，并修改 FlutterActivity 的 import 指向。**新的 FlutterActivity 不需要手动注册 plugin**。

此时，MainActivity 类已经空，你可选择移除此类，但移除此类，需要同时修改 AndroidMainfest.xml 中对 `.MainActivity` 为 `io.flutter.embedding.android.FlutterActivity`。

1.b. 除import 修改外，还需要做些改动，见下例： 原代码：

```kotlin
class MainActivity : FlutterActivity() {

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        GeneratedPluginRegistrant.registerWith(flutterEngine)
        MethodChannle(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
+                .setMethodCallHandler(
+                    (call, result) -> {
+                        // Your existing code
+                })
    }

}
```

简言之，将 onCreate 的代码迁移至 configureFlutterEngine 中。

### 修改 AndroidManifexst.xml 和 styles.xml

2.1 移除 application 标签中的 io.flutter.app.FlutterApplication 。 2.2. 移除所有`android:name="io.flutter.app.android.SplashScreenUntilFirstFrame` 相关的 meta 2.3 设定启动图及默认界面背景。在 style.xml 中添加

```markup
<!-- You can name this style whatever you'd like -->
<style name="LaunchTheme" parent="@android:style/Theme.Black.NoTitleBar">
    <item name="android:windowBackground">@drawable/[your_launch_drawable_here]</item>
</style>

<!-- 仅出现于 Flutter 首帧出现之前 -->
<!-- You can name this style whatever you'd like -->
<style name="NormalTheme" parent="@android:style/Theme.Black.NoTitleBar">
    <item name="android:windowBackground">@drawable/[your_normal_background_drawable]</item>
</style>
```

2.4 以上 style 命名可自定义，将会在 AndroidManifest.xml 中用到：

```markup
<activity android:name=".MainActivity"
  android:theme="@style/LaunchTheme"
  // some code omitted
  >
  <!-- Specify that the launch screen should continue being displayed -->
  <!-- until Flutter renders its first frame. -->
  <meta-data
    android:name="io.flutter.embedding.android.SplashScreenDrawable"
    android:resource="@drawable/launch_background" />

  <!-- Theme to apply as soon as Flutter begins rendering frames -->
  <meta-data
    android:name="io.flutter.embedding.android.NormalTheme"
    android:resource="@style/NormalTheme"
    />

  <!-- some code omitted -->
</activity>

```

2.5 Application 标签添加 meta

```markup
<meta-data
    android:name="flutterEmbedding"
    android:value="2" />
```

## Add-to-app 迁移

此部分介绍 add-to-app 场景下的迁移

### 与纯 flutter 项目相同的步骤：

- FlutterActivity 的使用迁移，同上，子类不需要主动注册插件。
- 移除 AndroidManifest 中 `FlutterApplication`
- 更新闪屏相关配置(style.xml 及 androidManifest.xml 中的修改)
- application 标签内添加新的 meta-data

### 其他独有步骤

移除 `FlutterMain.startInitialization(...)` 或 `FlutterMain.ensureInitializationComplete(...)`，这类操作已经被自动执行。

原 `io.flutter.facade.FlutterFragment` 已废弃，使用 `io.flutter.embedding.android.FlutterFragment`

原 `Flutter.createFragment(...)` 方法应该换成以下方法：

```kotlin
FlutterFragment.createDefault()
FlutterFragment.withNewEngine()
FlutterFragment.withCachedEngine(...)
```

`FlutterView` 已废弃，使用 `io.flutter.embedding.android.FlutterView`

flutter.dev 团队的大部分插件都已经迁移，如何使用新 API ，可参考 [battery package](https://github.com/flutter/plugins/tree/master/packages/battery)

* * *

#### 迁移步骤

1. 更新 \*Plugin.java 文件，实现 `FlutterPlugin` 接口，更复杂的情况，可分为 `FlutterPlugin` 和 `MethodCallHandler` 两个类。
