### 1. `__new__`和`__init__`
`__new__`方法是真正的类构造方法, 用于产生实例化对象(空属性). 重写`__new__`方法可以控制对象的产生过程.
`__init__`方法是初始化方法, 负责对实例化对象进行属性值初始化, 此方法必须返回None, `__new__`方法必须返回一个对象. 重写`__init__`方法可以控制对象的初始化过程.
```python
# 使用__new__来处理单例模式

class Student:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__new__ is None:
            obj = object.__new__(cls)
            cls.__init__(obj, *args, **kwargs)
            cls.__instance = obj

        return cls.__instance

stu1 = Student()
stu2 = Student()
print(stu1 is stu2)  # True
```
个人感觉, `__new__`一般很少用于普通的业务场景, 更多的用于元类之中, 因为可以更底层的处理对象的产生过程. 而`__init__`的使用场景更多

### 2. `__str__`, `__repr__`
两者的目的都是为了显式的显示对象的一些必要信息, 方便查看和调试, `__str__`被`print`默认调用, `__repr__`被控制台输出时默认调用, 即, 使用`__str__`控制用户展示, `__repr__`控制调试展示
```python
# 默认所有类继承object类, object类应该有一个默认的str和repr方法, 打印的是对象的来源以及对应的内存地址

class Student:
    def __init__(self, name, age):
        self.name = name
        self. age = age

stu = Student('foo', 26)  # <__main__.Student object at 0x00000230CFF0B4E0>
print(stu)
```
```python
# 自定义str来控制print的显示内容, str函数必须return一个字符串对象
# 使用repr = str来使控制台和print显示一致

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'{self.__class__}, {self.name}, {self.age}'

    __repr__ = __str__

stu = Student()
print(stu)  # <class '__main__.Student'>, foo, 26
```

### 3. `__call__`
`__call__`方法提供给对象可以被执行的能力, 就像函数那样, 而本质上, 函数就是对象, 函数就是一个拥有`__call__`方法的对象. 拥有`__call__`方法的对象, 使用`callable`可以得到`True`的结果, 可以使用`()`执行, 执行时可以传入参数, 也可以返回值. 所以我们可以使用`__call__`方法来实现实例化对象作为装饰器.
```python
# 检查一个函数的输入参数个数, 如果调用此函数时提供的参数个数不符合预定义, 则无法调用
# 单纯函数版本装饰器
def args_num_require(require_num):
    def outer(func):
        def inner(*args, **kwargs):
            if len(args) != require_num:
                print('函数参数个数不符合预定义，无法执行函数')
                return None
            
            return func(*args, **kwargs)
        return inner
    return outer

@args_num_require(2)
def show(*args):
    print('show函数成功执行')

show(1)  # 函数参数个数不符合预定义，无法执行函数
show(1,2)  # show函数成功执行
show(1,2,3)  # 函数参数个数不符合预定义，无法执行函数
```

```python

# 检查一个函数的输入参数个数,
# 如果调用此函数时提供的参数个数不符合预定义，则无法调用。

# 实例对象版本装饰器
class Checker:
    def __init__(self, require_num):
        self.require_num = require_num

    def __call__(self, func):
        self.func = func

        def inner(*args, **kwargs):
            if len(*args) != self.require_num:
                print('函数参数个数不符合预定义，无法执行函数')
                return None
            
            return self.func(*args, **kwargs)
        return inner

@Checker(2)
def show(*args):
    print('show函数成功执行')

show(1)  # 函数参数个数不符合预定义，无法执行函数
show(1,2) # show函数成功执行
show(1,2,3)  # 函数参数个数不符合预定义，无法执行函数
```

### 4、del
`__del__`用于当对象的引用计数为0时自动调用。
`__del__`一般出现在两个地方：1、手工使用del减少对象引用计数至0，被垃圾回收处理时调用。2、程序结束时调用。
`__del__`一般用于需要声明在对象被删除前需要处理的资源回收操作

```python
# 手工调用del, 可以将对象引用计数减一, 如果减到0, 将会触发垃圾回收

class Student:

    def __del__(self):
        print("调用对象的del方法, 此方法将会回收对象内存地址")

stu = Student() # 调用对象的__del__方法回收此对象内存地址

del stu

print('下面还有程序其他代码')
```

```python
class Student:

    def __del__(self):
        print('调用对象的del方法，此方法将会回收此对象内存地址')

stu = Student()  # 程序直接结束，也会调用对象的__del__方法回收地址
```

### 5. `__iter__`, `__next__`
这两个方法用于将一个对象模拟成**序列**. 内置类型如列表, 元组都可以被迭代, 文件对象也可以被迭代获取每一行的内容. 重写这两个方法就可以是实现自定义的迭代对象

```python
# 定义一个指定范围内的自然数类, 并可以提供迭代

class Num:
    def __init__(self, max_num):
        self.max_num = max_num
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_num:
            self.count += 1
            return self.count
        else:
            raise StopIteration('已经到达临界')

num = Num(20)
for i in num:
    print('count: ', num.count)
    print(i)
```