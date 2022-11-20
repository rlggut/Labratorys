def from10(n,deg):
    rs=""
    while(n>0):
        t=(n % deg)
        if(t>=10):
            rs=chr(ord('A')+t-10)+rs
        else:
            rs=chr(ord('0')+t)+rs
        n=n//deg
    return(rs)
def to10(st,deg):
    rs=0
    for i in (range(len(st))):
        rs=rs*deg
        print(rs,' ',st[i])
        if (ord(st[i])-ord('0')<=9):
            rs=rs+(ord(st[i])-ord('0'))
        else:
            rs=rs+(ord(st[i])-ord('A'))+10
    return(rs)