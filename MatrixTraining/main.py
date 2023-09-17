#License: CC BY
#Roman Gutenkov, 28/05/23
#Version: 0.0.0

from tkinter import *

import PIL.Image
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..')) #path to https://github.com/rlggut/Labratorys
from Matrix import *
from ImageProcess import *

class imageAnalizer():
    def __init__(self):
        self._image = Image.new("RGB", (256, 256), "white")
        self._fileName=""

    def setImage(self, file, newFileName=""):
        if(isinstance(file,str)):
            self._image = Image.open(file)
            self._fileName = file
        elif(isinstance(file,PIL.Image.Image)):
            self._image=file.copy()
            if(newFileName==""):
                if(self._fileName==""): self._fileName="newPic.png"
            else: self._fileName=newFileName

filename = "base.jpg"
analizer = imageAnalizer()
analizer.setImage(filename)

print("End of Work")

