#License: CC BY
#Roman Gutenkov, 29/12/24
#Version: 0.1

from tkinter import *
import sys
import os
import eyed3
#Жанры
#https://en.wikipedia.org/wiki/List_of_ID3v1_genres

path="C:\\Users\\Роман\\YandexDisk\\Ableton project\\Firstly\\Firstly Project\\Firstly.mp3"

audioFile = eyed3.load(path)
audioFile.tag.artist = "Unknown Kain"
audioFile.tag.album = "First Met"
audioFile.tag.album_artist = "Unknown Kain"
audioFile.tag.title = "Firstly"
audioFile.tag.track_num = 1
audioFile.tag.genre = "Electronic"
audioFile.tag.save()
print((audioFile.tag.genre))
