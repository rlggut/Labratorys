from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk
import sys
sys.path.append('/Users/GRL/Desktop/Labratorys')
from Matrix import *
from ImageProcess import *
import re

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking Edge Finding")
        self.canvasW = 200
        self.canvasH = 200
        size=""+str(int(self.canvasW*3.9))+"x"+str(int(self.canvasH *2.1))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.imageOrig = Image.new('RGB', (self.canvasW, self.canvasH), (240, 240, 240))
        self.photoOrig = ImageTk.PhotoImage(self.imageOrig)

        self.lblLoadOrig = Label(self.frame, text="Choose orig pic")
        self.lblLoadOrig.grid(column=0, row=0)
        self.btnLoadOrig = Button(self.frame, text="...", command=self.__clickedLoadingOrig)
        self.btnLoadOrig.grid(column=2, row=0)
        self.lblChoosedOrig = Label(self.frame, text="FileName.(png/jpg)")
        self.lblChoosedOrig.grid(column=0, row=1, columnspan=3)
        self.filenameOrig = ""

        self.lblLoadComp = Label(self.frame, text="Choose an image with outline")
        self.lblLoadComp.grid(column=3, row=0, columnspan=2)
        self.btnLoadComp = Button(self.frame, text="...", command=self.__clickedLoadingComp, state=DISABLED)
        self.btnLoadComp.grid(column=5, row=0)
        self.lblChoosedComp = Label(self.frame, text="FileName.(png/jpg)")
        self.lblChoosedComp.grid(column=3, row=1, columnspan=3)
        self.filenameComp = ""
        self.btnFinding = Button(self.frame, text="Finding edge", command=self.__clickedFindingEdge, state=DISABLED)
        self.btnFinding.grid(column=3, row=2, columnspan=3)
        self.lblPredictEdge = Label(self.frame, text="")
        self.lblPredictEdge.grid(column=3, row=3, columnspan=3)
        self.pbFinding = Progressbar(self.frame, orient='horizontal', length=150, mode='determinate')
        self.pbFinding.grid(column=3, row=4, columnspan=3, padx=10, pady=10)
        self.lblResultFinding = Label(self.frame, text="")
        self.lblResultFinding.grid(column=3, row=5, columnspan=3)

        self.lblMatrX = Label(self.frame, text="Matrix for X")
        self.lblMatrX.grid(column=0, row=2, columnspan=3)

        self.dataX=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=0+i, row=3+j)
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
        self.lblMatrY.grid(column=0, row=6, columnspan=3)

        self.dataY=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=0+i, row=7+j)
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

        self.lblEdge = Label(self.frame, text="Boundary detector")
        self.lblEdge.grid(column=0, row=10, columnspan=2)
        self.edgeSpin = Spinbox(self.frame, from_ =0, to_=300, width=5, command=self.__getMaskPic)
        self.edgeSpin.grid(column=2, row=10)
        self.edge = 100
        self.edgeSpin.delete(0, len(self.edgeSpin.get()))
        self.edgeSpin.insert(0, str(self.edge))

        self.btnRecalc = Button(self.frame, text="Recalc", command=self.__getMaskPic, state=DISABLED)
        self.btnRecalc.grid(column=0, row=11)

        self.canvas = Canvas(self.window, height=2*self.canvasH, width=2 * self.canvasW)
        self.с_imageOrig = self.canvas.create_image(0, 0, anchor='nw', image=self.photoOrig)
        self.canvas.grid(column=6, row=0, rowspan=12, columnspan=5)

        self.window.mainloop()

    def __clickedFindingEdge(self):
        self.pbFinding['value'] = 0
        imageOrig = self.imageOrig.convert('L')
        similarProc = compareImageProc(maskedImageMatrix(imageOrig, self.matrX, self.matrY, 1), self.imageComp)
        self.lblPredictEdge.configure(text="Preferred edge: 1")
        imageComp = self.imageComp.convert('RGB')
        for edge in range(1,301,5):
            similarProcTmp = compareImageProc(maskedImageMatrix(imageOrig, self.matrX, self.matrY, edge), imageComp)
            if (similarProcTmp > similarProc):
                self.lblPredictEdge.configure(text="Preferred edge: " + str(edge))
                similarProc = similarProcTmp
            val=((100*edge)/300)
            self.pbFinding['value'] = val
            self.pbFinding.update()
        self.pbFinding['value'] = 100
        self.lblResultFinding.configure(text="Deviations about: "+str(int((100 - similarProc)*100)/100)+"%")
    def __clickedLoadingComp(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        if(file==""):
            return False
        self.lblResultFinding.configure(text="")
        self.lblPredictEdge.configure(text="")
        self.pbFinding['value'] = 0
        self.filenameComp = file
        self.imageComp = Image.open(file)
        self.imageComp.load()
        self.imageComp = self.imageComp.convert('RGB')
        pattern = '[^\/]+\.\D+'
        file = re.search(pattern,file).group(0)
        self.lblChoosedComp.configure(text=file)
        factorW = self.canvasW / self.imageComp.width
        factorH = self.canvasH / self.imageComp.height
        factor=min(factorW, factorH)
        self.imageComp=self.imageComp.resize((int(factor * self.imageComp.width), int(factor * self.imageComp.height)))
        self.photoComp = ImageTk.PhotoImage(self.imageComp)
        self.с_imageComp = self.canvas.create_image(self.canvasW, self.canvasH, anchor='nw', image=self.photoComp)
        self.btnFinding["state"] = "normal"

    def __clickedLoadingOrig(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        if(file==""):
            return False
        self.lblResultFinding.configure(text="")
        self.lblPredictEdge.configure(text="")
        self.pbFinding['value'] = 0
        self.btnRecalc["state"] = "normal"
        self.btnLoadComp["state"] = "normal"
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
        self.с_imageOrig = self.canvas.create_image(0, 0, anchor='nw', image=self.photoOrig)

        self.imageGrey = self.__getGrey()
        self.imageGrey.load()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.с_imageGrey = self.canvas.create_image(0, self.canvasH, anchor='nw', image=self.photoGrey)
        self.__getMaskPic()
    def __getMaskPic(self):
        if(self.filenameOrig== ""):
            return False
        if(re.match("[^0-9]",self.edgeSpin.get())):
            self.edgeSpin.delete(0, len(self.edgeSpin.get()))
            self.edgeSpin.insert(0, str(self.edge))
        self.edge=int(self.edgeSpin.get())
        self.__getMatrXY()
        self.imageMasked = maskedImageMatrix(self.imageGrey, self.matrX, self.matrY, self.edge)
        self.photoMasked = ImageTk.PhotoImage(self.imageMasked)
        self.с_imageMasked = self.canvas.create_image(self.canvasW, 0, anchor='nw', image=self.photoMasked)
        self.canvas.grid(column=3, row=0, rowspan=10)
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

    def __getGrey(self):
        res = self.imageOrig.convert("L")
        return res
    def __getGreyOwn(self):
        res = Image.new('RGB', (self.imageOrig.width, self.imageOrig.height), (0, 0, 0))
        for y in range(self.imageOrig.height):
            for x in range(self.imageOrig.width):
                value = self.imageOrig.getpixel((x, y))
                greyCol = int(value[0]*0.3+value[1]*0.59+value[2]*0.11)
                res.putpixel((x,y), (greyCol,greyCol,greyCol))
        return res

app=App()