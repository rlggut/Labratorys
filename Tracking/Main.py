from tkinter import *
from PIL import Image, ImageTk
import threading
import time
import pyautogui
import os

def FindingImage(orig, image):
    if not(isinstance(orig, Image.Image)):
        return False
    if not(isinstance(image, Image.Image)):
        return False
    if(orig.width<image.width):
        return False
    if(orig.height<image.height):
        return False
    y=0
    x=0
    flag=True
    while(flag):
        i=0
        j=0
        lastx=x
        lasty=y
        while(orig.getpixel((x,y))==image.getpixel((i,j))):
            x=x+1
            if(x==orig.width):
                x=0
                y=y+1
            i=i+1
            if(i==image.width):
                i=0
                j=j+1
                x=lastx
                y=y+1
            if(y==orig.height):
                break
            if(j==image.height):
                break
        if(j==image.height):
            return str(x)+'x'+str(y)
        else:
            x=lastx+1
            y=lasty
            if((orig.width-x)<image.width):
                x=0
                y=lasty+1
        if(y==orig.height):
            flag=False
    return "X"

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
        self.lblFinding = Label(self.frame, text="Nothing to find")
        self.lblFinding.grid(column=2, row=0)

        self.canvasScreen = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageScreen = self.canvasScreen.create_image(0, 0, anchor='nw', image=self.screen)
        self.canvasScreen.grid(column=0, row=1,rowspan=2,columnspan=2)
        self.zone = self.canvasScreen.create_rectangle(0, 0, 0, 0, activefill='lightgreen', width=5)

        self.canvasSelect = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageSelect = self.canvasSelect.create_image(0, 0, anchor='nw', image=self.select)
        self.canvasSelect.grid(column=2, row=1, rowspan=2)

        self.window.bind('<ButtonPress>', self.__mousePressEvent)
        self.window.bind('<ButtonRelease>', self.__mouseReleaseEvent)
        self.window.bind('<Motion>', self.__mouseMoving)

        self.firstX=0
        self.firstY=0
        self.lastButton=0
        self.ready=False
        self.reading=False

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
        self.ready=False
        if(event.num==1):
            self.firstX = event.x
            self.firstY = event.y
    def __mouseReleaseEvent(self, event):
        self.lastButton=0
        if(event.num==1):
            dx=abs(self.firstX - event.x)
            dy=abs(self.firstY - event.y)
            if(dx*dy==0):
                return
            fx = min(self.firstX, event.x)
            sx = max(self.firstX, event.x)
            fy = min(self.firstY, event.y)
            sy = max(self.firstY, event.y)
            factorW = self.canvasW / self.imageOrig.width
            factorH = self.canvasH / self.imageOrig.height
            factor=min(factorW, factorH)
            self.selectOrig = self.imageScreen.crop((int(fx*factor), int(fy*factor),
                                                     int(sx*factor), int(sy*factor)))

            self.select = self.imageScreen.crop((fx, fy, sx, sy))
            self.canvasScreen.delete(self.zone)
            factorW = self.canvasW / self.select.width
            factorH = self.canvasH / self.select.height
            factor = min(factorW, factorH)
            self.imageSelect = self.select.resize((int(factor * self.select.width),
                                                       int(factor * self.select.height)))
            self.select = ImageTk.PhotoImage(self.imageSelect)
            self.с_imageSelect = self.canvasSelect.create_image(0, 0, anchor='nw', image=self.select)
            self.ready=True

            self.threadFinding = threading.Thread(target=self.__Finding, args=())
            self.threadFinding.start()

    def __Finding(self):
        while(self.ready):
            time.sleep(0.2)
            if(not self.ready):
                break
            self.lblFinding['text']='Calculated'
            res=(FindingImage(self.imageOrig, self.selectOrig))
            if(res=='X'):
                self.lblFinding['text']='Not found'
            else:
                self.lblFinding['text']='Found at '+res
            self.__TakePic()

    def __TakePic(self):
        if(not self.reading):
            self.reading=True
            screen = pyautogui.screenshot('screenshot.png')
            self.imageOrig = Image.open('screenshot.png')
            factorW = self.canvasW / self.imageOrig.width
            factorH = self.canvasH / self.imageOrig.height
            factor=min(factorW, factorH)
            self.imageScreen=self.imageOrig.resize((int(factor*self.imageOrig.width), int(factor*self.imageOrig.height)))
            self.screen = ImageTk.PhotoImage(self.imageScreen)
            self.с_imageScreen = self.canvasScreen.create_image(0, 0, anchor='nw', image=self.screen)
            self.reading=False
            os.remove('screenshot.png')


app=App()