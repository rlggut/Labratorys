class Matrix:
    def createNill(self):
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
        self.createNill()
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
                res.__setItem(i,j,self.matr[i][j]+other.matr[i][j])
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
                res.__setItem(i,j,elemRes)
        return res
    def __setItem(self, x, y, data):
        if not(isinstance(x, int)):
            return False
        if not(isinstance(y, int)):
            return False
        if(x>=self.n)or(x<0):
            return False
        if(y>=self.m)or(y<0):
            return False
        self.matr[x][y]=data

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
    def SobelX(self):
        self.n=3
        self.m=3
        self.matr=[[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
    def SobelY(self):
        self.n=3
        self.m=3
        self.matr=[[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
    def PrewittX(self):
        self.n=3
        self.m=3
        self.matr=[[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]]
    def PrewittY(self):
        self.n=3
        self.m=3
        self.matr=[[-1, -1, -1],[0, 0, 0],[1, 1, 1]]

    def f1(self):
        self.n = 3
        self.m = 3
        self.matr = [[5, 6, 4], [8, 9, 7], [-4, -5, -3]]
    def f2(self):
        self.n = 3
        self.m = 3
        self.matr = [[3, 4, 9], [2, -1, 6], [5, 3, 5]]

sob=Matrix()
sob.f1()
print(sob,'\n')
prew=Matrix()
prew.f2()
print(prew,'\n')
print(sob*prew,'\n')