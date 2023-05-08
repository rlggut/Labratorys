from Signals import *
from PIL import Image, ImageDraw, ImageTk

def drawSpectrLine(data, width=100,height=-1, blockSizeVert=1):
    if(height==-1): height=100
    image = Image.new("RGB", (width, height), "white")
    kf=height/len(data)
    draw = ImageDraw.Draw(image)
    data = FFTAnalysis(data)
    maxAmpl = max(data)
    blocks=len(data)//blockSizeVert
    for i in range(blocks):
        aver=0
        for j in range(blockSizeVert):
            aver+=data[i*blockSizeVert+j]
        aver//=blockSizeVert
        paint = (0,min(int((255*aver)/maxAmpl),255),0)
        draw.rectangle([(0, int((blocks-i)*blockSizeVert*2*kf)), (width-1, int(min((blocks-i-1)*blockSizeVert*2*kf,height)))], fill=paint, width=1)
    del draw
    return image


class spectr2D():
    def __init__(self, framerate):
        self._framerate=framerate
        self._furieCount=1024
        self._timeStep=self._furieCount//16
        self._lineWidth=1

    def setData(self, sig = []):
        if (isinstance(sig, signal)): self._signal = sig.getData()
        else: self._signal = sig
        self._width=len(self._signal)
        if(self._width==0): return
        self._width=(self._width//self._timeStep)*self._timeStep
        self._image = Image.new("RGB", ((self._width*self._lineWidth)//self._timeStep, self._furieCount//2), "white")
        for i in range(self._width//self._timeStep):
            frm=i*self._furieCount
            to=frm+self._furieCount
            if(to>=len(self._signal)):
                to=len(self._signal)-1
                frm=to-self._furieCount
            self._image.paste(drawSpectrLine(self._signal[frm:to],self._lineWidth,512,1), (i*self._lineWidth,0))
        self._image.save("spectr2D.png")
