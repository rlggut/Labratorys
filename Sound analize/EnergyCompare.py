#ToDo: сравнение времени вычисления стандартной формулы мощности и альтернативной для обнаружения тишины в сигнале
import wave
from soundCommon import *
import time

fileNames = ["sample.wav", "tree.wav"]
researchTime = 10
chunkTimeSize=100
for file in fileNames:
    # чтение всех файлов
    wav = wave.open(file, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(min(researchTime * framerate, nframes))
    samples = pointFromBuff(content, sampwidth)
    pointForResearch = chunkTimeSize * framerate // 1000

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=(samples[i+j]*samples[i+j])
        power /= pointForResearch
    end1 = time.time() - start  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=(samples[i+j]**2)
        power /= pointForResearch
    end2 = time.time() - start  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=abs(samples[i+j])
        power /= pointForResearch
    end3 = time.time() - start  ## собственно время работы программы

    print(end1,end2,end3)