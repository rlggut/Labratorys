class Matrix:
    def createNill(self):
        self.matr=[]
        nillVec=[]
        for i in range(self.n):
            nillVec.append(0)
        for j in range(self.m):
            self.matr.extend(nillVec)
    def __init__(self, n):
        self.n=n
        self.m=n
        self.createNill()
    def __init__(self, m, n):
        self.n=n
        self.m=m
        self.createNill()
    def __init__(self):
        self.n=3
        self.m=3
        self.createNill()
    def __str__(self):
        res=""
        print(self.matr)
        for elem in self.matr:
            res += str(elem)+ " " 
        return res
        
        
ma=Matrix()
print(ma)