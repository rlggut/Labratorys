import re

def maskDict(maskStr):
    num1=0
    decim1=0
    num2=-1
    decim2=0
    decimFl=False
    maskPos=[]
    for i in range(len(maskStr)):
        if(maskStr[i]!=' '):
            if(maskStr[i]=='-'):
                num2=num1
                decim2=decim1
                num1=0
                decim1=0
            else:
                if(maskStr[i]=='.'):
                    decimFl=True
                else:
                    if(decimFl):
                        decimFl=False
                        decim1=int(maskStr[i])
                    else:
                        num1=num1*10+int(maskStr[i])
        if(maskStr[i]==' ' or i==len(maskStr)-1):
            if(num2==-1):
                mask=0x00
                if(decim1>0):
                    mask=0xFF-(1<<(decim1-1))
                maskPos.append([num1, mask])
            else:
                pos1=num1*8+decim1-1
                pos2=num2*8+decim2-1
                if(pos1>pos2):
                    tp=num1
                    num1=num2
                    num2=tp
                    tp=decim1
                    decim1=decim2
                    decim2=tp
                    pos1=num1*8+decim1-1
                    pos2=num2*8+decim2-1
                maskLen=pos2-pos1
                mask=0x00
                if(decim1>0):
                    mask=0xFF
                    while(decim1<=8 and maskLen>0):
                        mask=mask-(1<<(decim1-1))
                        decim1+=1
                        maskLen-=1
                maskPos.append([num1,mask])
                for j in range(num1+1,num2):
                    maskPos.append([j,0X00])
                mask=0x00
                if(decim2>0):
                    mask=0xFF
                    while(decim2>0 and maskLen>0):
                        mask=mask-(1<<(decim2-1))
                        decim2-=1
                        maskLen-=1
                maskPos.append([num2,mask])
            num1=0
            decim1=0
            num2=-1
            decim2=0
    maskPos.sort()
    return(dict(maskPos))


pattern='((((\d+)(\.[1-8])?-(\d+)(\.[1-8])?)|(\d+(\.[1-8])?)) ?)*'
maskInp=input()
maskFound=re.search(pattern,maskInp).group(0)
if(len(maskFound)!=len(maskInp)):
    print('String with trash!')
else:
    print(maskDict(maskFound))