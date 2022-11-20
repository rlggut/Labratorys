from abc import ABC, abstractmethod
from Tasks import *

class Variant():
    def __init__(self):
        self.n = 1
        self.task1=Task_t1()
        self.tasks=[self.task1]
    def getQuestion(self,num):
        if(num>self.n)or(num<=0):
            return
        return self.tasks[num-1].getQuestion()
    def getAnswer(self,num):
        if(num>self.n)or(num<=0):
            return
        return self.tasks[num-1].getAnswer()
    def setVariantNum(self,num):
        for task in self.tasks:
            task.setVariant(num)
    def getTaskNumbers(self):
        return self.n