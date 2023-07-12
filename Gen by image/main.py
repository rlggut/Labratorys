#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.1.3.6

from tkinter import *

import PIL.Image
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..')) #path to https://github.com/rlggut/Labratorys
from Matrix import *
from ImageProcess import *
class imageProc():
    def __init__(self):
        self._image = Image.new("RGB", (256, 256), "white")
        self._imageMos = None
        self._waveImage = None
        self._smoothed = False
        self._fileName=""

    def setImage(self, file, newFileName=""):
        self._imageMos = None
        self._waveImage = None
        self._smoothed = False
        if(isinstance(file,str)):
            self._image = Image.open(file)
            self._fileName = file
        elif(isinstance(file,PIL.Image.Image)):
            self._image=file.copy()
            if(newFileName==""):
                if(self._fileName==""): self._fileName="newPic.png"
            else: self._fileName=newFileName
        self._imageMos = None
        self._waveImage = None
        self._lastMosN, self._lastMosM = 0, 0
    def makeSmoothMain(self, time=1):
        for i in range(time):
            self._image = makeGaussSmooth(self._image)
        self._smoothed = True
    def wasMainSmooth(self):
        return self._smoothed
    def saveSmoothMain(self, time=1):
        filename= "Smooth_"+self._fileName
        if(not self._smoothed):
            self.makeSmoothMain(time)
        self._image.save(filename)
    def createMosaik(self, n=25, m=25):
        if(n<0): n=1
        if(m<0): m=1
        if(n!=self._lastMosN or m!=self._lastMosM):
            self._imageMos = Image.new("RGB", (self._image.width, self._image.height), "white")
            dx = self._image.width // n
            dy = self._image.height // m
            for y in range(m):
                for x in range(n):
                    r, g, b = 0, 0, 0
                    for addx in range(dx):
                        for addy in range(dy):
                            p = self._image.getpixel((x * dx + addx, y * dy + addy))
                            r += (p[0] / (dx * dy))
                            g += (p[1] / (dx * dy))
                            b += (p[2] / (dx * dy))
                    for addx in range(dx):
                        for addy in range(dy):
                            self._imageMos.putpixel((x * dx + addx, y * dy + addy), (int(r), int(g), int(b)))
            self._lastMosN, self._lastMosM = n, m
    def getMosaik(self, n=-1, m=-1):
        if(n<0 or m<0):
            n, m = 25, 25
        self.createMosaik(n, m)
        self.__SobelMask()
        return self._imageMos
    def getMagnifMosaik(self, block=-1):
        block=int(block)
        if(block<=0):
            return self.getMosaik()
        return self.getMosaik(self._image.width//block,self._image.height//block)

    def saveMosaik(self, filename=""):
        if(filename==""):
            filename= "Mos_"+self._fileName
        if not(self._imageMos):
            self.getMosaik()
        self._imageMos.save(filename)

    def __delGlitch(self):
        self._sobelMosaik=delBorderGlitch(self._sobelMosaik, 3, 5)
    def __SobelMask(self):
        if(not self._imageMos):
            self.createMosaik()
        self._sobelMosaik=maskedImageMatrix(self._imageMos, getSobelMatrX(), getSobelMatrY(), 70)
        self.__delGlitch()
    def getSobelMosaik(self):
        if not(self._imageMos):
            self.getMosaik()
        self.__SobelMask()
        return self._sobelMosaik
    def saveSobMosaik(self, filename=""):
        if(filename==""):
            filename= "SobMos_"+self._fileName
        if not(self._sobelMosaik):
            self.getSobelMosaik()
        self._sobelMosaik.save(filename)
    def __comparePix(self,x,y,tx,ty,deg=80):
        col1=self._waveImage.getpixel((x,y))
        col2=self._image.getpixel((tx,ty))
        if(col1==(255,255,255) or col2==(255,255,255)):
            return False
        proc=0
        for i in range(3): proc+=abs(col1[i]-col2[i])
        return (proc<deg)

    def __waveMosaik(self, deg=10):
        self._waveImage = self._image.copy()
        white=(255,255,255)
        images=[]
        for y in range(self._waveImage.height):
            for x in range(self._waveImage.width):
                if(self._waveImage.getpixel((x,y))!=white):
                    upper,down,left,right=y,y,x,x
                    st=[]
                    st.append([x,y])
                    pixels=[]
                    self._waveImage.putpixel((x, y), white)
                    while(len(st)>0):
                        point = st.pop()
                        tx, ty = point[0], point[1]
                        upper, down = min(upper, ty), max(down, ty)
                        left, right = min(left, tx), max(right, tx)
                        pixels.append([tx, ty])
                        if(tx>0):
                            if(self.__comparePix(tx-1,ty,tx,ty,deg)):
                                st.append([tx-1, ty])
                                self._waveImage.putpixel((tx-1, ty), white)
                        if(ty>0):
                            if(self.__comparePix(tx,ty-1,tx,ty,deg)):
                                st.append([tx, ty-1])
                                self._waveImage.putpixel((tx, ty-1), white)
                        if(tx+1<self._waveImage.width):
                            if(self.__comparePix(tx+1,ty,tx,ty,deg)):
                                st.append([tx+1, ty])
                                self._waveImage.putpixel((tx+1, ty), white)
                        if(ty+1<self._waveImage.height):
                            if(self.__comparePix(tx,ty+1,tx,ty,deg)):
                                st.append([tx, ty+1])
                                self._waveImage.putpixel((tx, ty+1), white)
                    r, g, b = 0, 0, 0
                    n=len(pixels)
                    for i in range(n):
                        p = self._image.getpixel((pixels[i][0], pixels[i][1]))
                        r += (p[0] / n)
                        g += (p[1] / n)
                        b += (p[2] / n)
                    image = Image.new("RGB", (right - left + 1, down - upper + 1), "white")
                    for i in range(n):
                        image.putpixel((pixels[i][0] - left, pixels[i][1] - upper),(int(r),int(g),int(b)))
                    images.append([image,left,upper,n])
        image = Image.new("RGB", (self._waveImage.width, self._waveImage.height), "white")
        print("Количество областей в волновом алгоритме: ",len(images))
        for i in range(len(images)):
            im = images[i][0]
            x, y = images[i][1], images[i][2]
            n, m = im.height, im.width
            for ty in range(n):
                for tx in range(m):
                    if(image.getpixel((tx+x,ty+y))==(255,255,255)):
                        image.putpixel((tx+x,ty+y),im.getpixel((tx,ty)))
        self._waveImage = image.copy()
    def getWaveMosaik(self, newer=False):
        if(not self._waveImage or newer):
            self.__waveMosaik()
        return self._waveImage
    def saveWaveMosaik(self, filename=""):
        if(filename==""):
            filename= "WaveMos_"+self._fileName
        if not(self._waveImage):
            self.getWaveMosaik()
        self._waveImage.save(filename)
    def smoothWaveMosaik(self, time=1):
        for i in range(time):
            self._waveImage = makeGaussSmooth(self._waveImage)
    def getSmoothWaving(self, time=1):
        self.smoothWaveMosaik(time)
        return self._waveImage

filename = "base.jpg"
#filename = "Apple.png"
proc = imageProc()
proc.setImage(filename)
proc.makeSmoothMain(2)
proc.saveSmoothMain()
proc.getMagnifMosaik(2)
proc.saveMosaik()
proc.saveSobMosaik()
proc.saveWaveMosaik()
proc.smoothWaveMosaik(2)
'''proc.setImage(proc.getWaveMosaik())
proc.getWaveMosaik(True).show()'''