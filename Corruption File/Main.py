from tkinter import *
from tkinter import filedialog
import random
import os
from tkinter.messagebox import showinfo

class FileProc():
    def __init__(self):
        self.window = Tk()
        self.window.title("Искажение файлов")
        '''self.window.iconbitmap('Icon.ico')'''
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

        self.corrVar=IntVar()
        self.corrVar.set(1)
        self.unitCorr = Checkbutton(self.frame,text="Искажение",variable=self.corrVar, state = 'disabled')
        self.unitCorr.grid(column=0, row=3,sticky=W)
        self.dellVar = IntVar()
        self.delUnit = Checkbutton(self.frame,text="Удаление",variable=self.dellVar, state = 'disabled')
        self.delUnit.grid(column=0, row=4,sticky=W)
        self.revVar = IntVar()
        self.revers = Checkbutton(self.frame,text="Реверс байт",variable=self.revVar, state = "disabled")
        self.revers.grid(column=1, row=3,sticky=W)
        self.invVar=IntVar()
        self.invers = Checkbutton(self.frame,text="Инверсия байт",variable=self.invVar, state = "disabled")
        self.invers.grid(column=1, row=4,sticky=W)

        self.lblPercent = Label(self.frame, text="Частота ошибок")
        self.lblPercent.grid(column=2, row=1)
        self.spinError = Spinbox(self.frame, from_=0.1, to=100.0, increment=0.1,width=10, state = 'disabled')
        self.spinError.grid(column=2, row=2)
        self.lblOffset = Label(self.frame, text="Пропустить первые")
        self.lblOffset.grid(column=2, row=3)
        self.spinOffset = Spinbox(self.frame, from_=0, to=1000.0, increment=1,width=10, state = 'disabled', wrap=True)
        self.spinOffset.grid(column=2, row=4)
        self.btnCorr = Button(self.frame, text="Создать искажения", command=self._createCorrFile, state = 'disabled')
        self.btnCorr.grid(column=2, row=3)

        self.window.mainloop()
    def __delBit(self,num,offset):
        delBit=random.randint(0,7)+offset
        numAnsw=((num>>(16-delBit))<<(15-delBit))
        mask=0
        for bit in range(15-delBit):
            mask=mask<<1+1
        numAnsw=numAnsw+(num&mask)
        return(numAnsw)
    def __inversByte(self,num):
        return num^0xFF
    def __reversByte(self, num):
        answ=0
        for bit in range(8):
            answ=(answ<<1)+num%2
            num=num>>2
        return answ
    def __corrByte(self,num):
        mask=0
        for bit in range(8):
            bt= random.randint(0,1)
            mask=(mask<<1)+bt
        return num^mask
    def _createCorrFile(self):
        errRate = int(float(self.spinError.get())*10)
        if(self.errorType.get()==0):
            if(self.dellVar.get() == 0 and self.corrVar.get()==0):
                errRate=0
        elif(self.errorType.get()==1):
            if((self.dellVar.get() == 0 and self.corrVar.get()==0)and
                (self.revVar.get() == 0 and self.invVar.get() == 0)):
                errRate=0
        fileIn = open(self.fileName, 'rb')
        fileOut = open(self.fileName[:-4]+"_corr"+self.fileName[-4:],'wb+')
        reg=-1
        offset=0
        buffSize=1000
        self.collError=0
        float(self.spinError.get())
        buffIn=fileIn.read(int(float(self.spinOffset.get())))
        fileOut.write(bytes(buffIn))
        while(True):
            buffIn=fileIn.read(buffSize)
            buffOut=[]
            if(self.errorType.get()==0):
                for ch in buffIn:
                    if(reg<0):
                        reg=ch
                    else:
                        reg=(reg<<8)+ch
                        rnd = random.randint(0, 1000)
                        if(rnd<errRate):
                            self.collError+=1
                            if (self.dellVar.get() == 1 and self.corrVar.get()==0):
                                reg = self.__delBit(reg,offset)
                                offset+=1
                            elif (self.dellVar.get() == 0 and self.corrVar.get() == 1):
                                corr = random.randint(0, 7)
                                reg = reg ^ (1<<corr)
                            elif (self.dellVar.get() == 0 and self.corrVar.get() == 0):
                                reg = reg
                            else:
                                rnd = random.randint(0, 1)
                                if(rnd==1):
                                    reg = self.__delBit(reg, offset)
                                    offset += 1
                                else:
                                    corr = random.randint(0, 7)
                                    reg = reg ^ (1 << corr)
                        buffOut.append((reg>>(8-offset))&0xFF)
                        reg=ch>>offset
                        if(offset==8):
                            offset=0
                            reg=-1
            else:
                for ch in buffIn:
                    rnd = random.randint(0, 1000)
                    if (rnd < errRate):
                        self.collError += 1
                        buffFunc=[]
                        if(self.corrVar.get()==1):
                            buffFunc.append(self.__corrByte)
                        if (self.revVar.get() == 1):
                            buffFunc.append(self.__reversByte)
                        if (self.invVar.get() == 1):
                            buffFunc.append(self.__inversByte)
                        typError=len(buffFunc)
                        if(self.dellVar.get()==1):
                            typError+=1
                            ind = random.randint(0, typError - 1)
                            if(ind!=(typError - 1)):
                                buffOut.append(buffFunc[ind](ch))
                        else:
                            ind = random.randint(0, typError-1)
                            buffOut.append(buffFunc[ind](ch))
                    else:
                        buffOut.append(ch)
            fileOut.write(bytes(buffOut))
            if(len(buffIn)!=buffSize):
                break
        fileOut.close()
        fileIn.close()
        showinfo(title="Результат", message="Файл сохранен: "+fileOut.name+"\nКоличество изменений: "+str(self.collError))
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
        self.spinOffset.config(state='normal')
        size = os.path.getsize(self.fileName)
        self.spinOffset.config(to=min(self.spinOffset.cget("to"),size))

proc = FileProc()