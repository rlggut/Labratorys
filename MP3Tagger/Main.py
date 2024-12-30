#License: CC BY
#Roman Gutenkov, 29/12/24
#Version: 0.2

from tkinter import *
from tkinter import filedialog
import sys
import os
import eyed3
#Жанры
#https://en.wikipedia.org/wiki/List_of_ID3v1_genres

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("MP3 метаданные")
        self.window.geometry("280x150")
        self.frame = Frame(self.window)
        self.frame.grid()
        self.path=""

        self.btnFileChoose = Button(self.frame, text="Выбрать .mp3", command=self.__open)
        self.btnFileChoose.grid(column=0, row=0)
        self.btnFileSave = Button(self.frame, text="Сохранить метаданные", command=self.__save, state=DISABLED)
        self.btnFileSave.grid(column=1, row=0)

        self.lblArtist = Label(self.frame, text="Исполнитель")
        self.lblArtist.grid(column=0, row=1, padx=10)
        self.entryArtist = Entry(self.frame, text="", state=DISABLED, validatecommand=self.__anyChange)
        self.entryArtist.grid(column=1, row=1, padx=10)

        self.lblAlbum = Label(self.frame, text="Альбом")
        self.lblAlbum.grid(column=0, row=2, padx=10)
        self.entryAlbum = Entry(self.frame, text="", state=DISABLED, validatecommand=self.__anyChange)
        self.entryAlbum.grid(column=1, row=2, padx=10)

        self.lblName = Label(self.frame, text="Название")
        self.lblName.grid(column=0, row=3, padx=10)
        self.entryName = Entry(self.frame, text="", state=DISABLED, validatecommand=self.__anyChange)
        self.entryName.grid(column=1, row=3, padx=10)

        self.lblNumber = Label(self.frame, text="Номер трека")
        self.lblNumber.grid(column=0, row=4, padx=10)
        self.spinNum = Spinbox(self.frame, from_ =1, to_=50, state=DISABLED, validatecommand=self.__anyChange)
        self.spinNum.grid(column=1, row=4, padx=10)

        self.lblGenre = Label(self.frame, text="Жанр")
        self.lblGenre.grid(column=0, row=5, padx=10)
        self.entryGenre = Entry(self.frame, text="", state=DISABLED, validatecommand=self.__anyChange)
        self.entryGenre.grid(column=1, row=5, padx=10)

        self.window.mainloop()

    def __anyChange(self):
        self.btnFileSave['text'] = "Сохранить метаданные"
    def __open(self):
        path = (filedialog.askopenfilename())
        if(path.endswith(".mp3")):
            self.path=path
            audioFile = eyed3.load(self.path)
            self.entryArtist["state"]   = "normal"
            self.entryAlbum["state"]    = "normal"
            self.entryName["state"]     = "normal"
            self.spinNum["state"]       = "normal"
            self.entryGenre["state"]    = "normal"
            self.btnFileSave["state"]   = "normal"
            self.btnFileSave['text']    = "Сохранить метаданные"

            self.entryArtist.delete(0,END)
            self.entryAlbum.delete(0,END)
            self.entryName.delete(0,END)
            self.spinNum.delete(0,END)
            self.entryGenre.delete(0,END)

            self.entryArtist.insert(0,audioFile.tag.artist)
            self.entryAlbum.insert(0,audioFile.tag.album)
            self.entryName.insert(0,audioFile.tag.title)
            self.spinNum.insert(0,audioFile.tag.track_num[0])
            self.entryGenre.insert(0,audioFile.tag.genre)
    def __save(self):
            audioFile = eyed3.load(self.path)
            audioFile.tag.artist = self.entryArtist.get()
            audioFile.tag.album = self.entryAlbum.get()
            audioFile.tag.album_artist = audioFile.tag.artist
            audioFile.tag.title = self.entryName.get()
            audioFile.tag.track_num = self.spinNum.get()
            audioFile.tag.genre = self.entryGenre.get()
            audioFile.tag.save()

            self.btnFileSave['text']    = "Сохранено"

            self.entryArtist["state"]   = "disabled"
            self.entryAlbum["state"]    = "disabled"
            self.entryName["state"]     = "disabled"
            self.spinNum["state"]       = "disabled"
            self.entryGenre["state"]    = "disabled"
            self.btnFileSave["state"]   = "disabled"
app=App()