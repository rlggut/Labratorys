#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.3.1

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
        self._matrX = getPrewittMatrX()
        self._matrY = getPrewittMatrY()
        self._rate = 2
    def __str__(self):
        return "[Matrix X]:\n"+str(self._matrX)+"\n\n[Matrix Y]:\n"+str(self._matrY)

    def getRate(self):
        return self._rate
    def cutRate(self,n=2):
        if(n<=0): n = 2
        self._rate /= n
    def getMatrX(self):
        return self._matrX
    def getMatrY(self):
        return self._matrY

class imageAnalizer():
    def __init__(self, matr=matrixing()):
        self._image = Image.new("RGB", (256, 256), "white")
        self._pathImages=""
        self._fileName=""
        self._matr = matr
        self._scale = 100
        self._needLog = True
    def setNeedLog(self, log=True):
        self._needLog = log
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
        #Подсчет для направления по оси X
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
        self._image = self._image.convert("L")
        tmpX=countMatrixGrad(self._image,[matrUD,matrL,matrDU],self._scale)
        if(self._needLog): print('Кол-во совпадений векторов градиента по X: ', tmpX)

        # Подсчет для направления по оси Y
        matrU=Matrix(3,3)
        matrU.setData([[0,-1,0],
                       [0,0,0],
                       [0,1,0]])
        matrRL=Matrix(3,3)
        matrRL.setData([[0,0,-1],
                        [0,0,0],
                        [1,0,0]])
        self._image = self._image.convert("L")
        tmpY=countMatrixGrad(self._image,[matrUD,matrU,matrRL],self._scale)
        if(self._needLog): print('Кол-во совпадений векторов градиента по Y: ',tmpY)
        # Усреднение, чтобы матрицы были эквивалентными
        tmp = []
        for i in range(3):
            tmp.append((tmpX[i] + tmpY[i]) / 2)

        mx=tmp.index(max(tmp))
        mn=tmp.index(min(tmp))
        if(mn == mx): mn = 2
        mid=0+1+2-mx-mn
        if(tmp[mx]-tmp[mid]<0.1*tmp[mx]): tmp[mid]=tmp[mx]
        if(tmp[mid]-tmp[mn]<0.1*tmp[mid]): tmp[mn]=tmp[mid]
        res=[1,1,1]
        if(tmp[mn]>0):
            minDt = 10
            res[mid] = math.ceil(tmp[mid] / tmp[mn])
            res[mx] = math.ceil(tmp[mx] / tmp[mn])
            for i in range(1,10):
                for j in range(i,10):
                    for k in range(j,10):
                        dt = abs(j/i - tmp[mid]/tmp[mn])
                        dt += abs(k/i - tmp[mx]/tmp[mn])
                        if(dt<minDt):
                            res[mn] = i
                            res[mid] = j
                            res[mx] = k
                            minDt = dt
        else:
            res[mid]=0
            res[mx]=0
            res[mn]=0
        if(self._needLog): print('Усредненные коэффициенты по градиентам: ', res)

        mx = max(res)
        for i in range(len(res)):
            res[i] = res[i]/mx
        self._addMatrX = (res[0] * matrUD + res[1] * matrL + res[2] * matrDU)
        #self._addMatrX.normalizedX()
        self._addMatrY = (res[0] * matrUD + res[1] * matrU + res[2] * matrRL)
        #self._addMatrY.normalizedY()

    def setImagePath(self, path="pics"):
        self._pathImages = path
        self._trainingImages = []
        self._comparedImages = []
        if not(os.path.isdir(path)):
            return
        files = os.listdir(path)
        for file in files:
            if (file.count("edge") == 0):
                file_pair = "pics/" + (file[:-4] + "_edge.png")
                if (os.path.isfile(file_pair)):
                    filename = "pics/" + file
                    self._trainingImages.append(filename)
                    self._comparedImages.append(file_pair)
    def trainFromPath(self, path=-1):
        if(path==-1):
            if(self._pathImages==""):
                self.setImagePath()
        else:
            if(isinstance(path, str)):
                self.setImagePath(path)
            else:
                if (self._pathImages == ""):
                    self.setImagePath()
        minDt = self.comparedAll()
        if (self._needLog): print("Расчетное базовое отклонение: " + str(minDt))
        for image in self._trainingImages:
            if (self._needLog):
                print("Следующее изображение: ", image)
            self.analizeImage(image)
            kf = self._matr.getRate()
            step = 0
            self.getMatrix()
            while(step<4):
                matrX = self._matr._matrX + kf * self._addMatrX
                matrY = self._matr._matrY + kf * self._addMatrY
                if (self._needLog):
                    print("Добавочная матрица по оси Y")
                    print(kf * self._addMatrY)
                dt = self.comparedAll(matrX,matrY)
                if(dt>minDt):
                    kf = kf/2
                    matrX = self._matr._matrX + kf * self._addMatrX
                    matrY = self._matr._matrY + kf * self._addMatrY
                else:
                    minDt=dt
                    if(self._needLog): print("Обновление минимального отклонения: "+str(minDt))
                    self._matr._matrX = self._matr._matrX + kf * self._addMatrX
                    self._matr._matrY = self._matr._matrY + kf * self._addMatrY
                    break
                step+=1

    def comparedAll(self,matrX="",matrY=""):
        if (isinstance(matrX, str)):
            matrX=self._matr._matrX
        if (isinstance(matrY, str)):
            matrY=self._matr._matrY
        dt=0
        for i in range(len(self._trainingImages)):
            fileIM = Image.open(self._trainingImages[i])
            fileIM = maskedImageMatrix(fileIM, matrX, matrY, 100)
            fileIM.save(self._trainingImages[i][:-4] + "_edgeNW.png")
            fileComp = Image.open(self._comparedImages[i])
            add = compareImage(fileIM, fileComp)
            dt = dt + add
            if(self._needLog): print("Разница для изображения " + self._trainingImages[i] + " = " + str(add))
        return dt
    def getMatrix(self):
        print('Расчетные матрицы:')
        print(self._matr)
    def getMatrX(self):
        return self._matr.getMatrX()
    def getMatrY(self):
        return self._matr.getMatrY()


analizer = imageAnalizer()
analizer.setScale(20)
analizer.trainFromPath("pics")
analizer.getMatrix()
analizer.comparedAll()

print("End of Work")
