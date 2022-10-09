class Matrix:
    def createNill(self):
        self.matr=[]
        for j in range(self.m):
            nillVec=[]
            for i in range(self.n):
                nillVec.append(0)
            self.matr.append(nillVec)
    def __init__(self, m=3, n='!'):
        if not(isinstance(m, int)):
            m=3
        if(n=='!'):
            if(m<=0):
                m=3
            n=m
        self.n=n
        self.m=m
        self.createNill()
    def __str__(self):
        res=""
        for i in range(len(self.matr)):
            for elem in self.matr[i]:
                res += str(elem)+ " "
            if(i!=len(self.matr)-1):
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
        res=Matrix(self.m, self.n)
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
    def SobelX(self):
        n=3
        m=3
        self.matr=[[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
    def SobelY(self):
        n=3
        m=3
        self.matr=[[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
    def PrewittX(self):
        n=3
        m=3
        self.matr=[[-1, -1, -1],[0, 0, 0],[1, 1, 1]]
    def PrewittY(self):
        n=3
        m=3
        self.matr=[[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]]

sob=Matrix()
sob.SobelX()
print(sob,'\n')
prew=Matrix()
prew.PrewittX()
print(prew,'\n')
print(prew==sob,'\n')
sum=prew+sob
print(sum,'\n')
sum-=prew
print(sum,'\n')
sum-=sob
print(sum,'\n')