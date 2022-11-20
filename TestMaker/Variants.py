from abc import ABC, abstractmethod
from Tasks import *

class Variant():
    def __init__(self):
        self.n = 4
        self.task1_1=Task_t1_1()
        self.task1_2=Task_t1_2()
        self.task2_1=Task_t2_1()
        self.task2_2=Task_t2_2()
        self.tasks=[self.task1_1,self.task1_2,self.task2_1,self.task2_2]
    def getQuestions(self):
        st=""
        for i in range(self.num):
            st=st+self.tasks[i].getQuestion()+"\n"
        return(st)
    def getAnswers(self):
        st=""
        for i in range(self.num):
            st=st+self.tasks[i].getAnswer()+"\n"
        return(st)
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