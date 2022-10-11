'''
How many combinations of letters "p", "r", "o", "e", "k", "t"  length 5 can be made, so that each vowel was no more than 1
'''
def ProektTask():
    sym=['p','r','o','e','k','t']
    answ=0
    for a1 in range(len(sym)):
        for a2 in range(len(sym)):
            for a3 in range(len(sym)):
                for a4 in range(len(sym)):
                    for a5 in range(len(sym)):
                        st=sym[a1]+sym[a2]+sym[a3]+sym[a4]+sym[a5]
                        if(st.count('o')<=1):
                            if(st.count('e')<=1):
                                answ+=1
    print(answ)
'''
How many combinations of symbols "t", "`", "u", "r", "i", "n", "g"  length 6 can be made, so that each symbol was no more than 1 time, symbol '`' wasn't in the beginning and nearest to 'u' and 'i'
'''
def uni(s):
    for i in range(len(s)):
        if(s.count(s[i])>1):
            return False
    return True
def TuringTask():
    sym=['t','`','u','r','i','n','g'] 
    answ=0
    for a1 in range(len(sym)):
        for a2 in range(len(sym)):
            for a3 in range(len(sym)):
                for a4 in range(len(sym)):
                    for a5 in range(len(sym)):
                        for a6 in range(len(sym)):
                            st=sym[a1]+sym[a2]+sym[a3]+sym[a4]+sym[a5]+sym[a6]
                            if(uni(st)):
                                if(st.count('`')==0):
                                    answ+=1
                                elif(st[0]!='`'):
                                    ps=st.index('`')
                                    if(st[ps-1]!='u')and(st[ps-1]!='i'):
                                        if(ps==5):
                                            answ+=1
                                        elif(st[ps+1]!='u')and(st[ps+1]!='i'):
                                            answ+=1
    print(answ)

ProektTask()
TuringTask()