from tkinter import *
import wave
from SignalWidget import *
from PIL import Image, ImageDraw, ImageTk

def pointFromBuff(buff, sampwidth):
    points=[]
    minusBit=(2**(8*sampwidth-1))
    for i in range(0,len(buff)-sampwidth,sampwidth):
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
        heigth = 1024

        wgt = signalwidget(self.framerate, self.sampwidth, heigth, 4)
        wgt.setData(self.samples)
        wgt.saveImage("res.png")
        self.image = wgt.getImage().resize((self.canvasW, self.canvasH))

        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)


app=App()