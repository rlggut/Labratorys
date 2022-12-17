from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import pyautogui

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking picture")
        self.canvasW = 600
        self.canvasH = 400
        size=""+str(int(self.canvasW*2.1))+"x"+str(int(self.canvasH *1.1))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.imageScreen = Image.new('RGB', (self.canvasW, self.canvasH), (240,240,240))
        self.screen = ImageTk.PhotoImage(self.imageScreen)

        self.imageSelect = Image.new('RGB', (self.canvasW, self.canvasH), (240,255,240))
        self.select = ImageTk.PhotoImage(self.imageSelect)

        self.btnScreen = Button(self.frame, text="Take a pic", command=self.__TakePic)
        self.btnScreen.grid(column=0, row=0, padx=10)

        self.canvasScreen = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageScreen = self.canvasScreen.create_image(0, 0, anchor='nw', image=self.screen)
        self.canvasScreen.grid(column=0, row=1,rowspan=2)
        self.zone = self.canvasScreen.create_rectangle(0, 0, 0, 0, activefill='lightgreen', width=5)

        self.canvasSelect = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageSelect = self.canvasSelect.create_image(0, 0, anchor='nw', image=self.select)
        self.canvasSelect.grid(column=1, row=1, rowspan=2)

        self.window.bind('<ButtonPress>', self.__mousePressEvent)
        self.window.bind('<ButtonRelease>', self.__mouseReleaseEvent)
        self.window.bind('<Motion>', self.__mouseMoving)

        self.firstX=0
        self.firstY=0
        self.lastButton=0

        self.window.mainloop()
    def __mouseMoving(self, event):
        if(self.lastButton==1):
            self.canvasScreen.delete(self.zone)
            fx=min(self.firstX,event.x)
            sx=max(self.firstX,event.x)
            fy=min(self.firstY,event.y)
            sy=max(self.firstY,event.y)
            self.zone=self.canvasScreen.create_rectangle(fx, fy, sx, sy, activeoutline='lightgreen', width=1)
    def __mousePressEvent(self, event):
        self.lastButton=event.num
        if(event.num==1):
            self.firstX = event.x
            self.firstY = event.y
    def __mouseReleaseEvent(self, event):
        self.lastButton=0
        if(event.num==1):
            dx=abs(self.firstX - event.x)
            dy=abs(self.firstY - event.y)
            if(dx+dy>pow(self.canvasW//100,2)):
                fx = min(self.firstX, event.x)
                sx = max(self.firstX, event.x)
                fy = min(self.firstY, event.y)
                sy = max(self.firstY, event.y)
                crops = self.imageScreen.crop((fx, fy, sx, sy))
                self.canvasScreen.delete(self.zone)
                factorW = self.canvasW / crops.width
                factorH = self.canvasH / crops.height
                factor = min(factorW, factorH)
                self.imageSelect = crops.resize((int(factor * crops.width), int(factor * crops.height)))
                self.select = ImageTk.PhotoImage(self.imageSelect)
                self.с_imageSelect = self.canvasSelect.create_image(0, 0, anchor='nw', image=self.select)

    def __TakePic(self):
        screen = pyautogui.screenshot('screenshot.png')
        self.imageScreen = Image.open('screenshot.png')
        self.imageScreen.load()
        factorW = self.canvasW / self.imageScreen.width
        factorH = self.canvasH / self.imageScreen.height
        factor=min(factorW, factorH)
        self.imageScreen=self.imageScreen.resize((int(factor*self.imageScreen.width), int(factor*self.imageScreen.height)))
        self.screen = ImageTk.PhotoImage(self.imageScreen)
        self.с_imageScreen = self.canvasScreen.create_image(0, 0, anchor='nw', image=self.screen)


app=App()