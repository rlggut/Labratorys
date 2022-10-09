class Matrix:
    def createNill(self):
        self.matr=[]
        nillVec=[]
        for i in range(self.n):
            nillVec.append(0)
        for j in range(self.m):
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
            res+='\n'
        return res
        
        
ma=Matrix(3)
print(ma)