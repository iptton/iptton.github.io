---
title: "使用 powermock 解决 kotlin lateinit 问题，移除 application 依赖"
date: "2019-07-16"
---

多数情况下，Application 会被作为一个全局对象提供功能。通常的作法是给 Application 添加一个静态方法来获取其实例：

```kotlin
class MyApplication : Application() {

    companion object {
        lateinit var sBaseApp: IApplication
        val instance: IApplication
            get() = sBaseApp
    }

    init {
        sBaseApp = this
    }

    fun doSomeThing(){
      // balah balah
    }
}

class XXActivity{
  override fun onCreate(savedState:Bundle?){
    MyApplication.instance.doSomeThing()
  }
}

```

但是这样带来的问题是，怎么脱离复杂的 Application 类进行单元测试？ 纯用 `mockito` 和 `robolectic` 是无法达到目的的。这时就需要用到强大的 `powerMock`了：

```kotlin
Whitebox.setInternalState(MyApplication::class.java,"sBaseApp",app) // Powermock 提供反射修改属性的方法。
```

当然，只是上面还不够，还需要对 MyApplication 进行改造，抽象出一个 `IApplication`, 添加获取 context 的接口及其他普通接口。

```kotlin
interface IApplication {
  val context: Application // 通常这个用于提供 context 
  fun doSomeThing() // 其他能用接口
}
class MyApplication : Application(),IApplication {

    companion object {

        @JvmStatic
        lateinit var sBaseApp: IApplication

        @JvmStatic
        val instance: IApplication
            get() = sBaseApp
    }

    init {
        sBaseApp = this
    }
    override val context = this // -------------- override
    override fun doSomeThing(){ // -------------- override
      // balah balah
    }
}
```

相关测试代码：

```kotlin
@RunWith(AndroidJUnit4::class)
@Config(application = VApp::class, sdk = [28]) // 指定运行测试时使用的 Application 实例
class MainActivityTest {

    @Before
    fun setUp() {
        // 获取当前 Application 实例
        val app = ApplicationProvider.getApplicationContext<VApp>()
        // 通过 powerMock 反射修改 MyApplication 的对象
        Whitebox.setInternalState(MyApplication::class.java,"sBaseApp",app)
    }

    @Test
    fun testMain(){
        val activity = Robolectric.setupActivity(MainActivity::class.java)
    }
}
```

关键词：UninitializedPropertyAccessException, lateinit, kotlin , companion object, mockito, powermock, robolectric

kotlin.UninitializedPropertyAccessException: lateinit property sBaseApp has not been initialized
