"""个人简历对象的复制程序
通过copy而不是多次实例化操作来获得同一个对象的多个副本
"""

from copy import copy, deepcopy

# 原型接口类, 提供clone克隆方法
class PrototypeInterface(object):
    def clone(self):
        raise NotImplementedError('方法必须被实现')


class Profile(PrototypeInterface):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def clone(self):
        """如果只需要对象的属性值,则使用copy即可
        若需要对象所有深层引用的其他对象, 则需要使用deepcopy
        """
        return deepcopy(self)
    
    def show(self):
        print('个人简历信息')
        print(str(self.__dict__))


if __name__ == "__main__":
    profile = Profile('wjn', 26, 'man')

    # 要20份个人档案
    profile_list = list()
    for i in range(20):
        # 使用克隆(复制)来实现20份档案, 而不是实例化20次
        profile_list.append(profile.clone())

    # 结果是20份内存地址互不相同的profile对象
    print(profile_list)

    
