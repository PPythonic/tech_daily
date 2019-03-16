"""产品模块
产品划分多个抽象类, 每一个抽象类中有多个具体产品类
"""

from abc import ABCMeta, abstractmethod

# 产品类别1
class AbstractUser(object, metaclass=ABCMeta):
    pass

# 具体产品类1
class MysqlUser(AbstractUser):
    pass

# 具体产品类1
class RedisUser(AbstractUser):
    pass


# ===============================

# 产品类别2
class AbstractCourse(object, metaclass=ABCMeta):
    pass

# 具体产品类2
class MysqlCourse(AbstractCourse):
    pass

# 具体产品类2
class RedisCourse(AbstractCourse):
    pass

