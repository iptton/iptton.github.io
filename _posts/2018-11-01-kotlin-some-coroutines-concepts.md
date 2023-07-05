---
title: "kotlin : some coroutines concepts"
date: "2018-11-01"
---

1. one coroutine has one context,dispatcher,etc.
2. a coroutine code called a job
3. a job will be run in a thread . in Unconfined dispatcher, job may not only run in one thread.
4. since job run in threads , we need to do lock/unlock things like doing in threads.
