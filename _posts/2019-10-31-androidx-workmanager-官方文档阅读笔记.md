---
title: "AndroidX: WorkManager 官方文档阅读笔记"
date: "2019-10-31"
---

通过 WorkManager ，你指定执行的约束条件，然后可以放手把任务交给系统来执行。如果需要确认 WorkManager 是否你要的解决方案，可以详阅 [background processing guide](https://developer.android.com/guide/background/).

## 使用入门

Worker 和 AsyncTask 的 API 设计极像：

```kotlin
class UploadWorker(context:Context, params: Workerparameters) 
        : Worker(context,params) {
    override fun doWorkd(): Result {
    uploadImage()
    return Result.success()
  }      
}
```

doWork 方法就像 AsyncTask 里的 doInBackground ，而启动 Worker 的方法是：`Worker#startWork` 但是这个方法不需要我们调用，我们可直接通过 WorkManager 来把任务入栈

```kotlin
WorkManager.getInstance(requireContext()).enqueue(
            OneTimeWorkRequestBuilder<GetChannelWorker>().build()
        )
```

WorkManager#enqueue ( WorkRequest ) 可以把任务入队列执行

> 疑问，任务优先级如何处理？

## 定义 WorkRequest

上一节说了如何简单地创建一个 `WorkRequest` 并入队执行，本节我们将:

- 为任务添加约束条件（如网络是否可用）
- 设置任务执行的最小延迟时间
- 设置任务重试及back-off 策略
- 设置任务输入输出
- 任务做标记分组

### 任务约束条件

我们可通过 `Constraints` 指定任务仅在设备插电时或闲时执行

```kotlin
val constrains = Constrains.Builder()
    .setRequiresDeviceIdle(true)
    .setRequiresCharging(true)
    .build()

val compressionWork = OneTimeWorkRequestBuilder<CompressWorker>()
    .setConstraints(constrains)
    .build()
```

如果有多个约束，那任务会在所有约束条件都满足时才能执行。

如果约束指定的条件在任务执行过程中发生变化，WorkManager 会自动暂停任务，在重新满足条件后才会再次执行（**疑问：如果是 CoroutineWorker ，任务是被 resume 还是 restart ? 如果是 Worker ，应该是线程执行，如何做到停止线程？**）

### 初始延迟

如果你希望任务不是马上被执行（注：一般是性能相关？），可设置初始延迟时间 ：

```kotlin
val uploadWorkRequest = OneTimeWorkRequestBuilder<UploadWorker>()
    .setInitialDelay(10, TimeUnit.MINUS)
    .build()
```

### 重试及back-off策略

在 Worker 中可通过 Result.retry() 来重试任务。back-off 策略有两种，一是指数一是线性，

即下次重试的间隔时间为 1 2 4 8 16 秒递增，还是 1 1 1 1 1 1 秒这样的线性数字

```kotlin
val uploadWorkRequest = OneTimeWorkRequestBuilder<UploadWorker>()
        .setBackoffCriteria(
                BackoffPolicy.LINEAR,
                OneTimeWorkRequest.MIN_BACKOFF_MILLIS, // 当前值是10,000 即10秒，默认重试时间为30秒
                TimeUnit.MILLISECONDS)
        .build()
```

### 设置任务输入输出

所有输入输出都是通过一个 key-value 对的 `Data` 对象来传递：

```kotlin
// workDataOf (part of KTX) converts a list of pairs to a [Data] object.
val imageData = workDataOf(Constants.KEY_IMAGE_URI to imageUriString)

val uploadWorkRequest = OneTimeWorkRequestBuilder<UploadWorker>()
        .setInputData(imageData)
        .build()
```

Worker 通过 getInputData 可获得此对象，类似的在 Result.success / Result.failure 方法里，可以传递一个 Data 对象返回。

### 任务打标记分组

任务可以通过标记来分组

```kotlin
val cacheCleanupTask =
        OneTimeWorkRequestBuilder<CacheCleanupWorker>()
    .setConstraints(constraints)
    .addTag("cleanup")
    .build()
```

分组的好处是，你可以批量地操作任务：`WorkManager#cancelAllWorkByTag(String)` `WorkManager#getWorkInfosByTagLiveData(String)` 等

## 观察任务状态

### 任务状态(Work State)

任务在生命周期中有多个状态：

- **BLOCKED** : 如果此任务设置了前置任务，且前置任务未执行完，则当前任务处于 BLOCK 状态
- **ENQUEUED**: 任务处于等待约束条件达到或轮到的执行的状态
- **RUNNING**: 执行中
- **SUCCEEDED**:执行成功状态，这是终结状态，只有 **OneTimeWorkRequest**可能进入此状态
- **FAILED**: 同上，所不同的是，如果有别的任务依赖此任务，那它们也会被标记为 FAILED 且不会执行下去（**疑问：如果它们不是 OneTimeWorkRequest 呢？**）
- **CANCELLED**: 显式地取消一个未结束的请求，则它会进入此状态。依赖于此任务的其他所有任务也同样会被标记为此状态且不会执行。

### 观察任务状态

任务被加入 WorkManager 队列后，可通过 `WorkInfo` 对象获取其状态信息，里面含有 id / tag / state / output-data 。

获取 WorkInfo 有三种办法：

```kotlin
// 单个 Request
WorkManager.getWorkInfoById(UUID) 
WOrkManager.getWorkInfoByIdLiveData(UUID)

// 给定 tag
WorkManager.getWorkInfoByTag(String)
WorkManager.getWorkInfoByTagLiveData(String)

// 给定任务名称
WorkManager.getWorkInfoByUniqueWork(String)
WorkManager.getWorkInfoByUniqueWorkLiveData(String)
```

带 LiveData 的调用，可通过其返回的 LiveData 进行监听：

```Kotlin
WorkManager.getInstance(myContext).getWorkInfoByIdLiveData(uploadWorkRequest.id)
        .observe(lifecycleOwner, Observer { workInfo ->
            if (workInfo != null && workInfo.state == WorkInfo.State.SUCCEEDED) {
                displayMessage("Work finished!")
            }
        })
```

### 观察任务中间进度

自 `2.3.0-alpha01` 开始，WorkManager 支持监听任务的中间进度变化。使用 `Worker#setProgressAsync` 方法即可通知使用 LiveData.Observe 的回调获得通知。

（**注意，此处的 setProgress 和 setProgressAsync 都没有线程调度。**）

## 将任务连起来

WorkManager 允许按指定顺序执行任务

```kotlin
WorkManager.getInstance(myContext)
    // Candidates to run in parallel
    .beginWith(listOf(filter1, filter2, filter3))
    // Dependent work (only runs after all previous work in chain)
    .then(compress)
    .then(upload)
    // Don't forget to enqueue()
    .enqueue()

```

`beginWith` 函数返回一个 `WorkContinuation` 对象，`WorkContinuation#then` 则同样返回一个 `WorkContinuation` 对象。

一个复杂点的例子：（实际上 WorkContinuation#combine 源码注释上就有）

1. 获得上传 CDN 的 KEY(A0)
2. 上传视频(A1)，
3. 获得上传 CDN 的 KEY(B0)
    
4. 上传封面(B1)，
    
5. 根据以上两个上传后得到的 URL 调用PB协议 (C)

预期的顺序为 ( A, B)并行然后 C

  A0   B0
  |    |
  A1   B1
  -------
     |
     C

```kotlin
val workManager: WorkManager = WorkManager.getInstance()
        val uploadVideo = workManager
                .beginWith(getVideoKeyWorker)
                .then(uploadVideoWorker)
        val uploadVideoThumb = workManager
                .beginWith(getVideoThumbWorker)
                .then(uploadVideoThumbWorker)

        WorkContinuation.combine(uploadVideo,uploadVideoThumb)
                                .then(invokePBWorker)
                .enqueue()
```

顺序调用的任务，前一任务的输出会自动成为下一任务的输出，但如果前一任务为并发的几个任务要怎么办？这里就需要用到 **setInputMerger** 方法了。系统提供两类Merger: **ArrayCreatingInputMerger** 和 **OverwritingInputMerger** 当遇到相同key时，前者会在此key下创建一个数组把所有值放进去（这个算法会稍为复杂，可以看源码注释），后者会根据顺序，后来者覆盖前值。

```kotlin
WorkContinuation.combine(uploadVideo,uploadVideoThumb)
                                .setInputMerger(ArrayCreatingInputMerger::class) // 注意这行
                                .then(invokePBWorker)
                .enqueue()
```

## 取消/停止任务

```kotlin
WorkManager.cancelWorkById(UUID)
WorkManager.cancelWorkByTag(String)
WorkManager.cancelUniqueWork(String)
```

调用以上接口时，如果任务处于完成状态，不会有任何作用，如果处理**RUNNING** 状态，则会调用`LisenableWorke#onStopped` 方法，以便做些清理操作。**疑问：如何做到取消的？**

```kotlin
    internal class ThreadWorker(ctx: Context,parameters: WorkerParameters)
        : Worker(ctx,parameters) {
        override fun doWork(): Result {
            var i=0
            while(i<10) {
                Thread.sleep(500)
                setProgressAsync(workDataOf("progress" to "${i++}"))
            }
            println("on success")
            return Result.success()
        }

        override fun onStopped() {
            super.onStopped()
            println("on Stopped")
        }

    }

    private fun cacnelTask() {
        val req = OneTimeWorkRequestBuilder<ThreadWorker>().build()
        WorkManager.getInstance(applicationContext).enqueue(req)
        WorkManager.getInstance(applicationContext)
            .getWorkInfoByIdLiveData(req.id)
            .observe(this,androidx.lifecycle.Observer {
            findViewById<TextView>(R.id.output).text = "result:${it.progress.getString("progress")}"
        })

        thread {
            Thread.sleep(2000)
            WorkManager.getInstance(applicationContext).cancelWorkById(req.id)
        }
    }
```

> 上例可看到，实际上 cancel 后线程并没有结束执行。但是 WorkManager 不会把 Result.success 抛给 observer 。可在 doWork 内检测 isStopped 。

## 处理重复性任务

与 `OneTimeWorkRequest` 相对的是 `PeriodicWorkRequest` ，后者**可重复地执行，但不能被连起来。**

```kotlin
val constraints = Constraints.Builder()
        .setRequiresCharging(true)
        .build()

val saveRequest =
PeriodicWorkRequestBuilder<SaveImageToFileWorker>(1, TimeUnit.HOURS)
    .setConstraints(constraints)
    .build()

WorkManager.getInstance(myContext)
    .enqueue(saveRequest)

```

**注意，和 `JobScheduler` 一样，重复执行的最短时间是15分钟**

## 特定任务

Unique Work 指的是给写名字的任务 ，使用方法：

```kotlin
WorkManager.enqueueUniqueWork(String, ExistingWorkPolicy, OneTimeWorkRequest)
WorkManager.enqueueUniquePeriodicWork(String, ExistingPeriodicWorkPolicy, PeriodicWorkRequest).
```

第一个参数为名字，第二个参数指定当 Manager中已经存在相同名字任务时的冲突策略，第三个为具体任务。

冲突策略有三种：REPLACE / KEEP / APPEND 分别代表：取消旧的执行新的 / 保留旧的忽略新和 / 新的排在旧的后面共同执行。 第三个是一个连接，所以不能用于 PeriodicWorkRequest 。

**疑问：如果有一个 Unique 任务已经执行完成，再次执行，会冲突吗？从注释上看，应该不会，从设计角度考虑，也不应该冲突。**

## 测试

**注：worker 的测试其实是把异步变成同步，测试结果并不准确**

对于延时，约束条件，定时等则是通过 testDriver 来模拟条件触达。

```kotlin
@RunWith(AndroidJUnit4::class)
class BasicInstrumentationTest {
    @Before
    fun setup() {
        val context = InstrumentationRegistry.getTargetContext()
        val config = Configuration.Builder()
            // Set log level to Log.DEBUG to make it easier to debug
            .setMinimumLoggingLevel(Log.DEBUG)
            // Use a SynchronousExecutor here to make it easier to write tests
            .setExecutor(SynchronousExecutor())
            .build()

        // Initialize WorkManager for instrumentation tests.
        WorkManagerTestInitHelper.initializeTestWorkManager(context, config)
    }

  @Test
  @Throws(Exception::class)
  fun testSimpleEchoWorker() {
      // Define input data
      val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

      // Create request
      val request = OneTimeWorkRequestBuilder<EchoWorker>()
          .setInputData(input)
          .build()

      val workManager = WorkManager.getInstance(applicationContext)
      // Enqueue and wait for result. This also runs the Worker synchronously
      // because we are using a SynchronousExecutor.
      workManager.enqueue(request).result.get()
      // Get WorkInfo and outputData
      val workInfo = workManager.getWorkInfoById(request.id).get()
      val outputData = workInfo.outputData
      // Assert
      assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
      assertThat(outputData, `is`(input))
  }
  @Test
  @Throws(Exception::class)
  fun testWithInitialDelay() {
      // Define input data
      val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

      // Create request
      val request = OneTimeWorkRequestBuilder<EchoWorker>()
          .setInputData(input)
          .setInitialDelay(10, TimeUnit.SECONDS)
          .build()

      val workManager = WorkManager.getInstance(getApplicationContext())
      val testDriver = WorkManagerTestInitHelper.getTestDriver()
      // Enqueue and wait for result.
      workManager.enqueue(request).result.get()
      testDriver.setInitialDelayMet(request.id)
      // Get WorkInfo and outputData
      val workInfo = workManager.getWorkInfoById(request.id).get()
      val outputData = workInfo.outputData
      // Assert
      assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
      assertThat(outputData, `is`(input))
  }
  @Test
  @Throws(Exception::class)
  fun testWithConstraints() {
      // Define input data
      val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

      val constraints = Constraints.Builder()
          .setRequiredNetworkType(NetworkType.CONNECTED)
          .build()

      // Create request
      val request = OneTimeWorkRequestBuilder<EchoWorker>()
          .setInputData(input)
          .setConstraints(constraints)
          .build()

      val workManager = WorkManager.getInstance(myContext)
      val testDriver = WorkManagerTestInitHelper.getTestDriver()
      // Enqueue and wait for result.
      workManager.enqueue(request).result.get()
      testDriver.setAllConstraintsMet(request.id)
      // Get WorkInfo and outputData
      val workInfo = workManager.getWorkInfoById(request.id).get()
      val outputData = workInfo.outputData
      // Assert
      assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
      assertThat(outputData, `is`(input))
  }
  @Test
  @Throws(Exception::class)
  fun testPeriodicWork() {
      // Define input data
      val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

      // Create request
      val request = PeriodicWorkRequestBuilder<EchoWorker>(15, MINUTES)
          .setInputData(input)
          .build()

      val workManager = WorkManager.getInstance(myContext)
      val testDriver = WorkManagerTestInitHelper.getTestDriver()
      // Enqueue and wait for result.
      workManager.enqueue(request).result.get()
      // Tells the testing framework the period delay is met
      testDriver.setPeriodDelayMet(request.id)
      // Get WorkInfo and outputData
      val workInfo = workManager.getWorkInfoById(request.id).get()
      // Assert
      assertThat(workInfo.state, `is`(WorkInfo.State.ENQUEUED))
  }
}
```

在2.1.0之后的版本，`WorkManagerTestInitHelper.initializeTestWorkManager` 已经不是必要的了，可以直接使用 TestListenableWorkerBuilder 和 TestWorkerBuilder 来测试 worker 。

```kotlin
@RunWith(AndroidJUnit4::class)
class SleepWorkerTest {
    private lateinit var context: Context

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
    }

    @Test
    fun testSleepWorker() {
        // Kotlin code can use the TestListenableWorkerBuilder extension to
        // build the ListenableWorker
        val worker = TestListenableWorkerBuilder<SleepWorker>(context).build()
        runBlocking {
            val result = worker.doWork()
            assertThat(result, `is`(Result.success()))
        }
    }
}

```

```kotlin
// Kotlin code can use the TestWorkerBuilder extension to
// build the Worker
@RunWith(AndroidJUnit4::class)
class SleepWorkerTest {
    private lateinit var context: Context
    private lateinit var executor: Executor

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
        executor = Executors.newSingleThreadExecutor()
    }

    @Test
    fun testSleepWorker() {
        val worker = TestWorkerBuilder<SleepWorker>(
            context = context,
            executor = executor,
            inputData = workDataOf("SLEEP_DURATION" to 10000L)
        ).build()

        val result = worker.doWork()
        assertThat(result, `is`(Result.success()))
    }
}
```
