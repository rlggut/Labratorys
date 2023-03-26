from tkinter import *
import wave
from PIL import Image, ImageDraw, ImageTk

def pointFromBuff(buff, sampwidth):
    points=[]
    minusBit=(2**(8*sampwidth-1))
    for i in range(0,len(buff)-sampwidth,sampwidth):
        pt=0
        pt=buff[i+1]*256+buff[i]
        if(pt>minusBit):
            pt=-(2*minusBit-pt)
        points.append(pt)
    return(points)

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 1000
        self.canvasH = 400
        self.researchTime = 3
        self.researchDelta=100
        self.window.geometry("1000x400")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.__getData()

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0, rowspan=12)

        self.__Draw()
        self.window.mainloop()

    def __getData(self):
        self.wav = wave.open(self.filename, mode="r")
        (self.nchannels, self.sampwidth, self.framerate, self.nframes, comptype, compname) = self.wav.getparams()
        self.content = self.wav.readframes(min(self.researchTime * self.framerate, self.nframes))
        self.samples = pointFromBuff(self.content, self.sampwidth)
        self.__deleteSilence()
    def __deleteSilence(self):
        pointForResearch = self.researchDelta * self.framerate // 1000
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
        sizeY=1024
        step=1

        image1 = Image.new("RGB", (len(self.samples)//step, sizeY), "white")
        draw = ImageDraw.Draw(image1)

        draw.line([(0, sizeY//2), (len(self.samples)//step, sizeY // 2)], fill="green", width=1)
        ind=1
        while(ind*self.framerate<len(self.samples)):
            draw.line([(ind*self.framerate, sizeY-sizeY//8), (ind*self.framerate, sizeY)], fill="blue", width=16)
            ind += 1

        maxAmp=2**(self.sampwidth*8-1)
        lastY=sizeY//2
        t=1
        for i in range(0,len(self.samples),step):
            posY = self.samples[i]
            posY = (posY*(sizeY//2))//maxAmp
            draw.line([(t-1, lastY), (t, -posY + sizeY//2)], fill =128,width=1)
            lastY = -posY + (sizeY//2)
            t += 1
        self.image = image1.resize((self.canvasW, self.canvasH))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        image1.save("res.png")

app=App()