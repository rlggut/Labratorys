import wave
from Signals import *
from soundCommon import *
import time

filename = "sample.wav"
furieCount = 512
silenceEdge = 700
timeSlice = 100

wav = wave.open(filename, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
content = wav.readframes(nframes*nchannels)
signal = signal(filename)
signal.writeToFile("try.wav")
signal.deleteSilence(framerate, 100, silenceEdge)
timeSlice=(timeSlice*framerate)//1000

tmpData = signal.getData()
sptr1 = FFTAnalysis(tmpData[:furieCount])
sptr2 = FFTAnalysis(tmpData[1*furieCount:2*furieCount])

print(int(compareMasForMaximasPlaces(sptr1,sptr2,True)))