---
title: Jetpack Compose - Starter
tags: [Jetpack Compose, Kotlin]
---

# 基本概念
Jetpack Compose 与日常的 Android View 开发相比，有大量的新概念需要了解，有通用的，也有 Compose 自身专有的，本节介绍这些概念，以让读者能快速跨过最初的门槛。

## 1. 声明式 vs 命令式

Jetpack Compose 以声明式的方式来描述界面样式和交互。通过简单地描述数据与界面的关系，将界面的生成过程与数据变化的响应紧密结合。与传统的命令式方式不同，Jetpack Compose 的声明式设计使得开发人员能够更加轻松地构建复杂而美观的用户界面。这一创新性的方法为开发者带来了更高效、更灵活的界面开发体验。

以一个弹窗逻辑为例说明命令式与声明式的区别：例 1 为传统 Android View 实现，例 2 为 Jetpack Compose 实现：

例1：传统 Android View 实现 (命令式)

```java
public class MainActivity extends AppCompatActivity {
    private AlertDialog alertDialog;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button showButton = findViewById(R.id.show_button);
        showButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showAlertDialog();
            }
        });
    }

    private void showAlertDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("警告");
        builder.setMessage("这是一个警告窗口");
        builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });
        alertDialog = builder.create();
        alertDialog.show();
    }
}
```

例2：Jetpack Compose 实现 (声明式)

```kotlin
public class MainActivity extends AppCompatActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContent {
	        MainContent()
        }
    }
}
@Composable
fun MainContent() {
    var isAlertDialogVisible by remember { mutableStateOf(false) }

    Column {
        Button(
            onClick = { isAlertDialogVisible = true }
        ) {
            Text(text = "点击显示警告")
        }

        if (isAlertDialogVisible) {
            AlertDialog(
                onDismissRequest = { isAlertDialogVisible = false },
                title = { Text(text = "警告") },
                text = { Text(text = "这是一个警告窗口") },
                confirmButton = {
                    Button(
                        onClick = { isAlertDialogVisible = false }
                    ) {
                        Text(text = "确定")
                    }
                }
            )
        }
    }
}
```

在传统 Android View 实现中，我们需要手动管理弹窗的创建和显示，以及监听按钮点击事件和对话框按钮的点击事件。这种方式更加命令式，需要手动控制每一个步骤和状态的变化。

而在Jetpack Compose实现中，我们使用了声明式的方式来描述界面的结构和交互逻辑。我们只需要定义一个`isAlertDialogVisible`的状态变量，当点击按钮时，更新该变量的值，Compose会自动根据状态的变化来更新界面。这种方式更加简洁、易于理解和维护，不需要手动管理每个步骤和状态的变化。

总的来说，声明式编程更加直观和简洁，能够提高代码的可读性和可维护性。它将关注点放在描述事物的状态和关系上，而不是具体的操作步骤。命令式编程则更加注重具体的操作步骤和状态的变化，需要手动管理和控制每个步骤的执行。

## 2.  驱动 UI 变化的根源：State

在上一节的示例中，我们可以看到声明式的好处。它会自动帮我们处理数据和界面的关系，当数据发生变化时，它会自动更新界面。这样，我们就不需要手动去告诉界面要做什么。但这是有条件的，这背后的一个非常重要概念就是 *State* (状态)，这既是一个专有术语，在 Compose 中也同时是一个数据类型，所有能自动绑定 UI 变化的都必须是 *State* 类型。上例中的 `mutableStateOf` 就是创建 State 的一个方式，在看 compose 代码时，请注意这一点，所有能驱动 UI 变化的变量，都必然是 `State` 对象，它可能是 `mutableStateOf` 声明，也可能是其他方式声明。如果你在写 demo 时发现*变量*变了但 UI 没发生变化，那先检查一下你的变量是否 `State` 类型。

Compose 中有两个数据类型会被追踪变化并自动更usrs UI :

```kotlin
interface State<out T> {
	val value: T
}
interface MutableState<T>: State<T> {
	override var value:T
}
```


## 3. UI 树：节点即显示

第一节 Compose 例子我们可以看到，AlertDialog 并没有调用 `show` / `dismiss` 之类的方法，那它是怎么显示和隐藏的？这是 Compose 和传统 View 的一个关键区别，UI 节点的添加与移除不需要用户显式地执行，compose 在背后帮你写了，你只需要声明即可。以添加一个文本为例：

传统 Android View 需要以下步骤（使用 XML 本质也是通过以下步骤完成）
```kotlin
val waringTipView = TextView(context).apply {
    text = "hello world"
}
val showTipLiveData: LiveData = viewModel.shouldShowText()
showTipLiveData.observe{ showTip -> // 监听 livedata 的变化
	if (showTip) {
	    viewGroup.addView(waringTipView)
	} else {
		viewGroup.removeView(waringTipView)
	}
}
```
而 Compose 则是：
```kotlin
@Composable
fun WarningTip(viewModel: SomeViewModel) {
	val showTip by viewModel.shouldShowText().observeAsState() // 监听 livedata 变化
	if (showTip) {
		Text("hello world")
	} // else 呢？
}
```

先忽略 `oberveAsState` 方法和 Text 与 TextView 的构造，两个写法有两处最大的区别：
- Compose 没有 addChild 操作
- Compose 没有 removeChild 的 else 逻辑

了解为什么 Compose 没有 addChild 和 removeChild 这两行


## 3. UI是如何变化的：重组与位置记忆 (Recomposition and Positioned Memorization)

每当`State`对象的值发生变化时，Compose会自动重新绘制UI以反映新的值。

例如，假设我们有一个名为`count`的整数状态变量。我们可以使用以下代码创建并更新该状态变量：

```kotlin
val count = remember { mutableStateOf(0) }

count.value = 10 // 更新count的值为10
```

然后，我们可以在Compose函数中使用该状态变量来定义UI组件。例如，我们可以显示当前计数的文本和两个按钮来增加和减少计数值：

```kotlin
@Composable
fun Counter() {
    val count = remember { mutableStateOf(0) }

    Column {
        Text(text = "Count: ${count.value}")

        Button(onClick = { count.value++ }) {
            Text(text = "Increase")
        }

        Button(onClick = { count.value-- }) {
            Text(text = "Decrease")
        }
    }
}
```

在上面的例子中，我们首先使用`remember { mutableStateOf(0) }`创建了一个初始值为0的状态变量 `count`。然后，在UI组件中使用该状态变量进行渲染。

当点击“增加”按钮时，我们通过将 `count.value++` 将计数器增加1，并且Compose会自动重新绘制UI以反映新的计数值。

同样地，当点击“减少”按钮时，我们通过将 `count.value--` 将计数器减少1，并且Compose会自动重新绘制UI以反映新的计数值。

这就是Jetpack Compose中绑定UI的基本概念。通过使用`State`对象，我们可以轻松地将数据与界面进行关联，并让Compose自动处理UI的更新。

## ReplaceableGroup

返回 Unit 的 Composable 函数会生成  RestartableGroup，而返回非 Unit 值的返回的则是 ReplaceableGroup:

```kotlin
@Composable
fun getInt(): Int {
	return 1234
}
```

生成以下代码：(去掉 liveLiteral 和 源码映射后)
```java
    @Composable
    public static final int rememberId(@Nullable Composer $composer, int $changed) {
        $composer.startReplaceableGroup((int)-662017609);
        int n = 1234;
        $composer.endReplaceableGroup();
        return n;
    }
```