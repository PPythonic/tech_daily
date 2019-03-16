"""操作符模块"""
from abc import ABCMeta, abstractmethod

class AbstractOperator(object, metaclass=ABCMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def handle(self):
        pass

class Add(AbstractOperator):
    def handle(self):
        return self.x + self.y

class Sub(AbstractOperator):
    def handle(self):
        return self.x - self.y

class Multi(AbstractOperator):
    def handle(self):
        return self.x * self.y

class Div(AbstractOperator):
    def handle(self):
        return self.x / self.y
