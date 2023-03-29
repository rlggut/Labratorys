import math
from Waveform import *
from PIL import Image, ImageDraw, ImageTk
class signalwidget():
    def __init__(self, framerate=8000, sampwidth=2, height=400, frameImages=4):
        self._frameImage = frameImages
        self._framerate = framerate
        self._sampwidth = sampwidth
        self._height = height
        self._timePerImage = 100 #ms

        self._haveImage = False
    def setData(self, sig=[]):
        self._haveImage = False
        self._signal = sig
        self._time = (len(sig)*1000) // self._framerate
        self._signal = self._signal[:((self._time * self._framerate) // 1000)]
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._images=[]
        self._waves=[]
        for i in range(self._numsOfFrames):
            wave = waveform(self._height, self._sampwidth)
            wave.setData(self._signal[i*self._sizeForFrame
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