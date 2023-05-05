from Signals import *
from PIL import Image, ImageDraw, ImageTk

def drawSpectrLine(data, maxAmpl, timeStep=100,height=-1, blockSize=1):
    if(height==-1): height=100
    image = Image.new("RGB", (timeStep, height), "white")
    kf=height/len(data)
    draw = ImageDraw.Draw(image)
    data = FFTAnalysis(data)
    maxAmpl = max(data)
    blocks=len(data)//blockSize
    for i in range(blocks):
        aver=0
        for j in range(blockSize):
            aver+=data[i*blockSize+j]
        aver//=blockSize
        paint = (0,min(int((255*aver)/maxAmpl),255),0)
        draw.rectangle([(0, int((blocks-i)*blockSize*2*kf)), (timeStep-1, int(min((blocks-i-1)*blockSize*2*kf,height)))], fill=paint, width=1)
    del draw
    return image


class spectr2D():
    def __init__(self, framerate):
        self._framerate=framerate
        self._maxAmpl = framerate/4
        self._furieCount=1024

    def setData(self, sig = []):
        if (isinstance(sig, signal)): self._signal = sig.getData()
        else: self._signal = sig
        self._width=len(self._signal)
        if(self._width==0): return
        self._width=(self._width//100)*100
        self._image = Image.new("RGB", (self._width, self._furieCount//2), "white")
        timeStep=self._furieCount
        for i in range(self._width//100):
            frm=i*timeStep
            to=frm+self._furieCount
            if(to>=len(self._signal)):
                to=len(self._signal)-1
                frm=to-self._furieCount
            self._image.paste(drawSpectrLine(self._signal[frm:to],3000,timeStep,512,1), (i*100,0))
        self._image.save("spectr2D.png")
