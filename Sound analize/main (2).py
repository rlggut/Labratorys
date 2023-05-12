from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import wave
from SignalWidget import *
from SpectrForm import *
from Signals import *
from soundCommon import *
from Spectr2D import *
import time
import threading

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 1200
        self.canvasH = 200
        self.researchDelta=100
        self._furieCount = 512
        self._silenceEdge = 700
        self.imageSptr2D=None
        self.spectrReady=False
        self.oscillReady = False
        self._lastTimeLine = None
        self._reload = False
        self.window.geometry("1200x500")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.signal = signal()
        self.__getData()

        self.btnFileOrig = Button(self.frame, text="Выбрать файл", command=self.__clickedLoadingOrig)
        self.btnFileOrig.grid(column=0, row=0)
        self.lblChoosedOrig = Label(self.frame, text=self.filename)
        self.lblChoosedOrig.grid(column=1, row=0, columnspan=4)
        self.lblSilence = Label(self.frame, text="Порог тишины")
        self.lblSilence.grid(column=5, row=0)
        self.silenceSpin = Spinbox(self.frame, from_ =0, to = 1000, increment=10, width=5, command=self.__SilenceEdge, state=DISABLED)
        self.silenceSpin.grid(column=6, row=0)
        self.silenceSpin.delete(0, len(self.silenceSpin.get()))
        self.silenceSpin.insert(0, str(self._silenceEdge))

        self.canvasOscill = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvasOscill.grid(column=0, row=1, columnspan=14)

        self.btnLeft = Button(self.frame, text="<-", command=self.__moveOscillLeft, state=DISABLED)
        self.btnLeft.bind("<Left>", self.__moveOscillLeft)
        self.btnLeft.grid(column=0, row=2)
        self.btnRight = Button(self.frame, text="->", command=self.__moveOscillRight, state=DISABLED)
        self.btnRight.bind("<Right>", self.__moveOscillRight)
        self.btnRight.grid(column=6, row=2)

        self.btnPlus = Button(self.frame, text="Zoom in(+)", command=self.__zoomIn, state=DISABLED)
        self.btnPlus.grid(column=1, row=2)
        self.btnMinus = Button(self.frame, text="Zoom out(-)", command=self.__zoomOut, state=DISABLED)
        self.btnMinus.grid(column=5, row=2)

        self.lblDurance = Label(self.frame, text=":")
        self.lblDurance.grid(column=2, row=2, columnspan=3)

        self.canvasSpectr = Canvas(self.frame, height=self.canvasH, width=self.canvasW//2, bg='white')
        self.canvasSpectr.grid(column=0, row=3, columnspan=7)

        self.canvasSptr2D = Canvas(self.frame, height=self.canvasH, width=self.canvasW//2, bg='white')
        self.canvasSptr2D.grid(column=7, row=3, columnspan=7)

        self.lblComboFurie = Label(self.frame, text="Элементов Фурье")
        self.lblComboFurie.grid(column=0, row=4)
        self.var = StringVar()
        self.comboFurie = ttk.Combobox(self.frame, textvariable=self.var)
        self.comboFurie['values'] = [128, 256, 512, 1024, 2048]
        self.comboFurie.current(2)
        self.comboFurie['state'] = 'readonly'
        self.comboFurie.grid(column=1, row=4)
        self.comboFurie.bind("<<ComboboxSelected>>", self.__changeFurieCount)

        self.__Draw()
        self.window.mainloop()
    def __SilenceEdge(self):
        self._silenceEdge = int(self.silenceSpin.get())
        self.__getData()
    def __changeFurieCount(self, event):
        self._furieCount = int(self.comboFurie.get())
        self.__Draw()
    def __clickedLoadingOrig(self):
        file = filedialog.askopenfilename(filetypes=[("SoundWave (wav)", ("*.wav"))])
        if (file == ""):
            return False
        self.filename = file
        if(len(file)>40):
            file=file[0:20]+'...'+file[-20:]
        self.lblChoosedOrig.configure(text=file)
        self._reload=True
        self.sptr2D.stopWork()
        self._signalWgt.stopWork()
        while(not self.spectrReady or not self.oscillReady):
            time.sleep(0.03)
        self.spectrReady=False
        self.oscillReady=False
        self._reload = False
        self.__blockButtons()
        self.__getData()
        self.__Draw()

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
    def __blockButtons(self):
        self.btnMinus['state'] = 'disabled'
        self.btnPlus['state'] = 'disabled'
        self.btnRight['state'] = 'disabled'
        self.btnLeft['state'] = 'disabled'
        self.silenceSpin['state'] = 'disabled'
    def __correctButtons(self):
        if (self._numsOfFrames < 2*self._frameImage):
            self.btnMinus['state'] = 'disabled'
        else:
            self.btnMinus['state'] = 'normal'
        if (self._frameImage == 1):
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
    def __moveOscillLeft(self, event=None):
        self._from=max(self._from-1,0)
        self.__correctButtons()
        self.__Draw()
    def __moveOscillRight(self, event=None):
        self._from = min(self._from + 1, self._numsOfFrames-self._frameImage)
        self.__correctButtons()
        self.__Draw()
    def __getData(self):
        self.wav = wave.open(self.filename, mode="r")
        (self._nchannels, self._sampwidth, self._framerate, self._nframes, comptype, compname) = self.wav.getparams()
        self.content = self.wav.readframes(self._nframes*self._nchannels)
        self.signal = signal(chooseChannel(pointFromBuff(self.content, self._sampwidth),self._nchannels,1))
        self.signal.deleteSilence(self._framerate*100, self._silenceEdge)

        self._thrSpectr2d = threading.Thread(target=self.__ThreadSpectr2d)
        self._thrSpectr2d.start()

        self._timePerImage = 50
        self._frameImage = 4
        self._sizeForFrame = ((self._timePerImage * self._framerate) // 1000)
        self._time = (self.signal.getSize()*1000) // self._framerate
        self._numsOfFrames = math.ceil(self._time // self._timePerImage)
        self._from = 0
        #self.__ThreadOscill()
        self._thrOscill = threading.Thread(target=self.__ThreadOscill)
        self._thrOscill.start()
        self._spectr = spectrofm(self.canvasH, self._sampwidth, self.canvasH)

    def __ThreadOscill(self):
        self.oscillReady = False
        self._signalWgt = signalwidget(self._framerate, self._sampwidth, 1024, self._timePerImage, self._frameImage)
        self._signalWgt.setData(self.signal)
        if(not self._reload):
            self.imageOscill = self._signalWgt.getImage(0).resize((self.canvasW, self.canvasH))
            draw = ImageDraw.Draw(self.imageOscill)
            furrTime = (self._furieCount * self.canvasW) / (self._framerate * self._timePerImage * self._frameImage)
            draw.line([(0, self.canvasH), (furrTime, self.canvasH)], fill="blue", width=1)
            del draw
            self.photoOscill = ImageTk.PhotoImage(self.imageOscill)
            self.с_imageOscl = self.canvasOscill.create_image(0, 0, anchor='nw', image=self.photoOscill)
            self.__correctButtons()
            self.silenceSpin['state'] = 'normal'
        self.oscillReady=True

    def __ThreadSpectr2d(self):
        self.sptr2D = spectr2D(self._framerate)
        self.sptr2D.setData(self.signal.getData())
        if(not self._reload):
            image = self.sptr2D.getImage()
            self._kfSpctr2D = (self.canvasW // 2) / image.width
            self.imageSptr2D = image.resize((self.canvasW // 2, self.canvasH))
            self.photoSptr2D = ImageTk.PhotoImage(self.imageSptr2D)
            self.с_imageSptr2D = self.canvasSptr2D.create_image(0, 0, anchor='nw', image=self.photoSptr2D)
        self.spectrReady=True

    def __Draw(self):
        if(self.spectrReady):
            timeLine=int(((self._from*self._sizeForFrame*self._kfSpctr2D)/self.sptr2D.getStep())*self.sptr2D.getLineWidth())+1
            if(self._lastTimeLine):
                self.canvasSptr2D.delete(self._lastTimeLine)
            self._lastTimeLine = self.canvasSptr2D.create_line((timeLine,0),(timeLine,self.canvasH),fill="red",width=self.sptr2D.getLineWidth())
        if(self.oscillReady):
            self.imageOscill = self._signalWgt.getImage(self._from).resize((self.canvasW, self.canvasH))
            draw = ImageDraw.Draw(self.imageOscill)
            #self._framerate * self._timePerImage * self._frameImage <-> self.canvasW
            furrTime = (self._furieCount * self.canvasW) /(self._framerate * self._timePerImage * self._frameImage)
            draw.line([(0, self.canvasH), (furrTime, self.canvasH)], fill="blue", width=1)
            del draw
            self.photoOscill = ImageTk.PhotoImage(self.imageOscill)
            self.с_imageOscl = self.canvasOscill.create_image(0, 0, anchor='nw', image=self.photoOscill)

        self._spectrData = self.signal.getFutie((self._from)*self._sizeForFrame, (self._from)*self._sizeForFrame+self._furieCount)
        if(len(self._spectrData)!=0):
            self._spectr.setMaxAmpl(max(self._spectrData))
            self._spectr.setData(self._spectrData)
            #self._spectr.drawAverZone([0.02, 0.4, 0.4, 0.18])
            self.imageSpectr = self._spectr.getImage().resize((self.canvasW//2, self.canvasH))
        else:
            self.imageSpectr = Image.new("RGB", (self.canvasW//2, self.canvasH), "white")
            draw_text = ImageDraw.Draw(self.imageSpectr)
            fnt = ImageFont.truetype("arial.ttf", self.imageSpectr.height//2)
            draw_text.text((self.imageSpectr.width//4,self.imageSpectr.height//4), 'NO DATA',font=fnt, fill=('#1C0606') )
            del draw_text
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