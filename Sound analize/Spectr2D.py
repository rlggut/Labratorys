from Signals import *
from PIL import Image, ImageDraw, ImageTk

def drawSpectrLine(data, maxAmpl, timeStep=100, blockSize=1):
    image = Image.new("RGB", (timeStep, len(data)), "black")
    draw = ImageDraw.Draw(image)
    for i in range(len(data)//blockSize):
        aver=0
        for j in range(blockSize):
            aver+=data[i*blockSize+j]
        aver//=blockSize
        paint = (0,0,int((255*aver)/maxAmpl))
        draw.rectangle([(0, i*blockSize), (timeStep-1, min((i+1)*blockSize,len(data)-1))], fill=paint, width=1)
    return image


class spectr2D():
    def __init__(self, framerate):
        self._maxAmpl = framerate/4
        self._furieCount=512

    def setData(self, sig = []):
        if (isinstance(sig, signal)): self._signal = sig.getData()
        else: self._signal = sig
        self._width=len(self._signal)
        self._width=(self._width//100)*100
        self._image = Image.new("RGB", (self._width, self._furieCount//2), "white")
        timeStep=self._furieCount
        for i in range(self._width//100):
            frm=i*timeStep
            to=frm+self._furieCount
            if(to>=len(self._signal)):
                to=len(self._signal)-1
                frm=to-self._furieCount
            self._image.paste(drawSpectrLine(self._signal[frm:to],self._maxAmpl,timeStep,4), (i*100,0))
        self._image.save("spectr2D.png")
