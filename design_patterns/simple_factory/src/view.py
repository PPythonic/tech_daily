"""
计算器的界面模块
"""

def view():
    # 向用户获取操作符和两个数字
    print("welcome to factory calculator")
    x = input("please input a number: ")
    y = input("please input another number: ")
    o = input("please input operator: ")
    print(x, o, y)

    return x, y, o