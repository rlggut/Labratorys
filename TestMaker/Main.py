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
        self.radioClass = Radiobutton(self.frame, text="Classwork", variable=self.var, value=2)
        self.radioClass.grid(column=1, row=0)
        self.radioHome = Radiobutton(self.frame, text="Homework", variable=self.var, value=1)
        self.radioHome.grid(column=2, row=0)
        self.radioClass.select()

        now = datetime.datetime.now()
        self.lblDataSelect = LabelFrame(self.frame, text='Data selection', labelanchor=NW)
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

#        self.btnLoadOrig = Button(self.frame, text="...", command=self.__clickedLoadingOrig)
#        self.btnLoadOrig.grid(column=2, row=0)

        self.window.mainloop()
    def __correctData(self):
        days = monthrange(int(self.yearSpin.get()), int(self.monthSpin.get()))[1]
        if(int(self.daySpin.get())>days):
            self.daySpin.set(days)

app=App()