from tkinter import *
from tkinter import filedialog
import sys
import os

class FileProc():
    def __init__(self):
        self.window = Tk()
        self.window.title("File Corruption")
        self.canvasW = 350
        self.canvasH = 200
        size = "" + str(self.canvasW) + "x" + str(self.canvasH)
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()

        self.btnLoad = Button(self.frame, text="Укажите файл", command=self.__clickedLoading)
        self.btnLoad.grid(column=0, row=0)

        self.lblChoosed = Label(self.frame, text="Выберите тип ошибок")
        self.lblChoosed.grid(column=0, row=1, columnspan=3)
        self.errorType=IntVar(value=0)
        self.R1 = Radiobutton(self.frame,text="Битовые", value=0, variable=self.errorType)
        self.R1.grid(column=0, row=2)
        self.R2 = Radiobutton(self.frame,text="Байтовые", value=1, variable=self.errorType)
        self.R2.grid(column=2, row=2)

        self.delUnit = Checkbutton(self.frame,text="Удаление байт")
        self.delUnit.grid(column=0, row=3)
        self.revers = Checkbutton(self.frame,text="Реверс байт", state = "DISABLED")
        self.revers.grid(column=1, row=3)
        self.invers = Checkbutton(self.frame,text="Инверсия байт", state = "DISABLED")
        self.invers.grid(column=2, row=3)


        self.window.mainloop()

    def __clickedLoading(self):
        file = filedialog.askopenfilename()
        if (file == ""):
            return False
        print(file)


proc = FileProc()