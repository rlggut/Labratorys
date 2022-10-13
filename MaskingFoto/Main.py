from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Masking picture")
        self.window.geometry("800x450")
        self.frame = Frame(self.window)
        self.frame.grid()
        self.image = Image.new('RGB', (400, 400), (240,240,240))
        self.photo = ImageTk.PhotoImage(self.image)

        self.lblLoad = Label(self.frame, text="Choose pic")
        self.lblLoad.grid(column=0, row=0)
        self.btnLoad = Button(self.frame, text="...", command=self.clickedLoading)
        self.btnLoad.grid(column=3, row=0)
        self.lblChoosed = Label(self.frame, text="")
        self.lblChoosed.grid(column=0, row=1)

        self.canvasW = 200
        self.canvasH = 200
        self.canvas = Canvas(self.window, height=self.canvasH, width=3*self.canvasW)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(column=0, row=2)

        self.window.mainloop()

    def clickedLoading(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        self.lblChoosed.configure(text=file)
        self.image = Image.open(file)
        factorW = self.image.width/self.canvasW
        factorH = self.image.height / self.canvasH
        factor=max(factorW, factorH)
        print(self.image.width, self.image.height)
        if(factor>1):
            print(factor)
            self.image=self.image.reduce(int(factor))
        elif(factor<0.7):
            print(factor)
            self.image=self.image.resize((int(1/factor)*self.image.width,int(1/factor)*self.image.height))
            print((int(1/factor)*self.image.width,int(1/factor)*self.image.height))
        self.photo = ImageTk.PhotoImage(self.image)
        self.с_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.imageGrey = self.getGrey()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.с_imageGrey = self.canvas.create_image(self.image.width, 0, anchor='nw', image=self.photoGrey)
        self.canvas.grid(column=0, row=2)
    def getGrey(self):
        res = Image.new('RGB', (self.image.width, self.image.height), (0,0,0))
        for y in range(self.image.height):
            for x in range(self.image.width):
                value = self.image.getpixel((x,y))
                greyCol = int(value[0]*0.3+value[1]*0.59+value[2]*0.11)
                print( value, greyCol)
                res.putpixel((x,y), (greyCol,greyCol,greyCol))
        return res


app=App()