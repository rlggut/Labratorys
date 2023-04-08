from soundCommon import *
class signal():
    def __init__(self, data = []):
        self._signal = data
    def setData(self, data = []):
        self._signal = data
    def getData(self):
        return self._signal
    def deleteSilence(self, packSize = 8000,boundry = 400):
        self._signal = deleteSilence(self._signal, packSize, 1, boundry)
    def getSize(self):
        return len(self._signal)
    def getFutie(self, startPoint=0,endPoint=-1):
        if(endPoint==-1):
            endPoint=len(self._signal)
        return FFTAnalysis(self._signal[startPoint:endPoint])
    def getAverZone(self, zone=[0.02, 0.4, 0.4, 0.18]):
        avarageZ = []
        startPoint=0
        for percent in zone:
            endPoint=int(len(self._signal) * percent)+startPoint
            if (endPoint > len(self._signal)):
                break
            avarage = 0
            for i in range(startPoint, endPoint):
                avarage+=self._signal[i]
            avarage /= (endPoint-startPoint)
            avarageZ.append(avarage)
            startPoint=endPoint
        return avarageZ
    def getAverZoneData(self, zone=[0.02, 0.4, 0.4, 0.18]):
        avarageZ = self.getAverZone(zone)
        data=[]
        startPoint = 0
        ind=0
        for percent in zone:
            endPoint = int(len(self._signal) * percent) + startPoint
            if (endPoint > len(self._signal)):
                break
            for i in range(startPoint, endPoint):
                data.append(avarageZ[ind])
            startPoint = endPoint
            ind += 1
        return(data)