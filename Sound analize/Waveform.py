from PIL import Image, ImageDraw, ImageTk

class waveform():
    def __init__(self, height=400, sampwidth=2, midPoint=-1):
        self._height = height
        self._sampwidth = sampwidth
        self.setMaxAmpl()
        if(midPoint==-1):
            self._midPoint = self._height // 2
        else:
            self._midPoint = midPoint
    def setMaxAmpl(self, maxAmp=-1):
        if(maxAmp==-1):
            self._maxAmp=2 ** (self._sampwidth * 8 - 1)
        else:
            self._maxAmp = maxAmp
    def setData(self, sig, ):
        self._signal = sig
        self._width = len(sig)
        self._image = Image.new("RGB", (self._width, self._height), "white")

        self.draw = ImageDraw.Draw(self._image)
        self.draw.line([(0, self._midPoint), (len(self._signal), self._midPoint)], fill="green", width=1)
        lastY =  (self._midPoint) - self._signal[0]
        t = 1
        for i in range(1,len(self._signal)):
            posY = self._signal[i]
            posY = (posY * (self._midPoint)) // self._maxAmp
            self.draw.line([(t - 1, lastY), (t, - posY + self._midPoint)], fill="green", width=1)
            lastY = -posY + (self._midPoint)
            t += 1
        self.photo = ImageTk.PhotoImage(self._image)
    def getPhoto(self):
        return self.photo
    def getImage(self):
        return self._image
    def saveImage(self, path="res.png"):
        self._image.save(path)