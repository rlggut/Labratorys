from abc import ABC, abstractmethod
from Common import *

class Task(ABC):
    def __init__(self):
        self.num=0
        self._Base__createTask()
    @abstractmethod
    def _Base__createTask(self):
        pass
    def setVariant(self,num):
        self.num=num
        self._Base__createTask()
    def getQuestion(self):
        return self.question
    def getAnswer(self):
        return self.answ
class Task_t1(Task):
    def _Base__createTask(self):
        x = (self.num % 23) + 11
        x = x * x + 11
        x = (x % 31) + 17
        y = (self.num % 5) + 4
        self.question = 'Переведите число ' + str(x) + ' из десятичной в ' + str(y) + '-ричную'
        self.answ = from10(x, y)

