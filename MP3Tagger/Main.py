#License: CC BY
#Roman Gutenkov, 29/12/24
#Version: 0.2

from tkinter import *
from tkinter import filedialog
from ttkwidgets.autocomplete import AutocompleteCombobox
import sys
import os
from tkinter.ttk import Combobox

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

        genre = ["Blues",
            "Classic Rock",
            "Country",
            "Dance",
            "Disco",
            "Funk",
            "Grunge",
            "Hip-Hop",
            "Jazz",
            "Metal",
            "New Age",
            "Oldies",
            "Other",
            "Pop",
            "R&B",
            "Rap",
            "Reggae",
            "Rock",
            "Techno",
            "Industrial",
            "Alternative",
            "Ska",
            "Death Metal",
            "Pranks",
            "Soundtrack",
            "Euro-Techno",
            "Ambient",
            "Trip-Hop",
            "Vocal",
            "Jazz & Funk",
            "Fusion",
            "Trance",
            "Classical",
            "Instrumental",
            "Acid",
            "House",
            "Game",
            "Sound Clip",
            "Gospel",
            "Noise",
            "Alternative Rock",
            "Bass",
            "Soul",
            "Punk",
            "Space",
            "Meditative",
            "Instrumental Pop",
            "Instrumental Rock",
            "Ethnic",
            "Gothic",
            "Darkwave",
            "Techno-Industrial",
            "Electronic",
            "Pop-Folk",
            "Eurodance",
            "Dream",
            "Southern Rock",
            "Comedy",
            "Cult",
            "Gangsta",
            "Top 40",
            "Christian Rap",
            "Pop/Funk",
            "Jungle",
            "Native US",
            "Cabaret",
            "New Wave",
            "Psychadelic",
            "Rave",
            "Showtunes",
            "Trailer",
            "Lo-Fi",
            "Tribal",
            "Acid Punk",
            "Acid Jazz",
            "Polka",
            "Retro",
            "Musical",
            "Rock 'n' Roll",
            "Hard Rock",
            "Folk",
            "Folk-Rock",
            "National Folk",
            "Swing",
            "Fast Fusion",
            "Bebop",
            "Latin",
            "Revival",
            "Celtic",
            "Bluegrass",
            "Avantgarde",
            "Gothic Rock",
            "Progressive Rock",
            "Psychedelic Rock",
            "Symphonic Rock",
            "Slow Rock",
            "Big Band",
            "Chorus",
            "Easy Listening",
            "Acoustic",
            "Humour",
            "Speech",
            "Chanson",
            "Opera",
            "Chamber Music",
            "Sonata",
            "Symphony",
            "Booty Bass",
            "Primus",
            "Porn Groove",
            "Satire",
            "Slow Jam",
            "Club",
            "Tango",
            "Samba",
            "Folklore",
            "Ballad",
            "Power Ballad",
            "Rhythmic Soul",
            "Freestyle",
            "Duet",
            "Punk Rock",
            "Drum Solo",
            "A capella",
            "Euro-House",
            "Dance Hall",
            "Goa",
            "Drum & Bass",
            "Club-House",
            "Hardcore Techno",
            "Terror",
            "Indie",
            "BritPop",
            "Negerpunk",
            "Polsk Punk",
            "Beat",
            "Christian Gangsta Rap",
            "Heavy Metal",
            "Black Metal",
            "Crossover",
            "Contemporary Christian",
            "Christian Rock",
            "Merengue",
            "Salsa",
            "Thrash Metal",
            "Anime",
            "Jpop",
            "Synthpop",
            "Abstract",
            "Art Rock",
            "Baroque",
            "Bhangra",
            "Big Beat",
            "Breakbeat",
            "Chillout",
            "Downtempo",
            "Dub",
            "EBM",
            "Eclectic",
            "Electro",
            "Electroclash",
            "Emo",
            "Experimental",
            "Garage",
            "Global",
            "IDM",
            "Illbient",
            "Industro-Goth",
            "Jam Band",
            "Krautrock",
            "Leftfield",
            "Lounge",
            "Math Rock",
            "New Romantic",
            "Nu-Breakz",
            "Post-Punk",
            "Post-Rock",
            "Psytrance",
            "Shoegaze",
            "Space Rock",
            "Trop Rock",
            "World Music",
            "Neoclassical",
            "Audiobook",
            "Audio Theatre",
            "Neue Deutsche Welle",
            "Podcast",
            "Indie Rock",
            "G-Funk",
            "Dubstep",
            "Garage Rock",
            "Psybien"]

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
        self.comboGenre = AutocompleteCombobox(self.frame, completevalues=genre, state=DISABLED, validatecommand=self.__anyChange)
        self.comboGenre.grid(column=1, row=5, padx=10)

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
            self.comboGenre["state"]    = "normal"
            self.btnFileSave["state"]   = "normal"
            self.btnFileSave['text']    = "Сохранить метаданные"

            self.entryArtist.delete(0,END)
            self.entryAlbum.delete(0,END)
            self.entryName.delete(0,END)
            self.spinNum.delete(0,END)
            self.comboGenre.delete(0,END)

            self.entryArtist.insert(0,audioFile.tag.artist)
            self.entryAlbum.insert(0,audioFile.tag.album)
            self.entryName.insert(0,audioFile.tag.title)
            self.spinNum.insert(0,audioFile.tag.track_num[0])
            self.comboGenre.insert(0,audioFile.tag.genre)
    def __save(self):
            audioFile = eyed3.load(self.path)
            audioFile.tag.artist = self.entryArtist.get()
            audioFile.tag.album = self.entryAlbum.get()
            audioFile.tag.album_artist = audioFile.tag.artist
            audioFile.tag.title = self.entryName.get()
            audioFile.tag.track_num = self.spinNum.get()
            audioFile.tag.genre = self.comboGenre.get()
            audioFile.tag.save()

            self.btnFileSave['text']    = "Сохранено"

            self.entryArtist["state"]   = "disabled"
            self.entryAlbum["state"]    = "disabled"
            self.entryName["state"]     = "disabled"
            self.spinNum["state"]       = "disabled"
            self.comboGenre["state"]    = "disabled"
            self.btnFileSave["state"]   = "disabled"
app=App()