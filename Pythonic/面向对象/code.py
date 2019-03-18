# from abc import ABCMeta, abstractmethod

# class File(object, metaclass=ABCMeta):
#     @abstractmethod
#     def read(self):
#         pass

# class Text(File):
#     def read(self):
#         print("reading Text")

# text1 = Text()
# text1.read()
# text2 = File() #TypeError: Can't instantiate abstract class File with abstract methods read
# text2.read()


# class Student:
#     def __init__(self, name, money):
#         self.name = name
#         self.__money = money  # 注意, 需要使用另一个属性名, 否则会无限递归

#     @property
#     def money(self):
#         print(f'这里控制{self.name}的money属性访问')
#         return self.__money

#     @money.setter
#     def money(self, new_money):
#         print(f'这里可以控制{self.name}的money属性设置')
#         self.__money = new_money

#     @money.deleter
#     def money(self):
#         print(f'这里可以控制{self.name}的money属性删除')
#         raise AttributeError('此属性不可删除')

# stu1 = Student('stu1', 88888)

# print(stu1.money) # 这里控制stu1的money属性访问 88888
# stu1.money = 188888 # 这里可以控制stu1的money属性设置
# del stu1.money # 这里可以控制stu1的money属性删除  AttributeError: 此属性不可删除


# class Student:
#     def __init__(self, name, money, password):
#         self.name = name
#         self.__money = money
#         self.__password = password

#     def show_money(self, password):
#         if password == self.__password:
#             return self.__get_money()
#         else:
#             print('refuse')
#             return None

#     def __get_money(self):
#         return self.__money

# stu1 = Student('stu1', 88888, '123')
# print(stu1.show_money('123'))
# print(stu1.show_money('abc'))

# code = """
# a = 2
# global b
# b = 3

# def show():
#     print('hello')
# """

# g_dic = {}
# l_dic = {}

# exec(code, g_dic, l_dic)

# print(g_dic)
# print(l_dic)

# class MyMeta(type):
#     def __new__(cls, class_name, class_bases, class_dic):
#         print('元类, cls is', cls.__name__)
#         print('现在准备创建类对象', class_name)
#         return super().__new__(cls, class_name, class_bases, class_dic)

#     def __init__(self, class_name, class_bases, class_dic):
#         print('选择要对类对象初始化', self.__name__)
#         self.class_name = class_name
#         self.class_bases = class_bases
#         self.class_dic = class_dic

#         self.a = 2

# class Student(object, metaclass=MyMeta):
#     pass

# print(Student.a)

# class MyMeta(type):
#     def __call__(self, *args, **kwargs):
#         print('此类正在执行call', self.__name__)

#         obj = object.__new__(self)
#         self.__init__(obj, *args, **kwargs)
#         return obj

# class Student(object, metaclass=MyMeta):
#     pass

# stu1 = Student()

# print(stu1)

# class Student:
#     __instance = None

#     def __new__(cls, *args, **kwargs):
#         if cls.__instance is None:
#             obj = object.__new__(cls)  # 返回一个空对象
#             cls.__init__(obj, *args, **kwargs)
#             cls.__instance = obj

#         return cls.__instance

# stu1 = Student()
# stu2 = Student()
# print(stu1 is stu2)

# class Animal:
#     def f(self):
#         print("这是Animal")
#         print('self 是', self)

# class People(Animal):
#     def f(self):
#         print('这是People')
#         super().f()

# class Student(People):
#     def f(self):
#         print('这是Student')
#         super().f()

# stu1 = Student()
# print(stu1)
# stu1.f()       

# class Student:
#     def eat(self):
#         print('eating')

# stu1 = Student()
# stu2 = Student()

# print(stu1.eat)
# print(stu2.eat)

# class Student:
#     def eat(self):
#         print('eating')

# stu1 = Student()
# print(stu1)
# bound_func = stu1.eat
# print(bound_func.__self__)
# print(bound_func.__func__)


# class Wrapper:
#     def __init__(self, func):
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         print('start')
#         self.func()
#         print('end')

# @Wrapper
# def show():
#     print('这是show函数')

# show()

class Wrapper:
    def __init__(self, key):
        self.key = key

    def __call__(self, func):
        self.func = func

        def inner(*args, **kw):
            print('start')
            self.func(*args, **kw)
            print('end')
        return inner

@Wrapper('key')
def show():
    print('这里是show函数')

show()