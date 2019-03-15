from src.view import view
from src.calculate import cal
"""
一个简单的计算器程序,
用户输入两个数字及一个操作符即可得到计算的结果.

源码机构划分为:
1. 计算器的界面模块
2. 计算器的计算模块
3. 计算器的操作符模块,此模块使用简单工厂模式设计
"""


def run():
    """计算器公共接口"""
    x, y, o = view()
    result = cal(x, y, o)
    print("The result is: ", result)

if __name__ == "__main__":
    run()
