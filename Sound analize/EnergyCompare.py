#ToDo: сравнение времени вычисления стандартной формулы мощности и альтернативной для обнаружения тишины в сигнале
import random
import wave
from soundCommon import *
import time

fileNames = ["sample.wav", "tree.wav","fax.wav"]
researchTime = 10
chunkTimeSize=100
print("filename \t time \t\t x*x \t ** \t alter")
for file in fileNames:
    # чтение всех файлов
    wav = wave.open(file, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(int(min(researchTime * framerate, nframes*nchannels)))
    samples = pointFromBuff(content, sampwidth)
    pointForResearch = chunkTimeSize * framerate // 1000

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=(samples[i+j]*samples[i+j])
        power /= pointForResearch
    end1 = round(time.time() - start,5)  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=(samples[i+j]**2)
        power /= pointForResearch
    end2 = round(time.time() - start,5)  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0,len(samples)-pointForResearch,pointForResearch):
        power=0
        for j in range(pointForResearch):
            power+=abs(samples[i+j])
        power /= pointForResearch
    end3 = round(time.time() - start,5)  ## собственно время работы программы
    print(file,'\t', round(len(samples)/(framerate*nchannels),2),'\t\t', end1,'\t', end2,'\t', end3)

for timr in range(30000,140000,30000):
    samples=[]
    framerate = 8000
    nchannels=1
    for i in range(framerate*timr//1000):
        samples.append(random.randrange(-2000,2000))
    pointForResearch = chunkTimeSize * framerate // 1000

    start = time.time()  ## точка отсчета времени
    for i in range(0, len(samples) - pointForResearch, pointForResearch):
        power = 0
        for j in range(pointForResearch):
            power += (samples[i + j] * samples[i + j])
        power /= pointForResearch
    end1 = round(time.time() - start, 5)  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0, len(samples) - pointForResearch, pointForResearch):
        power = 0
        for j in range(pointForResearch):
            power += (samples[i + j] ** 2)
        power /= pointForResearch
    end2 = round(time.time() - start, 5)  ## собственно время работы программы

    start = time.time()  ## точка отсчета времени
    for i in range(0, len(samples) - pointForResearch, pointForResearch):
        power = 0
        for j in range(pointForResearch):
            power += abs(samples[i + j])
        power /= pointForResearch
    end3 = round(time.time() - start, 5)  ## собственно время работы программы
    print("Rand"+str(timr), '\t', round(len(samples) / (framerate * nchannels), 2), '\t\t', end1, '\t', end2, '\t', end3)