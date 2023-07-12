class Matrix:
    def __createNill(self):
        self.matr=[]
        for i in range(self.n):
            nillVec=[]
            for j in range(self.m):
                nillVec.append(0)
            self.matr.append(nillVec)
    def __init__(self, n=3, m='!'):
        if not(isinstance(m, int)):
            n=3
        if(m=='!'):
            if(n<=0):
                n=3
            m=n
        self.n=n
        self.m=m
        self.__createNill()
    def __str__(self):
        res=""
        for j in range(self.m):
            for i in range(self.n):
                res += str(self.matr[i][j])+ " "
            if(j!=self.m-1):
                res+='\n'
        return res
    def __eq__(self, other):
        if(self.n!=other.n):
            return False
        if(self.m!=other.m):
            return False
        for j in range(self.m):
            for i in range(self.n):
                if(self.matr[i][j]!=other.matr[i][j]):
                    return False
        return True
    def __ne__(self, other):
         return not(self==other)
    def __len__(self):
        return(min(self.n,self.m))
    def __add__(self, other):
        if(self.n!=other.n):
            return self
        if(self.m!=other.m):
            return self
        res=Matrix(self.n, self.m)
        for j in range(self.m):
            for i in range(self.n):
                res.__setIElem(i, j, self.matr[i][j] + other.matr[i][j])
        return res
    def __sub__(self, other):
        return(self+(-1)*other)
    def __rmul__(self, other):
        res=Matrix(self.m,self.n)
        if not(isinstance(other, int)):
            return False
        for y in range(self.m):
            for x in range(self.n):
                res.matr[x][y]=self.matr[x][y]*other
        return res
    def __mul__(self, other):
        if not(isinstance(other, Matrix)):
            return False
        if (self.n != other.m):
            return False
        res = Matrix(other.n, self.m)
        for j in range(self.m):
            for i in range(other.n):
                elemRes=0
                for k in range(self.n):
                    elemRes+=self.matr[k][j]*other.matr[i][k]
                res.__setIElem(i, j, elemRes)
        return res
    def __setIElem(self, x, y, data):
        if not(isinstance(x, int)):
            return False
        if not(isinstance(y, int)):
            return False
        if(x>=self.n)or(x<0):
            return False
        if(y>=self.m)or(y<0):
            return False
        self.matr[x][y]=data
    def getN(self):
        return self.n
    def getM(self):
        return self.m
    def setData(self, data):
        if not (isinstance(data, list)):
            return False
        self.n = len(data)
        self.m = len(data[0])
        self.__createNill()
        for j in range(self.m):
            for i in range(self.n):
                if(len(data[j])<=i):
                    self.__setIElem(i, j, 0)
                else:
                    self.__setIElem(i, j, data[i][j])
        return self
    def getMatrXY(self,x,y):
        if(x<0):
            return False
        if(y<0):
            return False
        if(x>=self.n):
            return False
        if(y>=self.m):
            return False
        return self.matr[x][y]
    def layOn(self,other):
        if not (isinstance(other, Matrix)):
            return 0
        if (self.n != other.n):
            return 0
        if (self.m != other.m):
            return 0
        res=0
        for y in range(self.m):
            for x in range(self.n):
                res+=self.matr[x][y]*other[x][y]
        return res
    def setSobelX(self):
        self.n=3
        self.m=3
        self.matr=[[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
    def setSobelY(self):
        self.n=3
        self.m=3
        self.matr=[[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
    def setPrewittX(self):
        self.n=3
        self.m=3
        self.matr=[[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]]
    def setPrewittY(self):
        self.n=3
        self.m=3
        self.matr=[[-1, -1, -1],[0, 0, 0],[1, 1, 1]]
    def setGauss(self):
        self.n=5
        self.m=5
        self.matr=[[0.000789,0.006581,0.013347,0.006581,0.000789],
                   [0.006581,0.054901,0.111345,0.054901,0.006581],
                   [0.013347,0.111345,0.225821,0.111345,0.013347],
                   [0.006581,0.054901,0.111345,0.054901,0.006581],
                   [0.000789,0.006581,0.013347,0.006581,0.000789]]
    def setAllOne(self, n=3):
        self.n=n
        self.m=n
        for y in range(n):
            for x in range(n):
                self.__setIElem(x,y,1)

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