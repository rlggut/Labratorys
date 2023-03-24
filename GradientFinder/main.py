from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))
from Matrix import *
from ImageProcess import *
import re


def nod(x, y):
    while(x*y>0):
        if(max(x,y)==x):
            x=x%y
        else:
            y=y%x
    return(x+y)

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Usage gradient for pic")
        self.canvasW = 200
        self.canvasH = 200
        size=str(int(self.canvasW*4.9))+"x"+str(int(self.canvasH *2.1))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()

        self.lblMatrX = Label(self.frame, text="Matrix for X")
        self.lblMatrX.grid(column=0, row=0, columnspan=3)

        self.dataX=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=j, row=1+i)
            if(i==0):
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '1')
            elif(i==1):
                dataColumn[0].insert(0, '-2')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '2')
            else:
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '1')
            self.dataX.append(dataColumn)
        self.lblMatrY = Label(self.frame, text="Matrix for Y")
        self.lblMatrY.grid(column=0, row=4, columnspan=3)

        self.dataY=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=j, row=5+i)
            if (i == 0):
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '-2')
                dataColumn[2].insert(0, '-1')
            elif (i == 1):
                dataColumn[0].insert(0, '0')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '0')
            else:
                dataColumn[0].insert(0, '1')
                dataColumn[1].insert(0, '2')
                dataColumn[2].insert(0, '1')
            self.dataY.append(dataColumn)

        self.btnRecalc = Button(self.frame, text="Recalc", command=self.__countGrade, state=DISABLED)
        self.btnRecalc.grid(column=0, row=8)

        self.canvas = Canvas(self.frame, height=2*self.canvasH, width=2 * self.canvasW, bg='white')
        self.canvas.grid(column=6, row=0, rowspan=12, columnspan=6)
        dx = (2 * self.canvasW) // 10
        dy = (2 * self.canvasH) // 10
        for i in range(11):
            self.canvas.create_line(i*dx, 0, i*dx, 2*self.canvasH)
        for i in range(11):
            self.canvas.create_line(0,i*dy, 2*self.canvasW, i*dy)

        for i in range(2):
            for j in range(10):
                self.canvas.create_line(i*dx, j * dy, (i+1)*dx, (j+1) * dy)
                self.canvas.create_line(i * dx, (j+1) * dy, (i + 1) * dx, j * dy)

                self.canvas.create_line(j * dx, i * dy, (j + 1) * dx, (i + 1) * dy)
                self.canvas.create_line(j * dx, (i + 1) * dy, (j + 1) * dx, i * dy)

        for i in range(8,10):
            for j in range(9,1,-1):
                self.canvas.create_line(i*dx, j * dy, (i+1)*dx, (j+1) * dy)
                self.canvas.create_line(i * dx, (j+1) * dy, (i + 1) * dx, j * dy)

                self.canvas.create_line(j * dx, i * dy, (j + 1) * dx, (i + 1) * dy)
                self.canvas.create_line(j * dx, (i + 1) * dy, (j + 1) * dx, i * dy)

        self.paintData = []
        for i in range(10):
            paintRow=[]
            for j in range(10):
                paintRow.append(0)
            self.paintData.append(paintRow)
        self.canvas.bind('<Enter>', self.__enterCanvas)
        self.canvas.bind('<Leave>', self.__leaveCanvas)
        self.window.bind('<Button-1>', self.__painting)

        self.lblLoadOrig = Label(self.frame, text="Choose orig pic")
        self.lblLoadOrig.grid(column=15, row=0)
        self.btnLoadOrig = Button(self.frame, text="...", command=self.__clickedLoadingOrig)
        self.btnLoadOrig.grid(column=16, row=0)
        self.lblChoosedOrig = Label(self.frame, text="FileName.(png/jpg)")
        self.lblChoosedOrig.grid(column=15, row=1, columnspan=3)
        self.filenameOrig = ""
        self.btnReMask = Button(self.frame, text="Retake mask", command=self.__getMaskPic)
        self.btnReMask.grid(column=15, row=2)

        self.canvasOrig = Canvas(self.frame, height=2*self.canvasH, width=self.canvasW)
        self.imageOrig = Image.new('RGB', (self.canvasW, self.canvasH), (255, 240, 240))
        self.photoOrig = ImageTk.PhotoImage(self.imageOrig)
        self.с_imageOrig = self.canvasOrig.create_image(0, 0, anchor='nw', image=self.photoOrig)
        self.canvasOrig.grid(column=15, row=3, rowspan=10, columnspan=5)

        self.window.mainloop()

    def __clickedLoadingOrig(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        if(file==""):
            return False
        self.filenameOrig = file
        self.imageOrig = Image.open(file)
        self.imageOrig.load()
        pattern = '[^\/]+\.\D+'
        file = re.search(pattern,file).group(0)
        self.lblChoosedOrig.configure(text=file)
        factorW = self.canvasW / self.imageOrig.width
        factorH = self.canvasH / self.imageOrig.height
        factor=min(factorW, factorH)
        self.imageOrig=self.imageOrig.resize((int(factor * self.imageOrig.width), int(factor * self.imageOrig.height)))
        self.photoOrig = ImageTk.PhotoImage(self.imageOrig)
        self.с_imageOrig = self.canvasOrig.create_image(0, 0, anchor='nw', image=self.photoOrig)

        self.imageGrey = self.imageOrig.convert("L")
        self.imageGrey.load()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.__getMaskPic()

    def __getMaskPic(self):
        if(self.filenameOrig== ""):
            return False
        self.edge=120
        self.__getMatrXY()
        self.imageMasked = maskedImageMatrix(self.imageGrey, self.matrX, self.matrY, self.edge)
        self.photoMasked = ImageTk.PhotoImage(self.imageMasked)
        self.с_imageMasked = self.canvasOrig.create_image(0, self.canvasH, anchor='nw', image=self.photoMasked)

    def __getMatrXY(self):
        self.matrX = Matrix(3, 3)
        matr = []
        for j in range(3):
            column = []
            for i in range(3):
                if (self.dataX[i][j].get() == '') or not (re.match('\-?\d+(\.\d+)?', self.dataX[i][j].get())) \
                        or (re.search('[^0-9\.\-]', self.dataX[i][j].get())):
                    self.dataX[i][j].delete(0, len(self.dataX[i][j].get()))
                    self.dataX[i][j].insert(0, '0')
                column.append(float(self.dataX[i][j].get()))
            matr.append(column)
        self.matrX.setData(matr)
        self.matrY = Matrix(3, 3)
        matr = []
        for j in range(3):
            column = []
            for i in range(3):
                column.append(float(self.dataY[i][j].get()))
            matr.append(column)
        self.matrY.setData(matr)
    def __enterCanvas(self,event):
        self.onCanvas=True

    def __leaveCanvas(self, event):
        self.onCanvas = False

    def __painting(self,event):
        if(self.onCanvas):
            x = event.x
            y = event.y
            dx=(2 * self.canvasW) // 10
            dy=(2 * self.canvasH) // 10
            x=x//dx
            y=y//dy
            if(x<2)or(y<2)or(x>=8)or(y>=8):
                return
            fillColor='white'
            if(self.paintData[y][x]==0):
                fillColor = 'black'
            self.paintData[y][x]=(self.paintData[y][x]+1)%2
            self.btnRecalc['state'] = "normal"
            self.canvas.create_rectangle(x*dx, y*dy, (x+1)*dx, (y+1)*dy, fill=fillColor)

    def __countGrade(self):
        self.btnRecalc['state'] = "disabled"
        straight=0
        upDown=0
        downUp=0
        for i in range(8):
            for j in range(8):
                x = j + 1
                y = i + 1
                if(self.paintData[y][x-1]+self.paintData[y][x+1]==1):
                    straight+=1
                if(self.paintData[y-1][x-1]+self.paintData[y+1][x+1]==1):
                    upDown+=1
                if(self.paintData[y+1][x-1]+self.paintData[y-1][x+1]==1):
                    downUp+=1
        k=nod(straight,upDown)
        k=nod(k,downUp)
        if(k==0):
            k=1
            straight=1
            upDown=1
            downUp=1
        straight=straight//k
        upDown=upDown//k
        downUp=downUp//k
        for i in range(3):
            for j in range(3):
                self.dataX[i][j].delete(0, len(self.dataX[i][j].get()))
        self.dataX[0][0].insert(0, str(-upDown))
        self.dataX[0][1].insert(0, '0')
        self.dataX[0][2].insert(0, str(downUp))

        self.dataX[1][0].insert(0, str(-straight))
        self.dataX[1][1].insert(0, '0')
        self.dataX[1][2].insert(0, str(straight))

        self.dataX[2][0].insert(0, str(-downUp))
        self.dataX[2][1].insert(0, '0')
        self.dataX[2][2].insert(0, str(upDown))

        straight = 0
        leftRight = 0
        rightLeft = 0
        for i in range(8):
            for j in range(8):
                x = j + 1
                y = i + 1
                if (self.paintData[y-1][x] + self.paintData[y+1][x] == 1):
                    straight += 1
                if (self.paintData[y - 1][x - 1] + self.paintData[y + 1][x + 1] == 1):
                    leftRight += 1
                if (self.paintData[y - 1][x + 1] + self.paintData[y + 1][x - 1] == 1):
                    rightLeft += 1
        k = nod(straight, leftRight)
        k = nod(k, rightLeft)
        if(k==0):
            k=1
            straight=1
            leftRight=1
            rightLeft=1
        straight = straight // k
        leftRight = leftRight // k
        rightLeft = rightLeft // k
        for i in range(3):
            for j in range(3):
                self.dataY[i][j].delete(0, len(self.dataY[i][j].get()))
        self.dataY[0][0].insert(0, str(leftRight))
        self.dataY[0][1].insert(0, str(straight))
        self.dataY[0][2].insert(0, str(rightLeft))

        self.dataY[1][0].insert(0, '0')
        self.dataY[1][1].insert(0, '0')
        self.dataY[1][2].insert(0, '0')

        self.dataY[2][0].insert(0, str(-rightLeft))
        self.dataY[2][1].insert(0, str(-straight))
        self.dataY[2][2].insert(0, str(-leftRight))

app=App()