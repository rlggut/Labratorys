#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.1.0

from tkinter import *

import PIL.Image
from PIL import Image, ImageTk
import sys
import os
import math
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
        matrUD=Matrix(3,3)
        matrUD.setData([[1,0,0],
                        [0,0,0],
                        [0,0,-1]])
        matrL=Matrix(3,3)
        matrL.setData([[0,0,0],
                       [1,0,-1],
                       [0,0,0]])
        matrDU=Matrix(3,3)
        matrDU.setData([[0,0,-1],
                        [0,0,0],
                        [1,0,0]])
        tmp=countMatrixGrad(self._image,[matrUD,matrL,matrDU],100)
        print('Кол-во совпадений:',tmp)
        mx=tmp.index(max(tmp))
        mn=tmp.index(min(tmp))
        mid=0+1+2-mx-mn
        if(tmp[mx]-tmp[mid]<0.1*tmp[mx]): tmp[mid]=tmp[mx]
        if(tmp[mid]-tmp[mn]<0.1*tmp[mid]): tmp[mn]=tmp[mid]
        res=[1,1,1]
        res[mid]=math.ceil(tmp[mid]/tmp[mn])
        res[mx]=math.ceil(tmp[mx]/tmp[mn])
        self._matr = res[0] * matrUD + res[1] * matrL + res[2] * matrDU
    def getMatrix(self):
        print('Расчетная матрица:')
        print(self._matr)

filename = "base.jpg"
analizer = imageAnalizer()
analizer.analizeImage(filename)
analizer.getMatrix()
print("End of Work")

