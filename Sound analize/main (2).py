from tkinter import *
import wave
import math
from PIL import Image, ImageDraw, ImageTk
class Waveform():
    def __init__(self, height=400, sampwidth=2):
        self._height = height
        self.sampwidth = sampwidth
    def setSignal(self, sig):
        self._signal = sig
        self._width = len(sig)
        self._image = Image.new("RGB", (self._width, self._height), "white")

        self.draw = ImageDraw.Draw(self._image)
        self.draw.line([(0, self._height // 2), (len(self._signal), self._height // 2)], fill="green", width=1)
        maxAmp = 2 ** (self.sampwidth * 8 - 1)
        lastY = self._height // 2
        t = 1
        for i in range(len(self._signal)):
            posY = self._signal[i]
            posY = (posY * (self._height // 2)) // maxAmp
            self.draw.line([(t - 1, lastY), (t, - posY + self._height // 2)], fill=128, width=1)
            lastY = -posY + (self._height // 2)
            t += 1
        self.photo = ImageTk.PhotoImage(self._image)
    def getPhoto(self):
        return self.photo
    def getImage(self):
        return self._image
    def saveImage(self, path="res.png"):
        self._image.save(path)

def pointFromBuff(buff, sampwidth):
    points=[]
    minusBit=(2**(8*sampwidth-1))
    for i in range(0,len(buff)-sampwidth,sampwidth):
        pt=0
        pt=buff[i+1]*256+buff[i]
        if(pt>minusBit):
            pt=-(2*minusBit-pt)
        points.append(pt)
    return(points)

class SignalWidget():
    def __init__(self, framerate=8000, sampwidth=2, height=400, frameImages=4):
        self._frameImage = frameImages
        self._framerate = framerate
        self._sampwidth = sampwidth
        self._height = height
        self._timePerImage = 100 #ms

        self._haveImage = False
    def setSignal(self, sig=[]):
        self._haveImage = False
        self._signal = sig
        self._time = (len(sig)*1000) // self._framerate
        self._signal = self._signal[:((self._time * self._framerate) // 1000)]
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._images=[]
        self._waves=[]
        for i in range(self._numsOfFrames):
            wave = Waveform(self._height, self._sampwidth)
            wave.setSignal(self._signal[i*self._sizeForFrame
                                        : min((i+1)*self._sizeForFrame,len(self._signal))])
            self._waves.append(wave)
            self._images.append(self._waves[i].getImage())
    def getImage(self):
        self._haveImage = True
        self._image = Image.new("RGB", (self._sizeForFrame * self._frameImage, self._height), "white")
        for i in range(self._frameImage):
            self._image.paste(self._images[i],(i*((self._timePerImage * self._framerate) // 1000), 0))
        return self._image
    def saveImage(self, path="res.png"):
        if not self._haveImage:
            self.getImage()
        self._image.save(path)
class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 1000
        self.canvasH = 400
        self.researchTime = 3
        self.researchDelta=100
        self.window.geometry("1000x400")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.__getData()

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0, rowspan=12)

        self.__Draw()
        self.window.mainloop()

    def __getData(self):
        self.wav = wave.open(self.filename, mode="r")
        (self.nchannels, self.sampwidth, self.framerate, self.nframes, comptype, compname) = self.wav.getparams()
        self.content = self.wav.readframes(min(self.researchTime * self.framerate, self.nframes))
        self.samples = pointFromBuff(self.content, self.sampwidth)
        self.__deleteSilence()
    def __deleteSilence(self):
        pointForResearch = self.researchDelta * self.framerate // 1000
        newSample=[]
        for i in range(0,len(self.samples)-pointForResearch,pointForResearch):
            power=0
            for j in range(pointForResearch):
                power+=abs(self.samples[i+j])
            power /= pointForResearch
            if(power>4*self.researchDelta):
                for j in range(pointForResearch):
                    newSample.append(self.samples[i+j])
        self.samples = newSample
    def __Draw(self):
        heigth = 1024

        #wave = Waveform(heigth, self.sampwidth)
        #wave.setSignal(self.samples)
        #self.image = wave.getImage().resize((self.canvasW, self.canvasH))
        #wave.saveImage("res.png")

        wgt = SignalWidget(self.framerate, self.sampwidth, heigth)
        wgt.setSignal(self.samples)
        wgt.saveImage("res.png")
        self.image = wgt.getImage().resize((self.canvasW, self.canvasH))

        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)


app=App()