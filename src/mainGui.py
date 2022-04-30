import glob
from multiprocessing.sharedctypes import Value
from turtle import update
import PySimpleGUI as sg

from PIL import Image, ImageTk

from asyncio.base_subprocess import BaseSubprocessTransport
import requests
import re as regex
from bs4 import BeautifulSoup
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
        imagename = './data/images/FOTO_' + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

def cleanDataFolder(): 
    dir = './data/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((min(image.width, 500), min(image.height, 500)))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

def update(contenido, i, window):
    load_image('./data/images/' + contenido[i], window)
    window['Prediction'].update(value=contenido[i])

def main():
    indiceFoto = 0
    ubicacionFotos = []
    imageLinks = []
    elements = [
        [sg.Input(size=(25,1), enable_events=True, key='url'), sg.Button("Search!")],
        [sg.Image(key='image')],
        [sg.Button('Prev'), sg.Button('Next')],
        [sg.Text("", size=(0,1), key='Prediction')]
    ]

    window = sg.Window("RoomRate", elements, size=(500,500))
    
    while True:
        event, values = window.read()
        if event == 'Search!':
            indiceFoto = 0
            url = values['url']
            code = getHTML(url)
            imageLinks = getListLinksPhotos(code)
            downloadImages(imageLinks)
            print(imageLinks)

            ubicacionFotos = os.listdir('./data/images/')
            ubicacionFotos.sort()
            print(ubicacionFotos)

            load_image('./data/images/' + ubicacionFotos[indiceFoto], window)

            window['Prediction'].update(value=ubicacionFotos[indiceFoto])

        
        if event == 'Next':
            indiceFoto = indiceFoto + 1
            if indiceFoto == len(ubicacionFotos):
                indiceFoto = len(ubicacionFotos) - 1
            print(str(indiceFoto) + '\n')
            update(ubicacionFotos, indiceFoto, window)

        if event == 'Prev':
            indiceFoto = indiceFoto - 1
            if indiceFoto < 0:
                indiceFoto = 0
            print(str(indiceFoto) + '\n')
            update(ubicacionFotos, indiceFoto, window)
        
        if event == sg.WIN_CLOSED:
            break    

if __name__ == "__main__":
    main()