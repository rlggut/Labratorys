from tkinter import *
import wave
from PIL import Image, ImageDraw, ImageTk
class Waveform():
    def __init__(self, width=2000, height=400):
        self._width = width
        self._height = height
        self._image = Image.new("RGB", (self._width, self._height), "white")
    def setSignal(self, sig, sampwidth=2):
        self._signal = sig
        if(len(sig)!=self._width):
            self._width = len(sig)
            self._image = Image.new("RGB", (self._width, self._height), "white")
        self.sampwidth = sampwidth

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
        sizeY=1024
        step=1

        wave = Waveform(len(self.samples), sizeY)
        wave.setSignal(self.samples,self.sampwidth)

        self.image = wave.getImage().resize((self.canvasW, self.canvasH))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        wave.saveImage("res.png")

app=App()