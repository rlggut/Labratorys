import math
from Waveform import *
from Signals import *
from PIL import Image, ImageDraw, ImageTk, ImageFont

class signalwidget():
    def __init__(self, framerate=8000, sampwidth=2, height=400, timePerImage = 100, frameImages=4):
        self._frameImage = frameImages
        self._framerate = framerate
        self._sampwidth = sampwidth
        self._height = height
        self._timePerImage = timePerImage #ms
        self._haveImage = False
        self._lastDue = (0,-1)


    def setData(self, sig=[]):
        self._work = True
        if(isinstance(sig, signal)):
            self._signal = sig.getData()
            self._time = (sig.getSize() * 1000) // self._framerate
        else:
            self._signal = sig
            self._time = (len(sig) * 1000) // self._framerate

        self._haveImage = False
        self._signal = self._signal[:((self._time * self._framerate) // 1000)]
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._images=[]
        self._waves=[]
        for i in range(self._numsOfFrames):
            if(not self._work):
                break
            wave = waveform(self._height, self._sampwidth)
            wave.setData(self._signal[i*self._sizeForFrame
                                        : min((i+1)*self._sizeForFrame,len(self._signal))])
            self._waves.append(wave)
            self._images.append(self._waves[i].getImage())
        self.getImage()
        self._work = False
    def stopWork(self):
        self._work=False
    def setZoom(self, zoom):
        self._frameImage = zoom
        self._lastDue = (-1, 0)

    def getImage(self, frm=-1):
        self._work = True
        if(frm == -1 and self._haveImage):
            return self._image
        if(frm == -1):
            frm = 0
        frm = max(min(frm, self._numsOfFrames - self._frameImage),0)
        to = frm+self._frameImage
        if(self._lastDue != (frm,to)):
            self._image = Image.new("RGB", (self._sizeForFrame * self._frameImage, self._height), "white")
            for i in range(frm, to):
                if(i>=len(self._images) or (not self._work)):
                    break
                self._image.paste(self._images[i], ((i-frm)*((self._timePerImage * self._framerate) // 1000), 0))
        self._haveImage = True
        self._lastDue=(frm,to)
        if(len(self._images)==0):
            draw_text = ImageDraw.Draw(self._image)
            fnt = ImageFont.truetype("arial.ttf", self._image.height//2)
            draw_text.text((self._image.width//3,self._image.height//4), 'NO DATA',font=fnt, fill=('#1C0606') )
            del draw_text
        self._work = False
        return self._image
    def saveImage(self, path="res.png"):
        if not self._haveImage:
            self.getImage()
        self._image.save(path)