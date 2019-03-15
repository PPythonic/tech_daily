"""
计算器的计算模块
"""

from src.operators import operator_factory

def cal(x, y, o):
    """计算接口"""
    # 获取对应的操作符类
    operator = operator_factory(o, x, y) # 返回类的实例化对象
    # 计算并返回结果
    operator.cal()
    result = operator.result

    return result