from PIL import Image, ImageDraw, ImageTk

class waveform():
    def __init__(self, height=400, sampwidth=2):
        self._height = height
        self.sampwidth = sampwidth
    def setData(self, sig):
        self._signal = sig
        self._width = len(sig)
        self._image = Image.new("RGB", (self._width, self._height), "white")

        self.draw = ImageDraw.Draw(self._image)
        self.draw.line([(0, self._height // 2), (len(self._signal), self._height // 2)], fill="green", width=1)
        maxAmp = 2 ** (self.sampwidth * 8 - 1)
        lastY =  (self._height // 2) - self._signal[0]
        t = 1
        for i in range(1,len(self._signal)):
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