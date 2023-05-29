from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os
import re

class imageProc():
    def __init__(self):
        self._image = Image.new("RGB", (256, 256), "white")
        self._imageMos = None
    def setImage(self, filename):
        self._fileName = filename
        self._image = Image.open(filename)
        self._imageMos = None
    def getMosaik(self, n=25, m=25):
        if(not self._imageMos):
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
        return self._imageMos

    def saveMosaik(self, filename=""):
        if(filename==""):
            filename= "Mos_"+self._fileName
        if not(self._imageMos):
            self.getMosaik()
        self._imageMos.save(filename)

proc = imageProc()
proc.setImage("base.jpg")
proc.saveMosaik("baseNw.jpg")
proc.getMosaik(10,10).show()
