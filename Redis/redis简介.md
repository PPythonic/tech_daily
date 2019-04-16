# 什么是Redis
* Redis是互联网技术领域使用最为广泛的存储中间件，它是`"Remote Dictionary Service"`（远程字典服务）的首字母缩写。
* 缓存是Redis使用最多的领域。

# Redis基础数据结构
Redis有5种基础的数据结构：
>1. string(字符串)

    字符串string是Redis最简单的数据结构，string的内部表示就是一个字符数组。Redis所有的数据结构都是以一个唯一的key字符串作为名称，然后通过这个唯一的key来获取相应的value数据。不同类型的数据结构的差异就在于value的结构不一样。
    字符串结构使用非常广泛，一个常见的用途就是缓存用户信息。我们将用户信息结构体使用JSON序列化成字符串，然后将序列化的字符串塞进Redis来缓存。同样，取用户信息会经过一个反序列化过程。
    Redis的字符串是动态字符串，是可以修改的字符串，内部结构的实现类似Java的ArrayList，采用预分配冗余空间的方式来减少对内存的频繁操作。

    举个栗子：（键值对)
    > set name wjn
    OK
    > get name
    "wjn"
    > exists name
    (integer) 1
    > del name
    (integer) 1
    > get name
    (nil)
    支持简单的增删改查操作。上面代码中的"name"就是字典中的key，而value就是字符串"wjn"。
    --> 批量键值对，节省网络耗时开销
    > mset name1 zhangsan name2 lisi name4 wangwu
    OK
    > mget name1 name2 name3
    "zhangsan"
    "lisi"
    "wangwu"
    --> 过期和set命令扩展
    可以对key设置过期时间，到时间会被自动删除，这个功能常用来控制缓存的失效时间。
    > set name wjn
    OK
    > expire name 5   # 5s后过期
    ...   # 等候5s
    > get name
    (nil)
    > setex key seconds value  # 等价于set + expire
    > setnx key value   # 如果key不存在就执行set创建
    -->  计数
    > set age 18
    OK
    > incr age
    (integet) 19
    > incrby age 5
    (integer) 24

>2. list

    Redis的链表相当于Java的LinkedList，注意它是链表而不是数组，这意味着list的插入和删除操作都非常快，时间复杂度为O(1)，但是索引定位很慢，时间复杂度为O(n)。

    Redis的列表结构常用来做异步队列处理。将需要延后处理的任务结构体序列化为字符串，塞进Redis的列表，另一个线程从这个列表中轮询数据进行处理。

    【右边进左边出，队列】  队列是先进先出的数据结构，常用来做消息队列和异步逻辑处理，它会确保元素的访问顺序性。
    > rpush books java python js
    (integer) 3
    > llen books
    (integer) 3
    > lpop books
    "java"

> hash(字典)

Redis的字典相当于java的HashMap，它是无需字典，`Redis字典的值只能是字符串`。

    > hset books code1 "java"
    (integer) 1
    > hmset books code2 "python" code3 "js"
    OK
    > hgetall books   # key和value间隔出现
    "code1"
    "java"
    "code2"
    "python"
    "code3"
    "js"
    > hlen books
    (integer) 3

同字符串一样，字典的单个子key也可以进行计数，它对应的指令是hincrby。