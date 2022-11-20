from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import re
from Variants import *
import datetime
from calendar import monthrange

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking picture")
        size="640x400"
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.variant=Variant()

        self.lblTypeOfWork = Label(self.frame, text="Choose type of work")
        self.lblTypeOfWork.grid(column=0, row=0)
        self.var = IntVar()
        self.radioClass = Radiobutton(self.frame, text="Classwork", variable=self.var, value=2, command=self.__saveFileDir)
        self.radioClass.grid(column=1, row=0)
        self.radioHome = Radiobutton(self.frame, text="Homework", variable=self.var, value=1, command=self.__saveFileDir)
        self.radioHome.grid(column=2, row=0)
        self.radioClass.select()

        now = datetime.datetime.now()
        self.lblDataSelect = LabelFrame(self.frame, text='Data selection', labelanchor=N)
        self.lblDay = Label(self.lblDataSelect , text="DD")
        self.lblDay.grid(column=0, row=0)
        self.daySpin = ttk.Spinbox(self.lblDataSelect , from_=1, to_=31, width=5, command=self.__correctData)
        self.daySpin.grid(column=1, row=0)
        self.daySpin.set(now.day)
        self.lblMonth = Label(self.lblDataSelect , text="MM")
        self.lblMonth.grid(column=2, row=0)
        self.monthSpin = ttk.Spinbox(self.lblDataSelect , from_=1, to_=12, width=5, command=self.__correctData)
        self.monthSpin.grid(column=3, row=0)
        self.monthSpin.set(now.month)
        self.lblYear = Label(self.lblDataSelect , text="YY")
        self.lblYear.grid(column=4, row=0)
        self.yearSpin = ttk.Spinbox(self.lblDataSelect , from_=now.year, to_=now.year+10, width=5, command=self.__correctData)
        self.yearSpin.set(now.year)
        self.yearSpin.grid(column=5, row=0)
        self.lblDataSelect.grid(column=0, row=1, columnspan=5)

        self.filenameDir="C:"
        self.lblSave = Label(self.frame, text="Where to save")
        self.lblSave.grid(column=0, row=2)
        self.btnDirSave = Button(self.frame, text="...", command=self.__clickedSaving)
        self.btnDirSave.grid(column=1, row=2)
        self.lblSaveFile = Label(self.frame, text="Will be saved as...")
        self.lblSaveFile.grid(column=0, row=3, columnspan=7)
        self.__saveFileDir()

        self.lblVariant = Label(self.frame, text="Choose key:")
        self.lblVariant.grid(column=0, row=4)
        self.entryKey = Entry(self.frame)
        self.entryKey.grid(column=1, row=4)
        self.btnSave = Button(self.frame, text="Create&Save", command=self.__SavingVariant)
        self.btnSave.grid(column=2, row=4)

        self.window.mainloop()

    def __SavingVariant(self):
        fopen = open(self.filenameDir+"/"+self.filenameSave, 'w')
        footer=""
        if(self.var.get()==1):
            footer = "Homework"
        else:
            footer = "Classwork"
        footer = footer+"              "+self.daySpin.get()+"/"+self.monthSpin.get()+"/"+str(int(self.yearSpin.get())%100)
        fopen.write(footer+"\n")
        fopen.write(self.variant.getQuestion(1))
        fopen.close()

        asnswFileName = self.filenameSave
        asnswFileName = asnswFileName.rstrip('.doc')
        asnswFileName = asnswFileName+"_answer.doc"
        fopen = open(self.filenameDir+"/"+asnswFileName, 'w')
        fopen.write(footer+"\n")
        fopen.write(self.variant.getAnswer(1))
        fopen.close()

    def __saveFileDir(self):
        self.filenameSave=""
        if(self.var.get()==1):
            self.filenameSave = "Homework "
        else:
            self.filenameSave = "Classwork "
        self.filenameSave = self.filenameSave+"("+self.daySpin.get()+"_"+self.monthSpin.get()+"_"+self.yearSpin.get() + ").doc"
        self.lblSaveFile["text"]="Will be saved as: "+self.filenameDir +"/"+ self.filenameSave

    def __correctData(self):
        days = monthrange(int(self.yearSpin.get()), int(self.monthSpin.get()))[1]
        if(int(self.daySpin.get())>days):
            self.daySpin.set(days)
        self.__saveFileDir()

    def __clickedSaving(self):
        file = filedialog.askdirectory()
        if (file == ""):
            return False
        self.filenameDir = file
        self.__saveFileDir()

app=App()