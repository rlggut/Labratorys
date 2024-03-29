import math
def pointFromBuff(buff, sampwidth):
    points=[]
    minusBit=(2**(8*sampwidth-1))
    for i in range(0,len(buff)-sampwidth,sampwidth):
        pt=0
        for j in range(sampwidth-1,-1,-1):
            pt=pt*256+buff[i+j]
        if(pt>minusBit):
            pt=-(2*minusBit-pt)
        points.append(pt)
    return(points)
def byteArrFromPoints(points, sampwidth):
    res=[]
    if(sampwidth==1): return points
    for pt in points:
        for i in range(sampwidth):
            res.append(pt & 0xFF)
            pt=pt>>8
    return bytearray(res)

def chooseChannel(buff=[],channelsNum=1,currentNum=1):
    res=[]
    ind=0
    for point in buff:
        if ind==currentNum-1:
            res.append(point)
        ind=(ind+1)%channelsNum
    return res
def deleteSilence(samples, framerate=8000, chunkTimeSize=100, threshold=400):
    pointForResearch = chunkTimeSize * framerate // 1000
    newSample=[]
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=abs(samples[i+j])
        power /= pointForResearch
        if(power>threshold):
            for j in range(pointForResearch):
                newSample.append(samples[i+j])
    return(newSample)

#https://ru.wikibooks.org/wiki/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2/%D0%91%D1%8B%D1%81%D1%82%D1%80%D0%BE%D0%B5_%D0%BF%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A4%D1%83%D1%80%D1%8C%D0%B5#C++
TwoPi = 6.283185307179586;
def FFTAnalysis(AVal):
    if(len(AVal)==0):
        return ([])
    AVal=AVal[:2**(int(math.log2(len(AVal))))]
    Nvl = len(AVal)
    n = Nvl * 2
    Tmvl = []
    for i in range(0,n,2):
        Tmvl.append(0);
        Tmvl.append(AVal[i//2])
    i = 1
    j = 1
    while (i < n):
        if (j > i):
          Tmpr = Tmvl[i]
          Tmvl[i] = Tmvl[j]
          Tmvl[j] = Tmpr
          Tmpr = Tmvl[i+1]
          Tmvl[i+1] = Tmvl[j+1]
          Tmvl[j+1] = Tmpr
        i = i + 2
        m = Nvl
        while ((m >= 2) and (j > m)):
          j = j - m
          m = m >> 1
        j = j + m
    Mmax = 2
    while (n > Mmax):
        Theta = -TwoPi / Mmax
        Wpi = math.sin(Theta)
        Wtmp = math.sin(Theta / 2)
        Wpr = Wtmp * Wtmp * 2
        Istp = Mmax * 2
        Wr = 1
        Wi = 0
        m = 1
        while (m < Mmax):
            i = m
            m = m + 2
            Tmpr = Wr
            Tmpi = Wi
            Wr = Wr - Tmpr * Wpr - Tmpi * Wpi
            Wi = Wi + Tmpr * Wpi - Tmpi * Wpr
            while (i < n):
                j = i + Mmax
                Tmpr = Wr * Tmvl[j] - Wi * Tmvl[j-1]
                Tmpi = Wi * Tmvl[j] + Wr * Tmvl[j-1]
                Tmvl[j] = Tmvl[i] - Tmpr
                Tmvl[j-1] = Tmvl[i-1] - Tmpi
                Tmvl[i] = Tmvl[i] + Tmpr
                Tmvl[i-1] = Tmvl[i-1] + Tmpi
                i = i + Istp
        Mmax = Istp;
    FTvl = []
    for i in range(Nvl//2):
        j = i * 2
        FTvl.append(2*math.sqrt((Tmvl[j]**2) + (Tmvl[j+1]**2))/Nvl)
    return FTvl
def findLocalMaxPoints(mas, needPoints=True):
    res=[]
    for i in range(1,len(mas)-1,1):
        if(mas[i]>mas[i-1] and mas[i]<mas[i+1]):
            if(needPoints):
                res.append((i,mas[i]))
            else:
                res.append(i)
    return res
def compareMaximasPlaces(max1,max2, step=10):
    comp=0
    i,j=0,0
    n,m=len(max1),len(max2)
    while(i<n and j<m):
        if(abs(max1[i]-max2[j])<=step):
            comp+=1
            i+=1
            j+=1
        elif(max1[i]>max2[j]+step):
            j+=1
        elif(max1[i]+step<max2[j]):
            i+=1
    return comp
def compareMasForMaximasPlaces(max1, max2, proc = False, step=10):
    max1=findLocalMaxPoints(max1, False)
    max2=findLocalMaxPoints(max2, False)
    tmp=compareMaximasPlaces(max1,max2,step)
    if(proc): return (tmp*100)/min(len(max1),len(max2))
    else: return tmp
def getRollingAvarage(data, nums=3):
    res=[]
    sum=0
    for i in range(min(nums, len(data))):
        sum=sum+data[i]/min(nums, len(data))
    res.append(sum)
    for i in range(nums, len(data)):
        sum=sum-data[i-nums]/nums+data[i]/nums
        res.append(sum)
    return res
def hasMainTone(data, step=40, needAvarage=True):
    if(needAvarage):
        data=getRollingAvarage(data)
    maxima = findLocalMaxPoints(data, False)
    dividedTones=0
    for i in range(1,len(maxima)):
        if(abs(maxima[i]/maxima[0]-i)<step/maxima[0]):
            dividedTones+=1
    return (dividedTones>5)
