from abc import ABC, abstractmethod
from Common import *
import random
import re
import math
from PIL import Image, ImageDraw
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
    def getPic(self):
        if (self.flags & 0x02 > 0):
            return self.canvas
        else:
            return
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

class Task_t5(Task):
    def _Base__createTask(self):
        dx=80
        nums=(self.num%7)+11
        points=[]
        means=[]
        for i in range(nums):
            points.append([])
            points[i].append(0)
            points[i].append(0)
            means.append(0)
        means[0]=1
        self.question='Сколькими способами можно пройти из вершины "A" в вершину "'+chr(ord('A')+nums-1)+'"'
        tiers=0
        if ((nums-2)% 3!=0):
            tiers=((nums-2)//3)+3
        else:
            tiers=((nums-2)//3)+2
        places=[]
        connected=[]
        for i in range(tiers):
            places.append([])
            connected.append([])
            for j in range(3):
                places[i].append(-1)
                connected[i].append(False)
        places[0][0]=-1
        places[0][1]=0
        places[0][2]=-1
        places[tiers-1][0]=-1
        places[tiers-1][1]=nums-1
        places[tiers-1][2]=-1

        self.canvas = Image.new("RGBA", (tiers*dx,150), (255,255,255,255))
        draw = ImageDraw.Draw(self.canvas)
        points[0][0]=15
        points[0][1]=90
        points[nums-1][0]=(dx//2)+(tiers-1)*dx
        points[nums-1][1]=90

        i=1;
        tp=1;
        while((nums-1)>i):
            if((nums-1-i)>=3):
                points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*tp
                points[i][1]=random.randint(7,23)
                places[tp][0]=i
                i=i+1
                points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*tp
                points[i][1]=random.randint(7,23)+50
                places[tp][1]=i
                i=i+1
                points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*tp
                points[i][1]=random.randint(7,23)+90
                places[tp][2]=i
                i=i+1
                tp=tp+1
            else:
                if((nums-1-i)==2):
                    points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*tp
                    points[i][1]=random.randint(7,23)
                    places[tp][0]=i
                    i=i+1
                    points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*tp
                    points[i][1]=random.randint(7,23)+90
                    places[tp][2]=i
                    i=i+1
                    places[tp][1]=-1
                    tp=tp+1
                else:
                    points[i][0]=random.randint(dx//4,(3*dx)//4)+dx*(tiers-2)
                    points[i][1]=random.randint(-7,23)+50
                    i=i+1
                    places[tiers-2][0]=-1
                    places[tiers-2][1]=i-1
                    places[tiers-2][2]=-1
        for i in range(nums):
            draw.ellipse((points[i][0]-3,points[i][1]-3,points[i][0]+3,points[i][1]+3), outline="black")
            draw.text((points[i][0]-5,points[i][1]+6),text=str(chr(ord('A')+i)),fill='black')
        connected[0][1]=True
        for i in range(tiers-1):
            for j in range(2):
                if(places[i][j]!=-1):
                    if(not connected[i][j]):
                        lines=0
                        if(j>0):
                            if(places[i][j-1]!=-1):
                                lines=lines+1
                                means[places[i][j]]=means[places[i][j-1]]
                                connected[i][j]=True
                                x1=points[places[i][j-1]][0]
                                y1=points[places[i][j-1]][1]
                                x2=points[places[i][j]][0]
                                y2=points[places[i][j]][1]
                                draw.line((x1,y1,x2,y2),fill='black')
                                x=x1-x2
                                y=y1-y2
                                a=math.pi - math.acos((x2-x1)/math.sqrt(x*x+y*y))
                                x=(x1+7*x2)//8
                                y=(y1+7*y2)//8
                                draw.line((x+int((10*math.cos(a+math.pi/10))),
                                                        y-int(10*math.sin(a+math.pi/10)),x,y),fill='black')
                                draw.line((x+int(10*math.cos(a-math.pi/10)),
                                             y-int(10*math.sin(a-math.pi/10)),x,y),fill='black')
                    lines=0
                    if(j>0):
                        if(places[i+1][j-1]!=-1):
                            lines=lines+1
                            means[places[i+1][j-1]]=means[places[i+1][j-1]]+means[places[i][j]]
                            connected[i+1][j-1]=True
                            x1=points[places[i][j]][0]
                            y1=points[places[i][j]][1]
                            x2=points[places[i+1][j-1]][0]
                            y2=points[places[i+1][j-1]][1]
                            draw.line((x1,y1,x2,y2),fill='black')
                            x=x1-x2
                            y=y1-y2
                            a=math.pi - math.asin((y2-y1)/math.sqrt(x*x+y*y))
                            x=(x1+7*x2)//8
                            y=(y1+7*y2)//8
                            draw.line((x+int(10*math.cos(a+math.pi/10)),y-int(10*math.sin(a+math.pi/10)),x,y),fill='black')
                            draw.line((x+int(10*math.cos(a-math.pi/10)),y-int(10*math.sin(a-math.pi/10)),x,y),fill='black')
                    if(places[i+1][j]!=-1):
                        if(lines==0)or(i % 2==0):
                            lines=lines+1
                            means[places[i+1][j]]=means[places[i+1][j]]+means[places[i][j]];
                            connected[i+1][j]=True
                            x1=points[places[i][j]][0]
                            y1=points[places[i][j]][1]
                            x2=points[places[i+1][j]][0]
                            y2=points[places[i+1][j]][1]
                            draw.line((x1,y1,x2,y2),fill='black')
                            x=x1-x2
                            y=y1-y2
                            a=math.pi - math.asin((y2-y1)/math.sqrt(x*x+y*y))
                            x=(x1+7*x2)//8
                            y=(y1+7*y2)//8
                            draw.line((x+int(10*math.cos(a+math.pi/10)),y-int(10*math.sin(a+math.pi/10)),x,y),fill='black')
                            draw.line((x+int(10*math.cos(a-math.pi/10)),y-int(10*math.sin(a-math.pi/10)),x,y),fill='black')
                    if(j<2):
                        if(places[i+1][j+1]!=-1)and((lines==0)or(i % 2==0)):
                            lines=lines+1
                            means[places[i+1][j+1]]=means[places[i+1][j+1]]+means[places[i][j]]
                            connected[i+1][j+1]=True
                            x1=points[places[i][j]][0]
                            y1=points[places[i][j]][1]
                            x2=points[places[i+1][j+1]][0]
                            y2=points[places[i+1][j+1]][1]
                            draw.line((x1,y1,x2,y2),fill='black')
                            x=x1-x2
                            y=y1-y2
                            a=math.pi - math.asin((y2-y1)/math.sqrt(x*x+y*y));
                            x=(x1+7*x2)//8
                            y=(y1+7*y2)//8
                            draw.line((x+int(10*math.cos(a+math.pi/10)),y-int(10*math.sin(a+math.pi/10)),x,y),fill='black')
                            draw.line((x+int(10*math.cos(a-math.pi/10)),y-int(10*math.sin(a-math.pi/10)),x,y),fill='black')
        del draw
        self.answ=str(means[nums-1])
        self.flags=2
