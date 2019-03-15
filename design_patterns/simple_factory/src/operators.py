"""
计算器的操作符模块
"""

operator_map = dict()

class AutoMappingMeta(type):
    """自动映射元类"""
    def __new__(cls, classname, classbases, class_dict):
        new_cls = super().__new__(cls, classname, classbases, class_dict)

        if new_cls.__name__ != 'BaseOperator':
            if not hasattr(new_cls, 'name'):
                raise RuntimeError('所有子类必须定义name属性')
            print("hereeeee")
            operator_map[getattr(new_cls, 'name')] = new_cls

        return new_cls

def operator_factory(char, *args, **kwargs):
    """
    简单工厂函数,根据用户提供的输入,
    选择对应的类并返回一个实例化对象
    """
    print(operator_map)
    cls = operator_map.get(char)
    print("-----", cls)
    return cls(*args, **kwargs)


# 定义一个基类或者抽象类来统一控制所有子类
class BaseOperator(object, metaclass=AutoMappingMeta):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.result = None

    def cal(self):
        raise NotImplementedError('必须实现此方法')


class Add(BaseOperator):
    name = "+"

    def cal(self):
        self.result = self.x + self.y

class Sub(BaseOperator):
    name = '-'

    def cal(self):
        self.result = self.x - self.y

class Multi(BaseOperator):
    name = '*'

    def cal(self):
        self.result = self.x * self.y

class Div(BaseOperator):
    name = '/'

    def cal(self):
        self.result = self.x / self.y