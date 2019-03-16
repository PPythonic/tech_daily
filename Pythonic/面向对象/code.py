from abc import ABCMeta, abstractmethod

class File(object, metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

class Text(File):
    def read(self):
        print("reading Text")

text1 = Text()
text1.read()
text2 = File() #TypeError: Can't instantiate abstract class File with abstract methods read
text2.read()