# TODO: проанализировать речевые участки через спектрограмму
# взять несколько заранее сделанных файлов, взять первые 10 секунд, больше не стоит
# отрезать тишину, получить зонные значения в файл
# взять медианное значение
# вычислить наименьшее значения для зон, чтобы сумма отклонений была наименьшей
# проверить суммарное отклонение от медианы с вычисленным
import wave
from Signals import *
from soundCommon import *
import statistics

researchTime = 10
fileNames = ["sample.wav", "tree.wav", "bear.wav"]
spectr = [] #тут все спектры, как signal
zoneAver = []
zone = [0.02, 0.4, 0.4, 0.18]
zone1 = []
zone2 = []
zone3 = []
zone4 = []
for file in fileNames:
    # чтение всех файлов
    wav = wave.open(file, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(min(researchTime * framerate, nframes*nchannels))
    print(framerate)
    sign = signal(pointFromBuff(content, sampwidth))
    # отрезание тишины и получение спектрограммы
    sign.deleteSilence(framerate * 100, 900)
    spectr.append(signal(sign.getFurie(0, 1024)))
    # получение значения для областей спектрограммы
    aver = spectr[len(spectr)-1].getAverZone(zone)
    maxAver = max(aver)
    # нормализация значений областей спектрограммы
    averRel = []
    for item in aver:
        averRel.append((100*item)/maxAver)
    zone1.append(averRel[0])
    zone2.append(averRel[1])
    zone3.append(averRel[2])
    zone4.append(averRel[3])
    zoneAver.append(averRel)
    print(averRel)
# медианные значения по областям
medin = [statistics.median(zone1), statistics.median(zone2), statistics.median(zone3), statistics.median(zone4)]
medinDev = 0
for item in zoneAver:
    medinDev += abs(medin[0]-item[0])
    medinDev += abs(medin[1]-item[1])
    medinDev += abs(medin[2]-item[2])
    medinDev += abs(medin[3]-item[3])
print('Для медианного значения зон ', medin, ' отклонение равно ', medinDev)
# проверка окрестностей значения медиан, как более оптимальные значения
for add1 in range(-10,10):
    for add2 in range(-10,10):
        for add3 in range(-10, 10):
            for add4 in range(-10,10):
                newMedin = [medin[0]+add1, medin[1]+add2, medin[2]+add3, medin[3]+add4]
                tmpDev=0
                for item in zoneAver:
                    tmpDev += abs(newMedin[0] - item[0])
                    tmpDev += abs(newMedin[1] - item[1])
                    tmpDev += abs(newMedin[2] - item[2])
                    tmpDev += abs(newMedin[3] - item[3])
                if(tmpDev<medinDev):
                    print('Для медианного значения зон ', newMedin, ' отклонение равно ', tmpDev)