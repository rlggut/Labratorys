from tkinter import *
import wave
from PIL import Image, ImageDraw
import numpy as np

def pointFromBuff(buff, sampwidth):
    points=[]
    minusBit=(2**(8*sampwidth-1))
    for i in range(0,len(buff)-sampwidth,sampwidth):
        pt=0
        for j in range(sampwidth):
            pt=pt*256+buff[i+j]
        if(pt>minusBit):
            pt=(minusBit-pt)
        points.append(pt)
    return(points)

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 800
        self.canvasH = 400
        self.window.geometry("800x400")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.__getInfo()

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0, rowspan=12)

        self.__Draw()
        self.window.mainloop()

    def __getInfo(self):
        self.wav = wave.open(self.filename, mode="r")
        (self.nchannels, self.sampwidth, self.framerate, self.nframes, comptype, compname) = self.wav.getparams()
        print(self.nchannels, self.sampwidth, self.framerate, self.nframes)

    def __Draw(self):
        content = self.wav.readframes(min(3*self.framerate,self.nframes))
        samples = pointFromBuff(content, self.sampwidth)
        image1 = Image.new("RGB", (len(samples), self.canvasH), "white")
        draw = ImageDraw.Draw(image1)
        maxAmp=2**(self.sampwidth*8-1)
        t=1
        for i in range(len(samples)):
            posY = samples[i]
            posY = (posY*(self.canvasH//2))//maxAmp
            if(posY>(self.canvasH//2)):
                print(samples[i],maxAmp,posY,"H")
            draw.ellipse([(t, -posY + (self.canvasH//2)), (t, -posY + (self.canvasH//2))], fill ="#ffff33", outline ="red")
            t += 1
        image1.save("res.png")
app=App()