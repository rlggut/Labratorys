from Waveform import *
import math

#https://ru.wikibooks.org/wiki/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2/%D0%91%D1%8B%D1%81%D1%82%D1%80%D0%BE%D0%B5_%D0%BF%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%A4%D1%83%D1%80%D1%8C%D0%B5#C++
TwoPi = 6.283185307179586;

def FFTAnalysis(AVal):
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

class spectrofm(waveform):
    def makeZone(self, zone):
        if(len(self._signal)==0):
            return
        self._zone = zone
        self._avarage = []
        startPoint=0
        for percent in zone:
            endPoint=int(len(self._signal) * percent)+startPoint
            if (endPoint > len(self._signal)):
                break
            avarage = 0
            for i in range(startPoint, endPoint):
                avarage+=self._signal[i]
            avarage /= (endPoint-startPoint)
            self.draw.line([(startPoint, avarage), (endPoint, avarage)], fill="green", width=1)
            self._avarage.append(avarage)
            startPoint=endPoint
        self.photo = ImageTk.PhotoImage(self._image)