class Matrix:
    def __createNill(self):
        self.matr=[]
        for y in range(self.y):
            nillVec=[]
            for x in range(self.x):
                nillVec.append(0)
            self.matr.append(nillVec)
    def __init__(self, n=3, m='!'):
        if not(isinstance(m, int)):
            m=n
        if(n<=0):
            n=3
            m=n
        self.y=n
        self.x=m
        self.__createNill()
    def __str__(self):
        res=""
        for y in range(self.y):
            for x in range(self.x):
                res += str(self.matr[y][x])+ " "
            if(y!=self.y-1):
                res+='\n'
        return res
    def __eq__(self, other):
        if(self.y!=other.y):
            return False
        if(self.x!=other.x):
            return False
        for y in range(self.y):
            for x in range(self.x):
                if(self.matr[y][x]!=other.matr[y][x]):
                    return False
        return True
    def __ne__(self, other):
         return not(self==other)
    def __len__(self):
        return(min(self.y,self.x))
    def __add__(self, other):
        if not (isinstance(other, Matrix)):
            return False
        if(self.y!=other.y):
            return self
        if(self.x!=other.x):
            return self
        res=Matrix(self.y, self.x)
        for y in range(self.y):
            for x in range(self.x):
                res.__setIElem(y, x, self.matr[y][x] + other.matr[y][x])
        return res
    def __sub__(self, other):
        return(self+(-1)*other)
    def __rmul__(self, other):
        res=Matrix(self.y,self.x)
        if not(isinstance(other, int)) and not(isinstance(other, float)):
            if not (isinstance(other, Matrix)):
                return False
            if (self.x != other.y):
                return False
            res = Matrix(self.y, other.x)
            for y in range(self.y):
                for x in range(other.x):
                    elemRes = 0
                    for k in range(other.y):
                        elemRes += self.matr[y][k] * other.matr[k][x]
                    res.__setIElem(y, x, elemRes)
            return res
        for y in range(self.y):
            for x in range(self.x):
                res.matr[y][x]=self.matr[y][x]*other
        return res
    def __setIElem(self, y, x, data):
        if not(isinstance(x, int)):
            return False
        if not(isinstance(y, int)):
            return False
        if(x>=self.x)or(x<0):
            return False
        if(y>=self.y)or(y<0):
            return False
        self.matr[y][x]=data
    def getN(self):
        return self.y
    def getM(self):
        return self.x
    def setData(self, data):
        if not (isinstance(data, list)):
            return False
        self.y = len(data)
        self.x = len(data[0])
        self.__createNill()
        for y in range(self.y):
            for x in range(self.x):
                if(len(data[y])<=x):
                    self.__setIElem(y, x, 0)
                else:
                    self.__setIElem(y, x, data[y][x])
        return self
    def getMatrXY(self,x,y):
        if(x<0) or (x>=self.x):
            return False
        if(y<0) or (y>=self.y):
            return False
        return self.matr[y][x]
    def layOn(self,other):
        if not (isinstance(other, Matrix)):
            return 0
        if (self.y != other.y):
            return 0
        if (self.x != other.x):
            return 0
        res=0
        for y in range(self.y):
            for x in range(self.x):
                res+=self.matr[y][x]*other[y][x]
        return res
    def setSobelX(self):
        self.y=3
        self.x=3
        self.matr=[[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
    def setSobelY(self):
        self.y=3
        self.x=3
        self.matr=[[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
    def setPrewittX(self):
        self.y=3
        self.x=3
        self.matr=[[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]]
    def setPrewittY(self):
        self.y=3
        self.x=3
        self.matr=[[-1, -1, -1],[0, 0, 0],[1, 1, 1]]
    def setGauss(self):
        self.y=5
        self.x=5
        self.matr=[[0.000789,0.006581,0.013347,0.006581,0.000789],
                   [0.006581,0.054901,0.111345,0.054901,0.006581],
                   [0.013347,0.111345,0.225821,0.111345,0.013347],
                   [0.006581,0.054901,0.111345,0.054901,0.006581],
                   [0.000789,0.006581,0.013347,0.006581,0.000789]]
    def setAllOne(self, n=3):
        self.y=n
        self.x=n
        for y in range(n):
            for x in range(n):
                self.__setIElem(y,x,1)

def getPrewittMatrY():
    matr = Matrix()
    matr.setPrewittY()
    return matr

def getPrewittMatrX():
    matr = Matrix()
    matr.setPrewittX()
    return matr
def getSobelMatrX():
    matr = Matrix()
    matr.setSobelX()
    return matr
def getSobelMatrY():
    matr = Matrix()
    matr.setSobelY()
    return matr
def getGauss():
    matr = Matrix()
    matr.setGauss()
    return matr
def getOneForAll(n=3):
    matr = Matrix()
    matr.setAllOne()
    return matr