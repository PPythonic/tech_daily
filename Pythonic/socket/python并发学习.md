# 1. 理解操作系统
操作系统`OS`统管了计算机的所有硬件, 并负责为应用程序分配和回收硬件资源

硬件资源总是有限的, 而应用程序对资源的欲望都是贪婪的

当多个应用程序发生资源争夺时, 操作系统`OS`负责出面调度, 保证多任务的资源分配以保证系统稳定执行

只有`CPU`可以执行代码, 所以在应用程序执行前必须申请到`CPU`资源, 同一时刻, 一个`CPU`只能执行一个任务代码

计算机的`CPU`数量（资源方）远远小于需要执行的任务数（需求方），操作系统将`CPU`的资源按照时间片划分，并根据任务类型分配，各任务轮流使用`CPU`

`CPU`的执行/切换速度非常快，对于用户而言，多任务看上去就像同时执行一样，此称为并发

如下是串行和并发的对比：
![](https://images2018.cnblogs.com/blog/1381809/201807/1381809-20180726093031259-414917527.jpg)

---

计算机的内存、硬盘、网卡、屏幕、键盘等硬件提供了数据交换的场所

`OS`提供了`IO`接口以实现数据交换，数据交换的过程一般不需要`CPU`的参与

`IO`接口有两种类型:
- 阻塞型IO
    发生IO(数据交换)的时候, 调用线程无法向下执行剩余代码, 意图占用`CPU`但不执行任何代码, **单线程阻塞型IO自身无法支持并发**
- 非阻塞型IO
    发生IO(数据交换)的时候, 调用线程可以向下执行剩余代码, **单线程阻塞型IO自身可以支持并发**

如下是阻塞型IO和非阻塞型IO的对比：
![](https://images2018.cnblogs.com/blog/1381809/201807/1381809-20180726093045409-157802242.jpg)

# 二. 任务类型
根据一个任务执行期间占用`CPU`的比例来划分, 有两种类型:
- CPU密集型
    绝大部分时间都是占用CPU并执行代码, 比如科学计算任务
- IO密集型
    绝大部分时间都未占用`CPU`, 而是发生`IO`操作, 比如网络服务

# 三. socket模块
`OS`提供了阻塞和非阻塞两种类型的接口, 应用程序可以自行选择

`Socket`模块封装了两种接口, `Socket`模块提供的默认函数是阻塞IO型

用户可以选择手工切换至非阻塞IO类型，使用`socketobj.setblocking(False)`切换至非阻塞IO模式。
下面将通过一个简单的例子程序来记录对并发的学习思考及总结

# 四、一个简单的C/S程序
客户端：循环接收用户的输入，并发送给服务器。从服务器接收反馈并打印至屏幕。
服务器：将接收到的用户输入，变成大写并返回给客户端

客户端代码固定，主要思考服务器端的代码。
一般我们会这样写服务端代码：
```python
# 服务器端
import socket

addr = ('127.0.0.1', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen(5)
print('监听中...')

while True: # 链接循环
    conn, client = server.accept()
    print(f'一个客户端上线 -> {client}')

    while True:  # 消息循环
        try:
            request = conn.recv(1024)
            if not request:
                break
            print(f"request: {request.decode('utf-8')}")
            conn.send(request.upper())

        except ConnectionResetError as why:
            print(f"客户端丢失, 原因是{why}")
            break
    
conn.close()
```

客户端代码
```python
# 客户端
import socket

addr = ('127.0.0.1', 8080)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)
print(f"服务器{addr}链接成功")

while True:  # 消息循环
    letters = input(">>>").strip()
    if not letters: continue

    try:
        client.send(letters.encode('utf-8'))
        response = client.recv(1024)
        print(response.decode('utf-8'))
    except ConnectionResetError as why:
        print(f'服务端丢失，原因是: {why}')
        break

client.close()
```

这种形式的编码我称为**单线程+阻塞IO+循环串行**, 有如下几个特点: 
- 编码简单, 模式简洁, 可读性强
- 串行提供服务, 用户使用服务器必须一个一个排队

单一线程的阻塞IO模型是无法支持并发的, 如果要支持并发, 有如下两种解决方案:
- 多进程, 多线程
- 异步

# 五. 使用阻塞IO实现并发
单线程阻塞IO本质上是无法实现并发的. 因为一旦发生IO阻塞, 下方代码就不会继续执行. 如果使用单线程阻塞IO来实现并发, 需要增加线程数目或者进程数目, 当某一个线程/进程发生阻塞的时候, 由`OS`调度至另一个线程/进程执行.

---

## 方案一：阻塞IO+多进程
```python
# 服务器端
import socket
from multiprocessing import Process

def task(conn):
    """通信循环处理函数"""
    while True:
        try:
            request = conn.recv(1024)
            if not request:
                break
            print(f"request: {request.decode('utf-8')}")
            conn.send(request.upper())
        except ConnectionError as why:
            print(f'客户端丢失，原因是: {why}')
            break
        
if __name__ == "__main__":  # windows下需要把新建进程写到main中, 不然会报错
    addr = ('127.0.0.1', 8080)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    print('监听中...')

    while True:
        conn, client = server.accept()
        print(f'一个客户端上线 -> {client}')

        p = Process(target=task, args=(conn, ))  # 开启子进程处理与用户的消息循环
        p.start()
```
将服务器对用户的消息循环操作封装到进程中, **单进程依然会发生阻塞**

**进程之间的调度交由`OS`负责(重要)**

进程较重, 创建和销毁进程都需要比较大的开销, 此外, 一台设备所能涵盖的进程数是有限的(一般几百)

进程之间的切换开销也不小

当进程数小于`CPU`核心数的时候, 可以实现真正的并行, 当进程数大于`CPU`核心数的时候, 依然以并发执行

---


## 方案二: 阻塞IO+多线程
```python
import socket
from threading import Thread

def Task(conn):
    """通信循环处理函数"""
    while True:
        try:
            request = conn.recv(1024)
            if not request:
                break
            print(f"request: {request.decode('utf-8')}")
            conn.send(request.upper())
        except ConnectionError as why:
            print(f'客户端丢失，原因是: {why}')
            break

if __name__ == "__main__":
    addr = ('127.0.0.1', 8080)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    print('监听中...')

    while True:
        conn, client = server.accept()
        print(f'一个客户端上线 -> {client}')

        t = Thread(target=task, args=(conn,))  # 启动多线程处理与用户的消息循环
        t.start()
```
将服务器对用户的操作封装到线程中, **单线程中依然会发生IO阻塞**

**线程之间的调度交由OS负责（重要）。**

线程较轻，创建和销毁的开销都比较小，但是线程数量也不会太大，一台设备一般能容纳几百至上千的线程。

**注意：因为CPython的GIL的存在，使用CPython编写的多线程代码，只能使用一个CPU核心，换句话说，使用官方的解释器执行Python多线程代码，无法并行(单进程中）。**

线程之间的切换开销比较小。

实际上，多线程的最大问题并不是并发数太少，而是数据安全问题

线程之间共享同一进程的数据，在频繁发生IO操作的过程中，难免需要修改共享数据，这就需要增加额外的处理，当线程数量大量增加时，如何妥善处理数据安全的问题就会变成主要困难

---

## 阻塞IO模型的思考和总结

- 多线程和多进程都是基于阻塞IO模式提供的并发，两者编程模型比较简单，可读性也很高
- 如果使用多线程/进程的方案来提供并发，当线程/进程数量不断增大时，系统稳定性将会下降。虽然可以使用线程/进程池来提供一定的优化，但超过一定数量之后，池子发挥的效果也会越来越小。所以，两者都无法支持超大规模的并发（如C10M及以上)
- **线程/进程切换都交由`OS`调度，调度策略依据`OS`的算法，应用程序无法主动控制，无法针对任务的特性做一些必要的调度算法调整**
- 编码思维直接、易理解，学习曲线平缓
- 多线程/进程的方案可以理解为单纯的增加资源，如果要想支持超大规模的并发，单纯的增加资源的行为并不合理
- 另一种解决方案的核心思路就是: **改变IO模型**

# 六. 使用非阻塞IO实现并发
非阻塞IO的核心是: 调用线程一旦向`OS`发起IO调用, `OS`就直接返回结果, 因此, 调用线程不会被阻塞而可以执行下面要执行的代码. 不过也因为不会被阻塞, 调用线程就无法判断立即返回的结果是不是期望结果. 所以调用线程需要增加额外的操作对返回结果进行判断, 正因为这一点, 就增加了编程难度(增加的难度可不是一点啊)

对立即返回的结果进行判断的方案有两种:
1. 轮询: 线程定期或者不定期的主动发起查询和判断
2. 回调函数+事件循环:  线程在发起IO时注册回调函数, 然后统一处理事件循环

---

## 方案一：非阻塞IO+Try+轮询
```python
服务器端代码
import socket

addr = ('127.0.0.1', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.setblocking(False)
server.listen(5)
print('监听中...')

# 需要执行接收的conn对象放入此列表
recv_list = []

# 需要发送数据的conn对象和数据放入此列表
send_list = []

# 执行链接循环
while True:
    try:
        conn, list = server.accept()
        # 执行成功, 说明返回值是conn, client
        print(f'一个客户端上线 -> {client}')
        # 将成功链接的conn放入列表, 当accept发生错误时执行conn的消息接收操作
        recv_list.append(conn)
    
    except BlockingIOError:
        # 执行accept不成功, 意味着当前未有任何链接
        # 在下一次执行accept之前, 可以执行其他的任务(消息接收操作)

        # 无法对处于遍历期间的接收列表执行remove操作, 使用临时列表存储需要删除的conn对象
        del_recv_list = []

        # 对已经成功链接的conn列表执行接收操作
        for conn in recv_list:
            try:
                request = conn.recv(1024)  # recv也是非阻塞
                if not request:
                    # 当前的conn链接已经失效
                    conn.close()
                    # 不再接收此conn链接的消息，将失效conn加入删除列表
                    del_recv_list.append(conn)
                    # 当前conn处理完毕，切换下一个
                    continue
                response = request.upper()
                # 发送列表需要存放元组，发送conn和发送的数据
                send_list.append((conn, response))
            except BlockingIOError:
                # 当前conn的数据还没准备好, 处理下一个conn
                continue
            except ConnectionResetError:
                # 当前conn失效,不再接收此conn消息
                conn.close()
                del_recv_list.append(conn)

        # 无法处理发送列表遍历期间的remove，使用临时列表
        del_send_list = []

        # 接收列表全部处理完毕, 准备处理发送列表
        for item in send_list:
            conn = item[0]
            response = item[1]

            # 执行发送
            try:
                conn.send(response)
                # 发送成功, 从发送列表中删除此项目
                del_send_list.append(item)
            except BlockingIOError:
                # 发送缓冲区有可能已经满了, 留待下次发送处理
                continue
            except ConnectionResetError:
                # 链接失效
                conn.close()
                del_recv_list.append(conn)
                del_send_list.append(item)

        # 删除接收列表中已经失效的conn对象
        for conn in del_recv_list:
            recv_list.remove(conn)

        # 删除发送列表中已经发送或者不需要发送的对象
        for item in del_send_list:
            send_list.remove(item)
```
**服务器使用单线程实现了并发**
对于`accept`接收到的多个`conn`对象, 加入列表, 并通过遍历读取列表, 发送列表来提供多用户访问

单线程中的`Socket`模块提供的`IO`函数都被设置成：非阻塞IO类型

增加了额外操作：对非阻塞调用立即返回的结果，使用了`Try`来判断是否为期望值

因为不知道何时返回的结果是期望值，所以需要不停的发起调用，并通过`Try`来判断，即，**轮询**

两次轮询期间，线程可以执行其他任务。但是模型中也只是不停的发起轮询，并没有利用好这些时间

优化：此模型中的主动轮询的工作由程序负责，其实可以交由`OS`代为操作。这样的话，应用程序就不需要编写轮询的部分，可以更聚焦于业务逻辑(`upper()`的部分)，`Python`提供了`Select`模块以处理应用程序的轮询工作

---

## 方案二. 非阻塞IO+ Select代理轮询
```python
# 服务器端代码
import socket
import select

addr = ('127.0.0.1', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.setblocking(False)
server.listen(5)
print('监听中...')

# 最开始的server对象需要被监听, 一旦可读, 说明可以执行accept
read_list = [server, ]

# 需要监听的写列表，一旦wl中可写对象处理完send，应该将它也从此列表中删除
write_list = []

# 用于临时存放某一个sock对象需要发送的数据
data_dic = {}

# 不停的发起select查询
while True:
    # 发起select查询, 尝试得到可以操作的socket对象
    rl, wl, xl = select.select(read_list, write_list, [], 1)
    # 操作可读列表
    for sock in rl:
        # 如果可读列表中的对象是server, 意味着有链接, 则server可执行accept
        if sock is server:
            # 执行accept一定不会报错, 所以不需要try
            conn, client = sock.accept()
            # 一旦获得conn，就需要将此conn加入可读列表
            read_list.append(conn)
        else:
            # 说明可读的对象是普通的conn对象,执行recv时要处理链接失效问题
            try:
                request = sock.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                # 此链接失效
                sock.close()
                read_list.remove(sock)
        else:
                # 还需要继续判断request的内容
                if not request:
                    # 说明此conn链接失效
                    sock.close()
                    # 不再监控此conn
                    read_list.remove(sock)
                    continue
                # 处理请求
                response = request.upper()
                # 加入发送列表
                write_list.append(sock)
                # 保存发送的数据
                data_dic[sock] = response

    # 操作可写列表
    for sock in wl:
        # 执行发送操作，send也会出错
        try:
            sock.send(data_dic[sock])
            # 发送完毕后，需要移除发送列表
            write_list.remove(sock)
            # 需要移除发送数据
            data_dic.pop(sock)

        except (ConnectionResetError, ConnectionAbortedError):
            # 此链接失效
            sock.close()
            read_list.remove(sock)
            write_list.remove(sock)
```

使用了`Select`模块之后, 应用程序不再需要编写主动轮询的代码, 而是将此部分工作交由`Select`模块的`select`函数代为处理

应用程序只需要遍历`select`函数返回的可操作`socket`列表, 并处理相关业务逻辑即可

虽然应用程序将轮询工作甩给了`select`, 自己不用编写代码. 不过`select`函数的底层接口效率不高, 使用`epoll`接口可以提升效率, 此接口被封装在`Selectors`模块中

此外,**`select`函数是一个阻塞IO**, 在并发数很少的时候, 线程大部分时间会阻塞在`select`函数上. **所以`select`函数应该适用于随时随刻都有`socket`准备好、大规模并发的场景**