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
        self.canvasW = 800
        self.canvasH = 400
        self.window.geometry("800x400")
        self.frame = Frame(self.window)
        self.frame.grid()

        self.filename = "sample.wav"
        self.__getInfo()

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0, rowspan=12)

        self.__Draw()
        self.window.mainloop()

    def __getInfo(self):
        self.wav = wave.open(self.filename, mode="r")
        (self.nchannels, self.sampwidth, self.framerate, self.nframes, comptype, compname) = self.wav.getparams()
        print(self.nchannels, self.sampwidth, self.framerate, self.nframes)

    def __Draw(self):
        sizeY=1024
        step=1
        content = self.wav.readframes(min(3*self.framerate,self.nframes))
        samples = pointFromBuff(content, self.sampwidth)
        image1 = Image.new("RGB", (len(samples)//step, sizeY), "white")
        draw = ImageDraw.Draw(image1)
        maxAmp=2**(self.sampwidth*8-1)
        lastY=sizeY//2
        t=1
        for i in range(0,len(samples),step):
            posY = samples[i]
            #print(samples[i],content[2*i],content[2*i+1])
            posY = (posY*(sizeY//2))//maxAmp
            draw.line([(t-1, lastY), (t, -posY + sizeY//2)], fill =128,width=1)
            lastY = -posY + (sizeY//2)
            t += 1
        self.image = image1.resize((self.canvasW, self.canvasH))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        image1.save("res.png")
app=App()