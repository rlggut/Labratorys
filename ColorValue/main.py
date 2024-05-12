from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))
from Matrix import *
from ImageProcess import *
import re

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Исследование градаций серого")
        self.canvasW = 300
        self.canvasH = 200
        size=str(int(self.canvasW*3.1))+"x"+str(int(self.canvasH *1.25))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.image = Image.new('RGB', (self.canvasW, self.canvasH), (240,240,240))
        self.photo = ImageTk.PhotoImage(self.image)

        self.lblLoad = Label(self.frame, text="Выберите изображение")
        self.lblLoad.grid(column=0, row=0)
        self.btnLoad = Button(self.frame, text="...", command=self.__clickedLoading)
        self.btnLoad.grid(column=2, row=0)
        self.lblChoosed = Label(self.frame, text="*.(png/jpg)")
        self.lblChoosed.grid(column=4, row=0, columnspan=3)
        self.filename = ""

        self.canvas = Canvas(self.window, height=1.1*self.canvasH, width=3 * self.canvasW+3)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(column=0, row=1,columnspan=5)

        self.window.mainloop()

    def __clickedLoading(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        if(file==""):
            return False
        self.filename = file
        self.image = Image.open(file)
        self.image.load()
        pattern = '[^\/]+\.\D+'
        file = re.search(pattern,file).group(0)
        self.lblChoosed.configure(text=file)
        factorW = self.canvasW / self.image.width
        factorH = self.canvasH / self.image.height
        factor=min(factorW, factorH)
        self.image=self.image.resize((int(factor*self.image.width), int(factor*self.image.height)))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        self.imageGrey = self.__getGrey()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.с_imageGrey = self.canvas.create_image(self.canvasW+1, 0, anchor='nw', image=self.photoGrey)

        self.imageGreyExp = self.__getGreyOwn()
        self.photoGreyExp = ImageTk.PhotoImage(self.imageGreyExp)
        self.с_imageGreyExp = self.canvas.create_image(2*self.canvasW+2, 0, anchor='nw', image=self.photoGreyExp)
    def __getGrey(self):
        res = self.image.convert("L")
        return res
    def __FsRGB(self, value):
        return int(value[0]*0.2126+value[1]*0.7152+value[2]*0.0722)
    def __funcGreen(self, value, color=[89,142,86]):
        m1=max(color[0],255-color[0])
        m2=max(color[1],255-color[1])
        m3=max(color[2],255-color[2])
        return int((abs(value[0]-color[0])*255)/m1*0.21+(abs(value[1]-color[1])*255)/m2*0.71
                   +(abs(value[2]-color[2])*255)/m3*0.08)
    def __getGreyOwn(self):
        res = Image.new('RGB', (self.image.width, self.image.height), (0,0,0))
        for y in range(self.image.height):
            for x in range(self.image.width):
                value = self.image.getpixel((x,y))
                greyCol = self.__funcGreen(value)
                res.putpixel((x,y), (greyCol,greyCol,greyCol))
        return res

app=App()