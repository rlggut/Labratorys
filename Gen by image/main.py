from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os
import re

image = Image.open("base.jpg")
imageNw = Image.new("RGB", (image.width, image.height), "white")
n, m = 10, 10
dx=image.width//n
dy=image.height//m
for y in range(m):
    for x in range(n):
        r, g, b = 0, 0, 0
        for addx in range(dx):
            for addy in range(dy):
                p=image.getpixel((x*dx+addx,y*dy+addy))
                r+=(p[0]/(dx*dy))
                g+=(p[1]/(dx*dy))
                b+=(p[2]/(dx*dy))
        for addx in range(dx):
            for addy in range(dy):
                imageNw.putpixel((x*dx+addx, y*dy+addy),(int(r),int(g),int(b)))
image.save("baseNw.jpg")
imageNw.show()
