from abc import ABC, abstractmethod
from Common import *
import random
import re
class Task(ABC):
    def __init__(self):
        self.num=0
        self._Base__createTask()
        self.lang="Ru"
        self.question = "Que?"
        self.questionE = "Que?"
        self.answ = "!"
        #0-without add material, 1- table, 2- pic
        self.flags=0
        self.table=[]
        self.tableN=0
        self.tableM=0
    @abstractmethod
    def _Base__createTask(self):
        pass

    def setLang(self, lg):
        self.lang = lg
    def getLang(self):
        return self.lang
    def setVariant(self,num):
        self.num=num
        self._Base__createTask()
    def getQuestion(self):
        if(self.lang=="Ru"):
            return self.question
        else:
            return self.questionE
    def getAnswer(self):
        return self.answ
    def getTable(self):
        if (self.flags & 0x01 > 0):
            return self.table
        else:
            return
    def getTableN(self):
        return self.tableN
    def getTableM(self):
        return self.tableM
    def getFlags(self):
        return self.flags

class Task_t1_1(Task):
    def _Base__createTask(self):
        x = (self.num % 23) + 11
        x = x * x + 11
        x = (x % 31) + 17
        y = (self.num % 5) + 4
        self.question = 'Переведите число ' + str(x) + ' из десятичной в ' + str(y) + '-ричную'
        self.questionE = 'Translate number ' + str(x) + ' from decimal to ' + str(y) + 'th'
        self.answ = from10(x, y)

class Task_t1_2(Task):
    def _Base__createTask(self):
        x=(self.num % 31)+7
        x=x * x +13
        x=(x % 43) +19
        y=(self.num % 7)+3
        self.question='Переведите число '+from10(x,y)+' из '+ str(y)+'-ричной в десятичную'
        self.questionE='Translate the number '+from10(x,y)+' from '+ str(y)+'th to decimal'
        self.answ=str(x)
class Task_t2_1(Task):
    def _Base__createTask(self):
        y1 =self.num % 31
        y1 =(y1+3)*(y1+5)*(y1+7)
        y1 =(y1 % 4)+2
        if(y1==2):
            y2=(self.num % 3)+2
        else:
            if(y1==3):
                y2=(self.num % 2)+2
            else:
                y2=2
        x=(self.num % 47)+13
        x=(x+13)*(x // 4)
        if(x<400):
            x=(x % 641)
        else:
            x=x-239
        self.question='Переведите число '+from10(x,y1)+' из '+ str(y1)+'-ричной в '+str((pow(y1,y2)))
        self.questionE = 'Translate number ' + from10(x, y1) + ' from ' + str(y1) + 'th to ' + str((pow(y1, y2)))
        self.answ=from10(x,(pow(y1,y2)))

class Task_t2_2(Task):
    def _Base__createTask(self):
        y1 = (self.num % 43) + 17
        y1 = y1 * y1
        y1 = (y1 % 7) + 2
        y2 = (self.num % 2) + 2
        if (y1 > 5) and (y2==3):
            y2 = 2
        x = (self.num % 101) + 17
        x = x * x
        x = (x % 119) + (self.num % 7) + 3;
        self.question = 'Переведите число ' + from10(x, pow(y1, y2)) + ' из ' + str(pow(y1, y2)) + '-ричной в ' + str(y1)
        self.questionE = 'Translate number ' + from10(x, pow(y1, y2)) + ' from ' + str(pow(y1, y2)) + 'th to ' + str(y1)
        self.answ = from10(x, y1);

class Task_t3(Task):
    def _Base__createTask(self):
        base=["A","0","!A","1","!B","A & B","!A & B","A & !B","!A & !B","A || B","!A || B","A || !B","!A || !B"]
        dct={'A': "(A & (A || B))", 'B': "(B || (A & B))", "1": "(A || !A)", "0": "(B & !B)"}
        st=base[self.num % len(base)]
        self.answ = st
        iterations=(self.num*self.num)%3 + 3
        random.seed(self.num)
        for i in range(iterations):
            find=False
            dctKey=""
            while not find:
                dctPoint=random.randint(0,len(dct)-1)
                for var in dct:
                    if(dctPoint==0):
                        dctKey=var
                        break
                    dctPoint-=1
                rt=re.search(dctKey, st)
                if(rt != None):
                    find=True
            st=st.replace(dctKey,dct.get(dctKey),1)
        self.question = "Сократите выражение: "+st
        self.questionE = "Shorten the expression: "+st

def wayPoint(tbl, size):
    ways=[]
    posWays=[]
    for i in range(size):
        posWays.append(-1)
        ways.append(-1)
    ways[0]=0
    posWays[0]=0
    find=True
    y=0
    while(find):
        for x in range(size):
            if(ways[x]==-1)and(tbl[y][x]>0)and((ways[y]+tbl[y][x]<posWays[x])or(posWays[x]==-1)):
                posWays[x]=ways[y]+tbl[x][y]
        mxInd=-1
        mx=-1
        find=False
        for i in range(size):
            if((posWays[i]>=0)and(ways[i]==-1)):
                find=True
                if(mxInd==-1)or(mx>posWays[i]):
                    mx=posWays[i]
                    mxInd=i
        if(find):
            ways[mxInd]=mx
            y=mxInd
    return(ways[size-1])

class Task_t4(Task):
    def _Base__createTask(self):
        self.answ = 0
        size = ((self.num % 7) + 11)// 2
        self.question = "Найдите кратчайший путь из вершины A в вершину "+chr(size+ord('A')-1)
        self.questionE = "Find the shortest path from vertex A to vertex "+chr(size+ord('A')-1)
        tp = (self.num % 101) + 87
        self.flags = 1
        self.tableN = size+1
        self.tableM = size+1
        tbl=[]
        for i in range(size):
            tbl.append([])
            for j in range(size):
                tbl[i].append(0)
        i = 0
        while (wayPoint(tbl, size)==-1) or (i < (3 * size)):
            x = (tp + ((self.num * i)% 5) + random.randint(0,size)) %  size
            y = (tp + ((self.num * i)% 7) + random.randint(0,size))% size
            if (x==y):
                y = (y+1)%size
            dl = (tp % 7) + (tp % 3) + 1
            if (((x + size - 2) % size > (size-4)) and (x==(size-1)) or ((x+size-2) % size > (size-4))
                and (y==(size-1))) and (dl < 7):
                dl = dl + 7
            if (dl==0):
                dl = 1
            tbl[x][y] = dl
            tbl[y][x] = dl
            tp = tp + 13
            if (wayPoint(tbl, size) != -1):
                i = i+1
        self.answ = str(wayPoint(tbl, size))

        self.table = []
        self.table.append([])
        self.table[0].append('')
        for i in range(size):
            self.table[0].append(chr(ord('A') + i))
        for y in range(size):
            self.table.append([])
            self.table[y+1].append(chr(ord('A')+y))
            for x in range(size):
                if(tbl[x][y]>0):
                    self.table[y+1].append(str(tbl[x][y]))
                else:
                    self.table[y+1].append('')