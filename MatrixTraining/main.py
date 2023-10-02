#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.2.1

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

        self._rate = 0.5
    def __str__(self):
        return "[Matrix X]:\n"+str(self._matrX)+"\n\n[Matrix Y]:\n"+str(self._matrY)

    def getRate(self):
        return self._rate
    def cutRate(self,n=2):
        if(n<=0): n = 2
        self._rate /= n
class imageAnalizer():
    def __init__(self, matr=matrixing()):
        self._image = Image.new("RGB", (256, 256), "white")
        self._fileName=""
        self._matr = matr
        self._scale = 100
    def setScale(self, sc):
        self._scale = sc

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
        matrUD.setData([[-1,0,0],
                        [0,0,0],
                        [0,0,1]])
        matrL=Matrix(3,3)
        matrL.setData([[0,0,0],
                       [-1,0,1],
                       [0,0,0]])
        matrDU=Matrix(3,3)
        matrDU.setData([[0,0,1],
                        [0,0,0],
                        [-1,0,0]])
        tmp=countMatrixGrad(self._image,[matrUD,matrL,matrDU],self._scale )
        print('Кол-во совпадений:',tmp)
        mx=tmp.index(max(tmp))
        mn=tmp.index(min(tmp))
        if(mn == mx): mn = 2
        mid=0+1+2-mx-mn
        if(tmp[mx]-tmp[mid]<0.1*tmp[mx]): tmp[mid]=tmp[mx]
        if(tmp[mid]-tmp[mn]<0.1*tmp[mid]): tmp[mn]=tmp[mid]
        res=[1,1,1]
        if(tmp[mn]>0):
            res[mid]=math.ceil(tmp[mid]/tmp[mn])
            res[mx] = math.ceil(tmp[mx] / tmp[mn])
        else:
            res[mid]=0
            res[mx]=0
            res[mn]=0
        addMatr = self._matr.getRate() * (res[0] * matrUD + res[1] * matrL + res[2] * matrDU)
        addMatr.normalizedX()
        #print(addMatr)
        #print("+")
        #print(self._matr._matrX)
        self._matr._matrX = self._matr._matrX + addMatr
        #print("=")
        #print(self._matr._matrX)
        self._matr.cutRate()
    def getMatrix(self):
        print('Расчетная матрица:')
        print(self._matr)


analizer = imageAnalizer()
analizer.setScale(20)
files = os.listdir("pics")
for file in files:
    if(file.count("edge")==0):
        file_pair = "pics/"+(file[:-4]+"_edge.png")
        if(os.path.isfile(file_pair)):
            filename = "pics/"+file
            analizer.analizeImage(filename)
analizer.getMatrix()
print("End of Work")

