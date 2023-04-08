from Waveform import *
class spectrofm(waveform):
    def drawAverZone(self, zone=[0.02, 0.4, 0.4, 0.18]):
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
            avarage = (avarage * (self._midPoint)) // self._maxAmp
            self.draw.line([(startPoint, self._midPoint - avarage), (endPoint, self._midPoint - avarage)], fill="green", width=1)
            self._avarage.append(avarage)
            startPoint=endPoint
        self.photo = ImageTk.PhotoImage(self._image)