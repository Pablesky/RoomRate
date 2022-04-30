# image_browser.py

import glob
from turtle import update
import PySimpleGUI as sg

from PIL import Image, ImageTk

from asyncio.base_subprocess import BaseSubprocessTransport
import requests
import re as regex
from bs4 import BeautifulSoup
import easygui
import os

def getHTML(url):
    r = requests.get(url)
    code = BeautifulSoup(r.content,'html.parser')
    return code

def getListLinksPhotos(HTMLcode):
    HTMLcode.prettify()
    linesWithImages = HTMLcode.find_all("img", class_="re-DetailMosaicPhoto")
    imagesLinks = []
    for linia in linesWithImages :
        link = regex.search(r'src=\"(.*?)\"', str(linia)).group(1)
        imagesLinks.append(link)
    return imagesLinks

def downloadImages(imageLinks):
    for i, imagen in enumerate(imageLinks):
        # open image link and save as file
        response = requests.get(imagen)
        imagename = './data/FOTO_' + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

def cleanDataFolder(): 
    dir = './data/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def parse_folder(path):
    images = glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png')
    return images

def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((330, 330))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")
        
def update(contenido, i, window):
    load_image('./data/' + contenido[i], window)

def main():
    i = 0
    contenido = []
    column = [sg.Button("Prev"), sg.Image(key="image"), sg.Button("Next")]
    elements = [
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), enable_events=True, key="file"),
            sg.Button("GO!"),
        ],
        column
    ]

    window = sg.Window("Image Viewer", elements, size=(475, 475))
    images = []
    location = 0

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "file":
            images = parse_folder(values["file"])
            if images:
                load_image(images[0], window)
        if event == "Next":
            i = i + 1
            if i == len(contenido):
                i = len(contenido) - 1
            print(str(i) + '\n')
            update(contenido, i, window)
        if event == "Prev":
            i = i - 1
            if i < 0:
                i = 0
            print(str(i) + '\n')    
            update(contenido, i, window)
        if event == "GO!":
            url = values['file']
            code = getHTML(url)
            imageLinks = getListLinksPhotos(code)
            downloadImages(imageLinks)

            contenido = os.listdir('./data/')
            print(contenido)

            load_image('./data/' + contenido[i], window)


    window.close()


if __name__ == "__main__":
    main()