from tkinter import *
import wave
from SignalWidget import *
from SpectrForm import *

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
        self.canvasW = 600
        self.canvasH = 200
        self.researchTime = 3
        self.researchDelta=100
        self.window.geometry("600x450")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.__getData()

        self.canvasOscill = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvasOscill.grid(column=0, row=0, columnspan=5)

        self.canvasSpectr = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvasSpectr.grid(column=0, row=2, columnspan=5)

        self.btnLeft = Button(self.frame, text="<-", command=self.__moveOscillLeft, state=DISABLED)
        self.btnLeft.grid(column=0, row=1)
        self.btnRight = Button(self.frame, text="->", command=self.__moveOscillRight)
        self.btnRight.grid(column=4, row=1)

        self.btnPlus = Button(self.frame, text="Zoom in(+)", command=self.__zoomIn)
        self.btnPlus.grid(column=1, row=1)
        self.btnMinus = Button(self.frame, text="Zoom out(-)", command=self.__zoomOut)
        self.btnMinus.grid(column=3, row=1)

        self.lblDurance = Label(self.frame, text=":")
        self.lblDurance.grid(column=2, row=1)

        self.__Draw()
        self.__correctButtons()
        self.window.mainloop()

    def __zoomOut(self):
        self._frameImage = (self._frameImage*2)
        if(self._frameImage+self._from>self._numsOfFrames):
            self._from = self._numsOfFrames - self._frameImage
        self._signalWgt.setZoom(self._frameImage)
        self.__correctButtons()
        self.__Draw()
    def __zoomIn(self):
        self._frameImage=max(1,(self._frameImage//2))
        self._signalWgt.setZoom(self._frameImage)
        self.__correctButtons()
        self.__Draw()
    def __correctButtons(self):
        if (self._numsOfFrames < 2*self._frameImage):
            self.btnMinus['state'] = 'disabled'
        else:
            self.btnMinus['state'] = 'normal'
        if (self._numsOfFrames == 1):
            self.btnPlus['state'] = 'disabled'
        else:
            self.btnPlus['state'] = 'normal'
        if (self._from<(self._numsOfFrames-self._frameImage)):
            self.btnRight['state'] = 'normal'
        else:
            self.btnRight['state'] = 'disabled'
        if (self._from==0):
            self.btnLeft['state'] = 'disabled'
        else:
            self.btnLeft['state'] = 'normal'
    def __moveOscillLeft(self):
        self._from=max(self._from-1,0)
        self.__correctButtons()
        self.__Draw()
    def __moveOscillRight(self):
        self._from = min(self._from + 1, self._numsOfFrames-self._frameImage)
        self.__correctButtons()
        self.__Draw()
    def __getData(self):
        self.wav = wave.open(self.filename, mode="r")
        (self._nchannels, self.sampwidth, self._framerate, self._nframes, comptype, compname) = self.wav.getparams()
        self.content = self.wav.readframes(min(self.researchTime * self._framerate, self._nframes))
        self.samples = pointFromBuff(self.content, self.sampwidth)
        self.__deleteSilence()

        self._timePerImage = 50
        self._frameImage = 4
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._time = (len(self.samples)*1000) // self._framerate
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._signalWgt = signalwidget(self._framerate, self.sampwidth, 1024, self._timePerImage, self._frameImage)
        self._signalWgt.setData(self.samples)
        self._from = 0

        self._spectr = spectrofm(1024, 1)


    def __deleteSilence(self):
        pointForResearch = self.researchDelta * self._framerate // 1000
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
        self._spectrData = FFTAnalysis(self.samples[(self._from)*self._sizeForFrame:
                                                    (self._from+self._frameImage)*self._sizeForFrame])
        self._spectr.setData(self._spectrData)
        self._spectr.makeZone([0.1, 0.4, 0.3, 0.2])

        self.imageOscill = self._signalWgt.getImage(self._from).resize((self.canvasW, self.canvasH))
        self.imageSpectr = self._spectr.getImage().resize((self.canvasW, self.canvasH))
        self.photoOscill = ImageTk.PhotoImage(self.imageOscill)
        self.photoSpectr = ImageTk.PhotoImage(self.imageSpectr)
        self.с_imageOscl = self.canvasOscill.create_image(0, 0, anchor='nw', image=self.photoOscill)

        self.с_imageSpctr = self.canvasSpectr.create_image(0, 0, anchor='nw', image=self.photoSpectr)

        tStart = self._from * self._timePerImage
        timeStr = str(tStart//1000)+":"
        tStart = tStart%1000
        if(tStart<100):
            timeStr = timeStr+'0'
        if(tStart<10):
            timeStr = timeStr+'0'
        timeStr = timeStr + str(tStart) + ' - '

        tEnd = ((self._from+self._frameImage)*self._timePerImage)
        timeStr = timeStr+str(tEnd//1000)+":"
        tEnd = tEnd%1000
        if(tEnd<100):
            timeStr = timeStr+'0'
        if(tEnd<10):
            timeStr = timeStr+'0'
        timeStr = timeStr + str(tEnd)

        self.lblDurance.configure(text=timeStr)


app=App()