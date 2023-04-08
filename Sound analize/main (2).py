from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import wave
from SignalWidget import *
from SpectrForm import *
from Signals import *
from soundCommon import *

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 600
        self.canvasH = 200
        self.researchTime = 3
        self.researchDelta=100
        self._furieCount = 512
        self.window.geometry("600x500")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.signal = signal()
        self.__getData()

        self.btnFileOrig = Button(self.frame, text="Выбрать файл", command=self.__clickedLoadingOrig)
        self.btnFileOrig.grid(column=0, row=0)
        self.lblChoosedOrig = Label(self.frame, text=self.filename)
        self.lblChoosedOrig.grid(column=1, row=0, columnspan=4)

        self.canvasOscill = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvasOscill.grid(column=0, row=1, columnspan=5)

        self.btnLeft = Button(self.frame, text="<-", command=self.__moveOscillLeft, state=DISABLED)
        self.btnLeft.grid(column=0, row=2)
        self.btnRight = Button(self.frame, text="->", command=self.__moveOscillRight)
        self.btnRight.grid(column=4, row=2)

        self.btnPlus = Button(self.frame, text="Zoom in(+)", command=self.__zoomIn)
        self.btnPlus.grid(column=1, row=2)
        self.btnMinus = Button(self.frame, text="Zoom out(-)", command=self.__zoomOut)
        self.btnMinus.grid(column=3, row=2)

        self.lblDurance = Label(self.frame, text=":")
        self.lblDurance.grid(column=2, row=2)

        self.canvasSpectr = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvasSpectr.grid(column=0, row=3, columnspan=5)

        self.var = StringVar()
        self.comboFurie = ttk.Combobox(self.frame, textvariable=self.var)
        self.comboFurie['values'] = [128, 256, 512, 1024, 2048]
        self.comboFurie.current(2)
        self.comboFurie['state'] = 'readonly'
        self.comboFurie.grid(column=0, row=4)
        self.comboFurie.bind("<<ComboboxSelected>>", self.__changeFurieCount)

        self.__Draw()
        self.__correctButtons()
        self.window.mainloop()

    def __changeFurieCount(self, event):
        self._furieCount = int(self.comboFurie.get())
        self.__Draw()
    def __clickedLoadingOrig(self):
        file = filedialog.askopenfilename(filetypes=[("SoundWave (wav)", ("*.wav"))])
        if (file == ""):
            return False
        self.filename = file
        self.lblChoosedOrig.configure(text=self.filename)
        self.__getData()

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
        self.signal = signal(pointFromBuff(self.content, self.sampwidth))
        self.signal.deleteSilence(self._framerate*100, 700)

        self._timePerImage = 50
        self._frameImage = 4
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._time = (self.signal.getSize()*1000) // self._framerate
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._signalWgt = signalwidget(self._framerate, self.sampwidth, 1024, self._timePerImage, self._frameImage)
        self._signalWgt.setData(self.signal)
        self._from = 0

        self._spectr = spectrofm(self.canvasH, 1, self.canvasH)
    def __Draw(self):
        self.imageOscill = self._signalWgt.getImage(self._from).resize((self.canvasW, self.canvasH))
        draw = ImageDraw.Draw(self.imageOscill)
        #self._framerate * self._timePerImage * self._frameImage <-> self.canvasW
        furrTime = (self._furieCount * self.canvasW) /(self._framerate * self._timePerImage * self._frameImage)
        draw.line([(0, self.canvasH), (furrTime, self.canvasH)], fill="blue", width=1)

        self.photoOscill = ImageTk.PhotoImage(self.imageOscill)
        self.с_imageOscl = self.canvasOscill.create_image(0, 0, anchor='nw', image=self.photoOscill)

        self._spectrData = self.signal.getFutie((self._from)*self._sizeForFrame, (self._from)*self._sizeForFrame+self._furieCount)
        if(len(self._spectrData)!=0):
            self._spectr.setMaxAmpl(max(self._spectrData))
            self._spectr.setData(self._spectrData)
            #self._spectr.drawAverZone([0.02, 0.4, 0.4, 0.18])
            self.imageSpectr = self._spectr.getImage().resize((self.canvasW, self.canvasH))
            self.photoSpectr = ImageTk.PhotoImage(self.imageSpectr)
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