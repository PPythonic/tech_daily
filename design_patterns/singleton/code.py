"""
一个简单的单例模式的实现程序,
不论对业务实例化多少次,均只有一个全局唯一的实例化对象,且初始化也只执行一次
"""

# 全局对象引用
# class Foo(object):
#     def __init__(self, name):
#         self.name = name

# global_foo = Foo("test1")

# if __name__ == "__main__":
#     print(global_foo is global_foo)  # True 如果可以严格控制实例化的引用就能模拟单例
#     print(global_foo is Foo("test2")) # False 但是无法严格控制类的实例化过程


# 重写业务类构造方法
# class Foo(object):
#     _singleton = False

#     def __new__(cls, *args, **kwargs): # 重写业务类的构造函数实现实现控制实例化过程
#         if not hasattr(cls, '_singleton'):
#             instance = super().__new__(cls)
#             setattr(cls, '_singleton', instance)
#         return getattr(cls, '_singleton')
    
#     def __init__(self, name):
#         self.name = name

# if __name__ == "__main__":
#     print(Foo("test1") is Foo("test1")) # True 无论如何执行实例化都只会在第一次触发实例化过程
#     print(Foo("test1") is Foo("test2")) # True 无法控制初始化过程,依然可以执行多次


# 重写元类__call__方法,控制实例化和初始化只执行一次
class MyMetaclass(type):
    def __call__(self, *args, **kwargs): # 重写元类__call__方法
        if not hasattr(self, '_singleton'):
            instance = object.__new__(self) # 控制实例化过程
            self.__init__(instance, *args, **kwargs) # 控制初始化过程
            setattr(self, '_singleton', instance)
        
        # 返回实例化对象
        instance = getattr(self, '_singleton')
        return instance
    
class Foo(object, metaclass=MyMetaclass):
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    t1 = Foo("test1")
    t2 = Foo("test2")
    t3 = Foo("test3")

    print(t1 is t2 is t3)
    print(t3.name)