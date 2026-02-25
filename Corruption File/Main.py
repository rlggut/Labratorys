from tkinter import *
from tkinter import filedialog
import sys
import os

class FileProc():
    def __init__(self):
        self.window = Tk()
        self.window.title("File Corruption")
        self.canvasW = 370
        self.canvasH = 130
        size = "" + str(self.canvasW) + "x" + str(self.canvasH)
        self.window.geometry(size)
        self.window.minsize(height=self.canvasH,width=self.canvasW)
        self.frame = Frame(self.window)
        self.frame.grid()

        self.btnLoad = Button(self.frame, text="Укажите файл", command=self._clickedLoading)
        self.btnLoad.grid(column=0, row=0)
        self.lblFile=Label(self.frame, text="")
        self.lblFile.grid(column=1, row=0, columnspan=3)

        self.lblChoosed = Label(self.frame, text="Выберите тип ошибок")
        self.lblChoosed.grid(column=0, row=1, columnspan=2)
        self.errorType=IntVar(value=0)
        self.R1 = Radiobutton(self.frame,text="Битовые", value=0, variable=self.errorType, command=self._changeAccept, state = 'disabled')
        self.R1.grid(column=0, row=2,sticky=W)
        self.R2 = Radiobutton(self.frame,text="Байтовые", value=1, variable=self.errorType, command=self._changeAccept, state = 'disabled')
        self.R2.grid(column=1, row=2,sticky=W)

        corrVar=IntVar()
        corrVar.set(1)
        self.unitCorr = Checkbutton(self.frame,text="Искажение",variable=corrVar, state = 'disabled')
        self.unitCorr.grid(column=0, row=3,sticky=W)
        dellVar = IntVar()
        self.delUnit = Checkbutton(self.frame,text="Удаление",variable=dellVar, state = 'disabled')
        self.delUnit.grid(column=0, row=4,sticky=W)
        revVar = IntVar()
        self.revers = Checkbutton(self.frame,text="Реверс байт",variable=revVar, state = "disabled")
        self.revers.grid(column=1, row=3,sticky=W)
        invVar=IntVar()
        self.invers = Checkbutton(self.frame,text="Инверсия байт",variable=invVar, state = "disabled")
        self.invers.grid(column=1, row=4,sticky=W)

        self.lblPercent = Label(self.frame, text="Частота ошибок")
        self.lblPercent.grid(column=2, row=1)
        self.spinError = Spinbox(self.frame, from_=0.1, to=100.0, increment=0.1,width=10, state = 'disabled')
        self.spinError.grid(column=2, row=2)
        self.btnCorr = Button(self.frame, text="Создать искажения", command=self._createCorrFile, state = 'disabled')
        self.btnCorr.grid(column=2, row=3)

        self.window.mainloop()
    def _createCorrFile(self):
        print()

    def _changeAccept(self):
        if((self.errorType.get())==1):
            self.revers.config(state = 'active')
            self.invers.config(state = 'active')
        else:
            self.revers.config(state = 'disabled')
            self.invers.config(state = 'disabled')

    def _clickedLoading(self):
        self.fileName = filedialog.askopenfilename()
        if (self.fileName == ""):
            return False
        fileStr = self.fileName
        if(len(fileStr)>40):
            fileStr = fileStr[:15]+"..."+fileStr[-25:]
        self.lblFile.config(text=fileStr)
        self.unitCorr.config(state='active')
        self.delUnit.config(state='active')
        self.R1.config(state='active')
        self.R2.config(state='active')
        self.btnCorr.config(state='active')
        self.spinError.config(state='normal')

proc = FileProc()