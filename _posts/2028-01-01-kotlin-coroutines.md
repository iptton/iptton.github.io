---
title: "kotlin - coroutines"
date: "2018-10-31"
---

[Advanced kotlin Coroutines tips and tricks](https://proandroiddev.com/coroutines-snags-6bf6fb53a3d1)

start to use kotlin is very easy, just put long time operation in `launch` , right ? for simple cases , sure.

```kotlin
runBlocking(Dispatchers.IO) {
    withTimeout(1000) {
        val socket = ServerSocket(42)

            socket.accept() // stuck here until some one connected.
    }
}
```

[reference](https://kotlinlang.org/docs/reference/coroutines/coroutine-context-and-dispatchers.html)

```kotlin
    launch(Dispatchers.Unconfined) { // not confined -- will work with main thread
        println("Unconfined      : I'm working in thread ${Thread.currentThread().name}")
        delay(500)
        println("Unconfined      : After delay in thread ${Thread.currentThread().name}")
    }
    launch { // context of the parent, main runBlocking coroutine
        println("main runBlocking: I'm working in thread ${Thread.currentThread().name}")
        delay(1000)
        println("main runBlocking: After delay in thread ${Thread.currentThread().name}")
    }
```

Unconfined context, after suspension point , the thread will change to other thread,not the original thread. **Unconfined dispatcher should not be used in general code.**

code below can produce a multi-thread problem. because sell & sell2 (maybe) run on diffrent thread.

```kotlin
fun main() {
    runBlocking(CoroutineName("main")) {
        produce()
        sell()
        sell2()
        delay(100000)
    }
}
var items:String = ""

fun produce(){
    GlobalScope.launch(Dispatchers.IO){
        println(Thread.currentThread().name)
        while(isActive){
            delay(Random.nextInt(500,1000).toLong())
//            delay(500)
            items += "A"
//            println("items in produce $items")
        }
    }
}

fun sell(){
    GlobalScope.launch(Dispatchers.Default){
        println(Thread.currentThread().name)
        while(isActive){
            delay(Random.nextInt(500,1000).toLong())
//            delay(500)
            if(items.isNotEmpty()){
                println("1.drop \n$items")
                items = items.substring(0,items.length-1)
                println(items)
            }
        }
    }
}
fun sell2(){
    GlobalScope.launch(Dispatchers.Default){
        println(Thread.currentThread().name)
        while(isActive){
            delay(Random.nextInt(500,1000).toLong())
//            delay(500)
            if(items.isNotEmpty()){
                println("2.drop \n$items")
                items = items.substring(0,items.length-1)
                println(items)
            }
        }
    }
}
```
