#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.0.1

from tkinter import *

import PIL.Image
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..')) #path to https://github.com/rlggut/Labratorys
from Matrix import *
from ImageProcess import *

class matrixing():
    def __init__(self):
        self._matrX = Matrix()
        self._matrX.setSobelX()
        self._matrY = Matrix()
        self._matrY.setSobelY()

        self._rate = 1
    def __str__(self):
        return "[Matrix X]:\n"+str(self._matrX)+"\n\n[Matrix Y]:\n"+str(self._matrY)
class imageAnalizer():
    def __init__(self, matr=matrixing()):
        self._image = Image.new("RGB", (256, 256), "white")
        self._fileName=""
        self._matr = matr

    def analizeImage(self, file, newFileName=""):
        if(isinstance(file,str)):
            self._image = Image.open(file)
            self._fileName = file
        elif(isinstance(file,PIL.Image.Image)):
            self._image=file.copy()
            if(newFileName==""):
                if(self._fileName==""): self._fileName="newPic.png"
            else: self._fileName=newFileName
    def getMatrix(self):
        print(self._matr)

filename = "base.jpg"
analizer = imageAnalizer()
analizer.analizeImage(filename)
analizer.getMatrix()

print("End of Work")

