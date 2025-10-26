---
title: "7 Pro-tips for Room"
date: "2019-11-15"
---

[7 Pro-tips for Room](https://medium.com/androiddevelopers/7-pro-tips-for-room-fbadea4bfbd1#4785)

- 预填数据：如果需要在数据库填充默认数据，可在 RoomDatabase#Callback 的 onCreate 或 onOpen 中执行。onCreate 仅在创建DB的第一次执行，onOpen 则是每次打开都会执行。

```kotlin
Room.databaseBuilder(context.applicationContext,
        DataDatabase::class.java, DB_NAME)
        // prepopulate the database after onCreate was called
        .addCallback(object : Callback() {
            override fun onCreate(db: SupportSQLiteDatabase) {
                super.onCreate(db)
                // moving to a new thread
                ioThread {
                    getInstance(context).dataDao()
                                        .insert(PREPOPULATE_DATA)
                }
            }
        })
        .build()
```

- 使用 DAO 继承能力

如果 DB 中有多个 table，那可以把相关的 Insert Update Delete 方法放到一个 BaseDao 中，因为 DAO 支持类继承。

```kotlin
interface BaseDao<T> {
    @Insert
    fun insert(vararg obj: T)
}
@Dao
abstract class DataDao : BaseDao<Data>() {
    @Query("SELECT * FROM Data")
    abstract fun getData(): List<Data>
}
```

- 使用 transactions 来执行 query 语句减少模板代码

@Transactoin 事务可组合查询，保证都执行。@Delete @Update @Insert 如果有多个参数，则它们也会被执行于一个事务中

```kotlin
@Dao
abstract class UserDao {

    @Transaction
    open fun updateData(users: List<User>) {
        deleteAllUsers()
        insertAll(users)
    }
    @Insert
    abstract fun insertAll(users: List<User>)
    @Query("DELETE FROM Users")
    abstract fun deleteAllUsers()
}
```

- 只读取你所需要的数据，以节省内存

考虑以下复杂的 User 类

```kotlin
@Entity(tableName = "users")
data class User(@PrimaryKey
                val id: String,
                val userName: String,
                val firstName: String, 
                val lastName: String,
                val email: String,
                val dateOfBirth: Date, 
                val registrationDate: Date)
```

在某些场景下，我们也许只需要使用以下信息：

```kotlin
data class UserMinimal(val userId: String,
                      val firstName:String,
                      val lastName:String)
```

那我们的DAO应该这样写：

```kotlin
@Dao
interface UserDao {
    @Query(“SELECT userId, firstName, lastName FROM Users)
    fun getUsersMinimal(): List<UserMinimal>
}
```
