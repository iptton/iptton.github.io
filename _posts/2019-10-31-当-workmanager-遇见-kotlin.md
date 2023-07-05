---
title: "当 WorkManager 遇见 Kotlin"
date: "2019-10-31"
---

[当 WorkManager 遇见 Kotlin](https://medium.com/androiddevelopers/workmanager-meets-kotlin-b9ad02f7405e)

这是第三篇关于 WorkManager 的文章。 WorkManager 是 Android Jetpack 中的一个异步处理库，是当前 Android 中处理后台任务的最佳实践。

以下为前两篇：

- [What WorkManager is and when to use WorkManager](https://medium.com/androiddevelopers/introducing-workmanager-2083bcfc4712)
- [How to use the WorkManager API to schedule Work](https://medium.com/androiddevelopers/workmanager-basics-beba51e94048)

本文将介绍：

- Kotlin 中使用 WorkManager
- CoroutineWorker 类
- 使用 TestListenableWorkerBuilder 测试 CoroutineWorker

### Kotlin 中使用 WorkManager

本文代码使用了 KTX 扩展，需在 build.gradle 中添加 `androidx.work:work-runtime-ktx` 依赖。

使用ktx 可以大大简化代码：

```java
Data myData = new Data.Builder()
                            .putInt(KEY_ONE_INT, aInt)
                            .putIntArray(KEY_ONE_INT_ARRAY, aIntArray)
                            ....
                            .build()
```

以上 Java 代码，可用 `workDataOf` 简化：

```kotlin
val data = workdDataOf(
    KEY_ONE_INT to aInt,
  KEY_ONE_INT_ARRAY to aIntArray,
  ...
)
```

### CoroutineWorker 类

WorkManager 除了 Java 中的 `Worker` `ListenableWorker` 和 `RxWorker` 外，Kotlin 自身有一个 `CoroutineWorker` 类。

`CoroutineWorker` 与 `Worker` 的主要区别是，前者的 `doWork` 方法是 suspend ，异步可挂起的，而后者则是同步执行任务。`CoroutineWorker` 的另一个重要特性是，它会自动处理任务的停止和取消，而 `Worker` 则需要实现 `onStopped` 方法来处理相关逻辑。

> 关于任务停止相关的信息，可详阅： [Threading in WorkManager guides](https://developer.android.com/topic/libraries/architecture/workmanager/advanced/threading).

`CoroutineWorker#doWork` 方法是 suspend 的，所以它默认会在 `Dispatchers.Default` 中执行

```kotlin
class MyWork(context: Context, params: WorkerParameters) : CoroutineWorker(context, params){
  override suspend fun doWork(): Result {
    return try{
      // do something
      Result.success()
    } catch (error: Throwable) {
      Result.failure()
    }
  }
}
```

需重点关注的是，CoroutineWorker 不同于 Worker 和 ListenableWorker ，它并不在 WorkerManager 的 Configuaration 指定的 Excutor 中执行。

### 使用 TestListenableWorkerBuilder 测试 CoroutineWorker

```kotlin
@RunWith(JUnit4::class)
class MyWorkTest {
  private lateinit var context: Context
  @Before fun setup() {
    context = ApplicationProvider.getApplicationContext()
  }
  @Test fun testMyWork() {
    val worker = TestListenableWorkerBuilder<MyWork>(context).build()

    val result = worker.startWork().get()

    assertThat(result,`is`(Result.success()))
  }
}
```
