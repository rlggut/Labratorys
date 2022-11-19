from abc import ABC, abstractmethod


def from10(n,deg):
    rs=""
    while(n>0):
        t=(n % deg)
        if(t>=10):
            rs=chr(ord('A')+t-10)+rs
        else:
            rs=chr(ord('0')+t)+rs
        n=n//deg
    return(rs)
def to10(st,deg):
    rs=0
    for i in (range(len(st))):
        rs=rs*deg
        print(rs,' ',st[i])
        if (ord(st[i])-ord('0')<=9):
            rs=rs+(ord(st[i])-ord('0'))
        else:
            rs=rs+(ord(st[i])-ord('A'))+10
    return(rs)

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
    def getText(self):
        return self.question
    def getAnswer(self):
        return self.answ

class Variant():
    def __init__(self):
        self.n = 0
    def getTask(self,num):
        if(num>self.n):
            return
    def getTaskNumbers(self):
        return self.n