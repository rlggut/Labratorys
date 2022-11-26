from abc import ABC, abstractmethod
from Tasks import *

class Variant():
    def __init__(self):
        self.n = 4
        self.categories=["Number systems, direct translation", "Number systems, intersystem translation","Logical expressions"]
        self.categoriesRus=["Системы счисления, прямой перевод", "Системы счисления, межсистемный перевод","Логические высказывания"]
        self.task1_1=Task_t1_1()
        self.task1_2=Task_t1_2()
        self.task2_1=Task_t2_1()
        self.task2_2=Task_t2_2()
        self.task3=Task_t3()
        self.taskCat=[[self.task1_1,self.task1_2],[self.task2_1,self.task2_2],[self.task3]]
    def getAllCategoriesName(self):
        return self.categories
    def getAllCategoriesNameRus(self):
        return self.categoriesRus
    def setVariantLang(self,lang):
        for tsk in self.taskCat:
            for task in tsk:
                task.setLang(lang)
    def getAllCategoriesQuestions(self):
        st = ""
        number = 1
        for tsk in self.taskCat:
            num=self.n%len(tsk)
            st = st + '№' + str(number) + '. ' + tsk[num].getQuestion() + "\n"
            number += 1
        return (st)
    def getAllCategoriesAnswers(self):
        st = ""
        number = 1
        for tsk in self.taskCat:
            num=self.n%len(tsk)
            st = st + '№' + str(number) + '. ' + tsk[num].getAnswer() + "\n"
            number += 1
        return (st)
    def getAllQuestions(self):
        st=""
        number=1
        for tsk in self.taskCat:
            for task in tsk:
                st=st+'№'+str(number)+'. '+task.getQuestion()+"\n"
                number+=1
        return(st)
    def getAllAnswers(self):
        st=""
        number=1
        for tsk in self.taskCat:
            for task in tsk:
                st=st+'№'+str(number)+'. '+task.getAnswer()+"\n"
                number+=1
        return(st)
    def getQuestion(self, cat=1, num=1):
        if(cat>len(self.taskCat))or(cat<=0):
            return
        if(num>len(self.taskCat[cat-1]))or(num<=0):
            return
        return self.taskCat[cat-1][num-1].getQuestion()
    def getAnswer(self, cat=1, num=1):
        if(cat>len(self.taskCat))or(cat<=0):
            return
        if(num>len(self.taskCat[cat-1]))or(num<=0):
            return
        return self.taskCat[cat-1][num-1].getAnswer()
    def setVariantNum(self,num=1):
        for tsk in self.taskCat:
            for task in tsk:
                task.setVariant(num)
    def getTaskNumbers(self):
        return self.n
    def getCatNumbers(self):
        return len(self.categories)
    def getNumbersInCat(self, num):
        if(num>len(self.categories))or(num<=0):
            return 0
        else:
            return len(self.categories[num-1])
