class Enumeration:
    def __init__(self, size, last):
        self.size=size
        self.last=last
        self.looped=False
        self.vec=[]
        for i in range(size):
            self.vec.append(0)
    def __add__(self, other):
        res=Enumeration(self.size, self.last)
        res.vec=list(self.vec)
        res.vec[0]=self.vec[0]+int(other)
        res.looped=self.wasLooped()
        for i in range(res.size):
            if(res.vec[i]>=res.last):
                if(i!=res.size-1):
                    res.vec[i+1]+=1
                else:
                    res.looped=True
                res.vec[i]=res.vec[i]%res.last
        return res
    def __str__(self):
        return(str(self.vec))
    def atEnd(self):
        for i in range(self.size):
            if(self.vec[i]!=self.last-1):
                return False
        return True
    def isNill(self):
        for i in range(self.size):
            if(self.vec[i]!=0):
                return False
        return True
    def wasLooped(self):
        return(self.looped)
    def uniq(self):
        for i in range(self.size):
            if(self.vec.count(self.vec[i])>1):
                return False
        return True

'''
How many combinations of symbols "t", "`", "u", "r", "i", "n", "g"  length 6 can be made, so that each symbol was no more than 1 time, symbol '`' wasn't in the beginning and nearest to 'u' and 'i'
'''
def TuringTask():
    sym=['t','`','u','r','i','n','g']
    length=6
    answ=0
    enumerator=Enumeration(length,len(sym))
    while not(enumerator.wasLooped()):
        if(enumerator.uniq()):
            st=""
            for i in range(length):
                st+=sym[enumerator.vec[i]]
            if(st.count('`')==0):
                answ+=1
            elif(st[0]!='`'):
                ps=st.index('`')
                if(st[ps-1]!='u')and(st[ps-1]!='i'):
                    if(ps==5):
                        answ+=1
                    elif(st[ps+1]!='u')and(st[ps+1]!='i'):
                        answ+=1
        enumerator+=1
    print(answ)

def ProektTask():
    sym=['p','r','o','e','k','t']
    length=5
    answ=0
    enumerator=Enumeration(length,len(sym))
    answ=0
    while not(enumerator.wasLooped()):
        st=""
        for i in range(length):
            st+=sym[enumerator.vec[i]]
        if(st.count('o')<=1):
            if(st.count('e')<=1):
                answ+=1
        enumerator+=1
    print(answ)

ProektTask()
TuringTask()