from tkinter import *
from PIL import Image, ImageTk
from Matrix import *

def makeGaussSmooth(image):
    if not(isinstance(image, Image.Image)):
        return False
    res = Image.new('RGB', (image.width, image.height), (0,0,0))
    gauss=Matrix()
    gauss.setGauss()
    for y in range(image.height):
        for x in range(image.width):
            r,g,b=0,0,0
            for j in range(-2,3):
                for i in range(-2,3):
                    if(x+i>=0 and x+i<image.width and y+j>=0 and y+j<image.height):
                        r += gauss.getMatrXY(i + 2, j + 2) * image.getpixel((x + i, y + j))[0]
                        g += gauss.getMatrXY(i + 2, j + 2) * image.getpixel((x + i, y + j))[1]
                        b += gauss.getMatrXY(i + 2, j + 2) * image.getpixel((x + i, y + j))[2]
            res.putpixel((x,y),(int(r),int(g),int(b)))
    return res

def maskedImageMatrix(image, matrX, matrY, edge):
    if not(isinstance(image, Image.Image)):
        return False
    if not(isinstance(matrX, Matrix)):
        return False
    if not(isinstance(matrY, Matrix)):
        return False
    if(matrX.getN()!=matrY.getN() or (matrX.getM()!=matrY.getM()) or (matrX.getM()!=matrX.getN())):
        return False
    res = Image.new('RGB', (image.width, image.height), (0,0,0))
    delt=(matrX.getN()-1)//2
    for y in range(delt,image.height-delt):
        for x in range(delt,image.width-delt):
            gX = 0
            gY = 0
            for j in range(-delt,delt+1):
                for i in range(-delt,delt+1):
                    value = image.getpixel((x+i, y+j))
                    if(isinstance(value,tuple)):
                        value=((value[0]+value[1]+value[2])/3)
                    gX += matrX.getMatrXY(i+1,j+1)*value
                    gY += matrY.getMatrXY(i+1,j+1)*value
            degree=pow(gX*gX+gY*gY,0.5)
            if(degree > edge):
                res.putpixel((x,y), (255,255,255))
    return res

def countMatrixGrad(image, matr, edge=100):
    n = 0
    res = 0
    if not(isinstance(image, Image.Image)):
        return -1
    if not(isinstance(matr, Matrix)):
        if not(isinstance(matr,list)):
            return -1
        else:
            for i in range(len(matr)):
                if not (isinstance(matr[i], Matrix)):
                    return -1
            lt=matr
            n = len(lt)-1
            matr=lt[0]
            res=[]
    for i in range(n+1):
        if(n!=0):
            matr=lt[i]
        if(matr.getN()!=matr.getN()):
            return -1
        delt=(matr.getN()-1)//2
        count = 0
        for y in range(delt,image.height-delt):
            for x in range(delt,image.width-delt):
                degree = 0
                for j in range(-delt,delt+1):
                    for i in range(-delt,delt+1):
                        value = image.getpixel((x+i, y+j))
                        if(isinstance(value,tuple)):
                            value=((value[0]+value[1]+value[2])/3)
                        degree += matr.getMatrXY(i+1,j+1)*value
                if(degree > edge):
                    count+=1
        if(n==0): res=count
        else: res.append(count)
    return res
def delBorderGlitch(image, n=3, edge=3):
    res = Image.new('RGB', (image.width, image.height), (0,0,0))
    delt=(n-1)//2
    for y in range(delt,image.height-delt):
        for x in range(delt,image.width-delt):
            dt = 0
            for j in range(-delt,delt+1):
                for i in range(-delt,delt+1):
                    value = image.getpixel((x+i, y+j))
                    if(value==(255,255,255)):
                        dt+=1
            if(dt> edge):
                res.putpixel((x,y), (255,255,255))
    return res

def compareImage(image1, image2):
    if not(isinstance(image1, Image.Image)):
        return False
    if not(isinstance(image2, Image.Image)):
        return False
    width = min(image1.width,image2.width)
    height = min(image1.height,image2.height)
    diffNums = 0
    for y in range(height):
        for x in range(width):
            if(image1.getpixel((x,y))!=image2.getpixel((x,y))):
                diffNums+=1
    return diffNums

def compareImageProc(image1, image2):
    diff = compareImage(image1, image2)
    size = max(image1.height*image1.width, image2.height*image2.width)
    return (100*(size-diff))/size