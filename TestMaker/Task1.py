from abc import ABC, abstractmethod
from Tasks import *

class Task_t1(Task):
    def _Base__createTask(self):
        x = (self.num % 23) + 11
        x = x * x + 11
        x = (x % 31) + 17
        y = (self.num % 5) + 4
        self.question = 'Переведите число ' + str(x) + ' из десятичной в ' + str(y) + '-ричную'
        self.answ = from10(x, y)

t1 = Task_t1()
t1.setVariant(9)
print(t1.question)
