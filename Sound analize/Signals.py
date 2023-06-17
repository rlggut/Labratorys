from soundCommon import *
import os
import wave
class signal():
    def __init__(self, data):
        self._signal = []
        self._nchannels = 1
        self._sampwidth = 2
        self._framerate = 8000
        if(isinstance(data,str)):
            self.openFromFile(data)
        elif(isinstance(data,list)):
            self._signal = data
    def openFromFile(self, filename=""):
        if(os.path.isfile(filename)):
            if(filename.count('.wav')):
                wav = wave.open(filename, mode="r")
                (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
                self._nchannels = nchannels
                self._sampwidth = sampwidth
                self._framerate = framerate
                content = wav.readframes(nframes * nchannels)
                self._signal = chooseChannel(pointFromBuff(content, sampwidth), nchannels, 1)
                wav.close()
                return True
        return False
    def writeToFile(self, filename):
        if (filename.count('.wav')):
            wav = wave.open(filename, mode="wb")
            wav.setparams((1,self._sampwidth,self._framerate,self.getSize()//16,"NONE","not compressed"))
            wav.writeframes(byteArrFromPoints(self._signal,self._sampwidth))
            wav.close()
            return True
        else:
            return False
    def getFramerate(self):
        return self._framerate
    def setFramerate(self, frame):
        self._framerate = frame
    def getSampwidth(self):
        return self._sampwidth
    def setSampwidth(self, samp):
        self._sampwidth = samp
    def setData(self, data = []):
        self._signal = data
    def getData(self):
        return self._signal
    def deleteSilence(self, framerate = 8000,chunkTime = 1, boundry = 400):
        self._signal = deleteSilence(self._signal, framerate, chunkTime, boundry)
    def getSize(self):
        return len(self._signal)
    def getFurie(self, startPoint=0, endPoint=-1):
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