from abc import ABC, abstractmethod

class Task(ABC):
    def setVariant(self,num):
        self.num=num
    @abstractmethod
    def getText(self):
        pass
    @abstractmethod
    def getAnswer(self):
        pass

class Tasks():
    def __init__(self):
        self.n = 0
    def getTask(self,num):
        if(num>self.n):
            return
    def getTaskNumbers(self):
        return self.n