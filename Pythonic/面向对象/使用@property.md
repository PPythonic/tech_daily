# 使用@property

再绑定属性时，如果我们直接把属性暴露出去，虽然写起来简单，但是没办法检查参数，导致可以把成绩随便更改：
```python
s = Student()
s.score = 9999
```
这显然不合逻辑。为了限制score的范围，可以通过一个set_score()的方法来设置成绩，在通过一个get_score()来获取成绩，这样，在set_score()方法里就可以检查参数
```python
class Student(object):
    def get_score(self):
        reture self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer')
        if value < 0 or value > 100:
            raise ValueError('score must be in 0~100')
        self._score = value
```
现在，对任意的Student实例进行操作，就不能随行所欲的设置score了
```python
s = Student()
s.set_score(99)
s.get_score()  # 99
s.set_score(999)
s.get_score() # ValueError: score must be in 0~100
```  
但是上面的调用方法又略显复杂，没有直接用属性那么直接简单
有没有既能检查参数，又可以用类似访问属性这样简单的方式来访问类的变量呢？对于追求完美的Python程序员，这是必须做到的！
还记得装饰器(decorator)可以给函数动态加上功能吗？对于类的方法，装饰器一样起作用，Python内置的`@property`装饰器就是负责把一个方法变成属性调用的
```python
class Student(object):

    @property
    def score(self):
        reture self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer')
        if value < 0 or value > 100:
            raise ValueError('score must be in 0~100')
        self._score = value
```
`@property`的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上`@property`就可以了，此时，`@property`本身又创建了另一个装饰器`@score.setter`，负责把一个setter方法变成属性赋值，于是，我们就有一个可控的属性操作
```python
s = Student()
s.score = 60 # 实际转化为s.set_score(60)
s.score # 实际转化为s.get_score()
```
注意到这个神奇的`@property`，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来是实现的
```python
class Student(object):

    @property
    def birth(self):
        return self._birth


    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2019 - self._birth
```
上面的birth是可读写属性，age是只读属性，因为age可以根据birth和当前时间推算出来。
## 小结
`@property`广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样程序运行时就减少了出错的可能性。