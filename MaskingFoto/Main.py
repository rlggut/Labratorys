from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
sys.path.append('/Users/GRL/Desktop/Labratorys')
from Matrix import *
import re

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking picture")
        self.canvasW = 200
        self.canvasH = 200
        size=""+str(int(self.canvasW*2.1))+"x"+str(int(self.canvasH *3))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.image = Image.new('RGB', (self.canvasW, self.canvasH), (240,240,240))
        self.photo = ImageTk.PhotoImage(self.image)

        self.lblLoad = Label(self.frame, text="Choose pic")
        self.lblLoad.grid(column=0, row=0)
        self.btnLoad = Button(self.frame, text="...", command=self.__clickedLoading)
        self.btnLoad.grid(column=2, row=0)
        self.lblChoosed = Label(self.frame, text="FileName.(png/jpg)")
        self.lblChoosed.grid(column=0, row=1, columnspan=3)
        self.filename = ""

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
        self.edgeSpin = Spinbox(self.frame, from_ =0, to_=300, width=5, command=self.__getMaskPick)
        self.edgeSpin.grid(column=2, row=10)

        self.btnRecalc = Button(self.frame, text="Recalc", command=self.__getMaskPick, state=DISABLED)
        self.btnRecalc.grid(column=0, row=11)

        self.canvas = Canvas(self.window, height=3*self.canvasH, width=1.2 * self.canvasW)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(column=3, row=0,rowspan=12)

        self.window.mainloop()

    def __clickedLoading(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        self.btnRecalc["state"] = "normal"
        self.filename = file
        self.image = Image.open(file)
        pattern = '[^\/]+\.\D+'
        file = re.search(pattern,file).group(0)
        self.lblChoosed.configure(text=file)
        factorW = self.image.width/self.canvasW
        factorH = self.image.height / self.canvasH
        factor=max(factorW, factorH)
        if(factor>1):
            self.image=self.image.reduce(int(factor))
        elif(factor<0.7):
            self.image=self.image.resize((int(1/factor)*self.image.width,int(1/factor)*self.image.height))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        self.imageGrey = self.__getGrey()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.с_imageGrey = self.canvas.create_image(0, self.canvasH, anchor='nw', image=self.photoGrey)
        self.__getMaskPick()
    def __getMaskPick(self):
        if(self.filename==""):
            return False
        self.edge=int(self.edgeSpin.get())
        self.__getMatrXY()
        self.imageMasked = self.getMask(self.imageGrey, self.matrX, self.matrY, self.edge)
        self.photoMasked = ImageTk.PhotoImage(self.imageMasked)
        self.с_imageMasked = self.canvas.create_image(0, 2 * self.canvasH, anchor='nw', image=self.photoMasked)
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
        res = Image.new('RGB', (self.image.width, self.image.height), (0,0,0))
        for y in range(self.image.height):
            for x in range(self.image.width):
                value = self.image.getpixel((x,y))
                greyCol = int(value[0]*0.3+value[1]*0.59+value[2]*0.11)
                res.putpixel((x,y), (greyCol,greyCol,greyCol))
        return res
    def getMask(self, image, matrX, matrY, edge=100):
        res = Image.new('RGB', (image.width, image.height), (0,0,0))
        for y in range(1,image.height-1):
            for x in range(1,image.width-1):
                gX = 0
                gY = 0
                for j in range(-1,2):
                    for i in range(-1,2):
                        value = image.getpixel((x+i, y+j))
                        gX += matrX.getMatrXY(i+1,j+1)*(value[0]+value[1]+value[2])/3
                        gY += matrY.getMatrXY(i+1,j+1)*(value[0]+value[1]+value[2])/3
                degree=pow(gX*gX+gY*gY,0.5)
                if(degree> edge):
                    res.putpixel((x,y), (255,255,255))
        return res

app=App()