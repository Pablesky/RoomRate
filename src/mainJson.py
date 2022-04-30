from multiprocessing.sharedctypes import Value
from tokenize import group
from turtle import update
import PySimpleGUI as sg
from PIL import Image, ImageTk
from asyncio.base_subprocess import BaseSubprocessTransport
import requests
import re as regex
from bs4 import BeautifulSoup
import os
from textwrap import indent
import requests
import time

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

def getPrice(HTMLcode):
    HTMLcode.prettify()
    linesWithImages = HTMLcode.find_all("span", class_="re-DetailHeader-price")
    return regex.search(r'>(.*?) €<',str(linesWithImages[0])).group(1)


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
        image.thumbnail((min(image.width, 300), min(image.height, 300)))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

def update(contenido, i, window,imageLinks, jsonValues):
    load_image('./data/images/' + contenido[i], window)
    window['Prediction'].update(value=jsonValues[i]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label'])
    mirar = jsonValues[i]['response']['solutions']['re_condition']['score']
    if mirar is not None:
        window['Rate'].update(value=mirar)
    else:
        window['Rate'].update(value="")

def getPrediction(ubicacionFoto):
    url = 'https://api-eu.restb.ai/vision/v2/multipredict'
    payload = {
        # Add your client key
        'client_key': 'b717829c286243060e2429cc405e60bc480b18b2a4fe84b462e47cdf2ff41283',
        'model_id': 're_roomtype_global_v2,re_features_v3,re_appliances_v2,re_condition',
        # Add the image URL you want to classify
        'image_url': ubicacionFoto
    }

    # Make the classify request
    time.sleep(1)
    response = requests.get(url, params=payload)

    # The response is formatted in JSON
    return response.json() 
    

def createJSON(imageLinks):
    JSONvalues = []
    for link in imageLinks:
        JSONvalues.append(getPrediction(link))
    
    return JSONvalues
        


def main():
    indiceFoto = 0
    ubicacionFotos = []
    imageLinks = []
    jsonValues = []
    price = 0
    elements = [
        [sg.Input(size=(25,1), enable_events=True, key='url'), sg.Button("Search!")],
        [sg.Image(key='image')],
        [sg.Button('Prev'), sg.Button('Next')],
        [sg.Text("", size=(0,1), key='Cost')],
        [sg.Text("", size=(0,1), key='Prediction')],
        [sg.Text("", size=(0,1), key='Rate')]
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
            
            price = getPrice(code)
            price = price.replace('.', '')
            price = int(price)
            

            ubicacionFotos = os.listdir('./data/images/')   
            ubicacionFotos.sort()
            jsonValues = createJSON(imageLinks)

            load_image('./data/images/' + ubicacionFotos[indiceFoto], window)
            window["Cost"].update(value=str(price) + '€')
            window['Prediction'].update(value=jsonValues[indiceFoto]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label'])
            mirar = jsonValues[indiceFoto]['response']['solutions']['re_condition']['score']
            if mirar is not None:
                window['Rate'].update(value=mirar)
            else:
                window['Rate'].update(value="")
            

        
        if event == 'Next':
            if len(ubicacionFotos) > 1:
                indiceFoto = indiceFoto + 1
                if indiceFoto == len(ubicacionFotos):
                    indiceFoto = 0
                update(ubicacionFotos, indiceFoto, window,imageLinks, jsonValues)  

        if event == 'Prev':
            if len(ubicacionFotos) > 1:
                indiceFoto = indiceFoto - 1
                if indiceFoto < 0:
                    indiceFoto = len(ubicacionFotos) - 1
                update(ubicacionFotos, indiceFoto, window,imageLinks,jsonValues)
        
        if event == sg.WIN_CLOSED:
            break    

if __name__ == "__main__":
    main()