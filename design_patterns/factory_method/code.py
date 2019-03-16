"""
一个简单的计算器程序,用户给定两个数字,
并指定计算的工厂类, 由此工厂类生成操作符对象并执行计算
"""

from src.factorys import ( # 用户自行选择的工厂类
    AddFactory,
    SubFactory,
    MultiFactory,
    DivFactory,
)

if __name__ == "__main__":
    x = 22
    y = 33
    add_factory = AddFactory()
    add = add_factory.create_opetator(x, y)
    print(add.handle())

    sub_factory = SubFactory()
    sub = sub_factory.create_opetator(y, x)
    print(sub.handle())