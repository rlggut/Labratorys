#License: CC BY
#Roman Gutenkov, 16/05/23
#Version: 1.0.3-1

import wave
from Signals import *
from soundCommon import *
import time

filename = "sample.wav"
furieCount = 512
silenceEdge = 300
timeSlice = 100

wav = wave.open(filename, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
content = wav.readframes(nframes*nchannels)
signal = signal(filename)

tmpData = signal.getData()
speach=[]
sptr2 = FFTAnalysis(tmpData[:furieCount])
for i in range(1, len(tmpData)//furieCount):
    sptr1 = FFTAnalysis(tmpData[i*furieCount:(i+1)*furieCount])
    if(int(compareMasForMaximasPlaces(sptr1,sptr2,True))>50):
        for j in range((i-1)*furieCount,i*furieCount):
            speach.append(tmpData[j])
    sptr2 = sptr1

wav = wave.open("spectr_"+filename, mode="wb")
wav.setparams((1,signal.getSampwidth(),signal.getFramerate(), len(speach)//signal.getSampwidth(),"NONE","not compressed"))
wav.writeframes(byteArrFromPoints(speach,signal.getSampwidth()))
wav.close()

signal.deleteSilence(framerate, 100, silenceEdge)
signal.writeToFile("silencer_"+filename)