from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
sys.path.append('/Users/GRL/Desktop/Labratorys')
from Matrix import *

def maskedImageMatrix(image, matrX, matrY, edge):
    if not(isinstance(image, Image.Image)):
        return False
    if not(isinstance(matrX, Matrix)):
        return False
    if not(isinstance(matrY, Matrix)):
        return False
    res = Image.new('RGB', (image.width, image.height), (0,0,0))
    for y in range(1,image.height-1):
        for x in range(1,image.width-1):
            gX = 0
            gY = 0
            for j in range(-1,2):
                for i in range(-1,2):
                    value = image.getpixel((x+i, y+j))
                    if(isinstance(value,tuple)):
                        value=((value[0]+value[1]+value[2])/3)
                    gX += matrX.getMatrXY(i+1,j+1)*value
                    gY += matrY.getMatrXY(i+1,j+1)*value
            degree=pow(gX*gX+gY*gY,0.5)
            if(degree> edge):
                res.putpixel((x,y), (255,255,255))
    return res

class ImageClass(Image.Image):
    def useFiltr(self, matrX, matrY, edge):
        self = maskedImageMatrix(self, matrX, matrY, edge)
