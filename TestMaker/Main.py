from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import re

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking picture")
        size="640x400"
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.window.mainloop()

app=App()