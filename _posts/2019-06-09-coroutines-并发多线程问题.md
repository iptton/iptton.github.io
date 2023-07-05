---
title: "coroutines 并发多线程问题"
date: "2019-06-09"
---

JetBrains 出了个EDU\_TOOL，不小心打开了一个全印尼文的课程，跟着看了下 coroutines 。全程只能看懂夹杂在里面的几个英文。

之前也没深入看 coroutines 。 coroutines 解决的是“call hell"问题，但并不是解决多线程并发问题，其本质还是一个多线程封装。 下例是在这个课程代码基础上改的，容易触发并发crash的代码。

由于还没怎么学 coroutines ，所以写法可能很多问题，不过这不重要，重要的是，先把这个多线程问题记录下来，也许哪天回头看，这个“多线程”问题另有他因？或者有更好的解决方案？

```kotlin
import kotlinx.coroutines.*
import kotlin.random.Random

@ObsoleteCoroutinesApi
fun main() = runBlocking<Unit> {

    repeat(3) {
        print("try start")
        launch(Dispatchers.Default) { doWork() }.start()
        println("started ....")
    }
}
val dispatcher = newFixedThreadPoolContext(13, "myPool")
var a = mutableListOf(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
var n = 17
suspend fun doWork() = runBlocking{
    launch(dispatcher) {
        repeat(20) {
            if (a.isEmpty()){
                println("$a")
                a.add(n++)
            }else {
                var n = a[0]
                println("got $n ${a.size} ${Thread.currentThread().name}" )
                delay( Random(1000).nextLong(2000) + 1000)
                var k = a.removeAt(0)
                println("got $k $n ${a.size} ${Thread.currentThread().name}" )
            }
        }
    }.start()
}

```
