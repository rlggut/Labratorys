#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.1.1.

from tkinter import *
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
        self._matrX, self._matrY = Matrix(3, 3), Matrix(3, 3)
        self._matrX.setSobelX()
        self._matrY.setSobelY()

    def setImage(self, filename):
        self._fileName = filename
        self._image = Image.open(filename)
        self._imageMos = None
        self._lastMosN, self._lastMosM = 0, 0
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
        if(n>0 and m>0):
            self.createMosaik(n, m)
            self.__SobelMask()
        if(not self._imageMos):
            self.createMosaik(25, 25)
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

    def __SobelMask(self):
        self._sobelMosaik=maskedImageMatrix(proc.getMosaik(), self._matrX, self._matrY, 100)
    def getSobelMosaik(self):
        if not(self._imageMos):
            self.getMosaik()
        self.__SobelMask()
        return self._sobelMosaik
    def saveSobMosaik(self, filename=""):
        if(filename==""):
            filename= "SobMos_"+self._fileName
        if not(self._imageMos):
            self.getMosaik()
        self._sobelMosaik.save(filename)


proc = imageProc()
proc.setImage("base.jpg")
proc.getMagnifMosaik(2)
proc.saveMosaik("baseNw.jpg")
proc.saveSobMosaik("baseSobNw.jpg")
