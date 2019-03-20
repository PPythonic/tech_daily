## 0. 参考地址
基本介绍 https://www.cnblogs.com/yinheyi/p/8127871.html

实验演示 https://www.cnblogs.com/xybaby/p/6406191.html#_label_2

详细讲解 http://aju.space/2017/07/31/Drive-into-python-asyncio-programming-part-1.html

官方文档selecotors  https://docs.python.org/3/library/selectors.html

官方文档select https://docs.python.org/3/library/select.html

## 1. 前言
并发的解决方案中, 因为阻塞IO调用的原因, 同步模型(串行/多进程/多线程)并不适合大规模高并发, 在非阻塞IO调用中, 我们可以使用一个线程完成高并发的功能, 不过因为非阻塞IO会立即返回, 如何判断IO准备就绪以及就绪之后如何处理就成了关键, 所以我们需要额外的处理.

不论使用哪一种额外处理方式, 核心都是为了获知IO准备就绪并执行对应的操作, 额外处理方式就是`回调+事件循环`

`OS`已经为我们提供了`select/poll/epoll/kqueue`等多种底层操作系统接口以处理IO准备就绪的通知(即通过`OS`提供的接口可以方便的编写事件循环). 而程序还需要完成: **如何在IO准备就绪的时候完成预定的操作**

`selecotrs`模块,总代码`611`行,其中有`5`个类是同一个级别,只是根据`OS`的类型而有所不同.模块中还包含大量的注释,所以核心代码数量就在`100`行左右.`selectors`模块为我们提供了异步编程中的回调模型(后面还会写异步编程中的协程模型),所以我觉得对此模块的研究是很有必要的.


## 2. 核心类
`selectors`模块中的核心类如下:
![](https://images2018.cnblogs.com/blog/1381809/201807/1381809-20180729094240015-564913257.jpg)

---
`BaseSelector`是一个抽象基类, 定义了核心子类的函数接口. `BaseSelector`类定义的核心接口如下:
```python
@abstractmethod
register(self, fileobj, events, data=None) # 提供文件对象的注册

@abstractmethod
unregister(self, fileobj)  # 注销已注册的文件对象

@abstractmethod
select(self, timeout=None) # 向OS查询准备就绪的文件对象
```
其中, 前两个函数封装了文件对象, 并提供了`data`变量用于保存附加数据, 这就提供了回调的环境, 第三个函数`select`是对`OS`底层`select/poll/epoll`接口的封装,用以提供一个统一的对外接口.

`_BaseSelectorImpl`:是一个实现了`register`和`unregister`的基类,注意,此基类并没有实现`select`函数,因为`select`函数在不同`OS上`使用的底层接口不同,所以应该在对应的子类中定义.

`SelectSelector`:使用`windows`时的接口
`EpollSelector`:使用`linux`时的接口(其他`3`个类相似,只是应用于不同的`OS`)
`DefaultSelector`:此为类别名,`selectors`模块会根据所在操作系统的类型,选择最优的接口.

如下只对`selectselector`类的核心代码进行分析,其他对应类的代码逻辑基本一致.

## 3. SelectSelector核心函数代码分析
有名元祖`selectorkey`
```python
Selectorkey = namedtuple('Selectorkey', ['fileobj', 'fd', 'events', 'data'])
```
此对象是一个有名元组, 可以认为是对文件对象`fileobj`, 对应的描述符`fd`, 对应的事件`events`, 附带的数据`data`这几个属性的封装. **此对象是核心操作对象**, 关联了需要监控的文件对象, 关联了需要`OS`关注的事件,  保存了附带数据(*其实这里就是放的回调函数*)

### 3.1 注册
```python
def __init__(self):
    super().__init__()
    self._readers = set()  # 使用集合处理唯一性
    self._writers = set()
```
首先, 构造函数中定义了`_reader`和`_writer`变量用于保存需要监听的文件对象的文件描述符值, 并使用集合特性来处理唯一性.

```python
def register(self, fileobj, events, data=None):
    key = super().register(fileobj, events, data)
    if event & EVENT_READ:
        self._readers.add(key.fd)
    if event & EVENT_WRITE:
        self._writers.add(key.fd)
    return key
```
一般我们使用`register`作为第一个操作的函数, 代表着**你需要监听的文件对象, 以及, 当它发生你关注的事件时, 你要如何处理**.

此函数有`3`个参数,分别是文件对象,监听事件(可读为`1`,可写为`2`),附带数据.

`fileobj`文件对象是类文件对象,与平台强相关,在`windows`上只能是`socket`,在`linux`上可以是任何`linux`支持的文件对象.

`events`是一个`int`类型的值,就是`EVENT_READ`和`EVENT_WRITE`

`data`是附带数据,我们可以把回调函数放在这里

此函数返回的`key`就是一个`selectorkey`有名元祖,
`register`函数将用户监听的文件对象和事件注册到有名元祖中,并加入监听集合`_readers`和`_writers`中.

### 3.2 注销
```python
def unregister(self, fileobj):
    key = super().unregister(fileobj)
    self._readers.discard(key.fd)
    self._writers.discard(key.fd)
    return key
```
当我们不需要监听某一个文件对象时,使用`unregister`注销它.这会使得它从`_readers`和`_writers`中被弹出.

### 3.3 查询
```python
def select(self, timeout=None):
    timeout = None if timeout is None else max(timeout, 0)
    ready = 0
    try:
        r, w, _ = self._select(self._readers, self._writers, [], timeout)
    except InterruptedError:
        return ready
    r = set(r)
    w = set(w)
    for fd in r | w:
        events = 0
        if fd in r:
            events |= EVENT_READ
        if fd in w:
            events |= EVENT_WRITE

        key = self._key_from_fd(fd)
        if key:
            ready.append((key, events & key.events))
    return key
```

这段代码描述了用户向`OS`发起的查询逻辑. `select`函数的`timeout`参数默认是`None`,这意味着默认情况下,如果没有任何一个就绪事件的发生,`select`调用会被永远阻塞.

`select`函数调用底层`select/poll/epoll`接口, 此函数在`SelectSelector`类和`EpollSelector`类中的定义有所区别,会根据`OS`的类型调用对应接口,`windows`和`linux`实际调用的底层接口对比如下:

```python
用户统一调用高层select函数,此函数实际调用的接口为:

# windows下使用select(SelectSelector类)
r, w, _ = self._select(self._readers, self._writers, [], timeout)

# linux下使用epoll(EpollSelector类)
fd_event_list = self._epoll.poll(timeout, max_ev)
```

函数使用`ready`变量保存准备就绪的元祖`(key, events)`

在`windows`中,一旦底层`select`接口返回,会得到`3`个列表,前两个表示可读和可写的文件对象列表,并使用集合处理为唯一性.准备就绪的元祖对象会加入`ready`列表中返回.如果定义了`timeout`不为`None`,且发生了超时,会返回一个空列表.

## 4. 总结
1. 操作系统提供的`select/poll/epoll`接口可用于**编写事件循环**, 而`Selectors`模块封装了`select`模块, `select`模块是一个低级别的模块,封装了`select/poll/epoll/kqueue`等接口.
2. `selectors`模块中定义了有名元祖`selectorkey`, 此对象封装了文件对象/描述符值/事件/附带数据,`selectorkey`为我们**提供了回调的环境**
3. 使用`selectors`模块可以实现使用**回调模型**来完成高并发的方案.
4. **(非常重要)**异步回调模型,大部分事件和精力都是对回调函数的设计.**回调模型使得每一个涉及IO操作的地方都需要单独分割出来作为函数,这会分割代码导致可读性下降和维护难度的上升.**