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
import numpy as np
from selenium import webdriver
import time
from bs4 import BeautifulSoup

Features = {'beamed_ceiling':0.7,
            'carpet':0.9,
            'ceiling fan': 0.6,
            'coffered_ceiling':0.6,
            'exposed_bricks':0.4,
            'fireplace':0.5,
            'french_doors':0.3,
            'hardwood_floor':0.3,
            'high_ceiling':0.1,
            'kitchen_bar':0.2,
            'kitchen_island':0.1,
            'natural_light':0.5,
            'notable_chandelier':0.8,
            'skylight':0.2,
            'stainless_steel': 0.1,
            'tile_floor': 0.5, 
            'vaulted_ceiling':0.5,
            'central_ac':0.1, 
            'deck':0.1, 
            'dock':0.4, 
            'fire_pit':0.4, 
            'hot_tub':0.3, 
            'lawn':0.6, 
            'mountain_view':0.7, 
            'outdoor_kitchen':0.6, 
            'outdoor_living_space':0.3, 
            'pergola':0.3, 
            'pool':0.1, 
            'water_view':0.2
            }

def JQuery(url):    
    # Create the webdriver object. Here the 
    # chromedriver is present in the driver 
    # folder of the root directory.
    driver = webdriver.Chrome(r"./chromedriver")
    
    # get https://www.geeksforgeeks.org/
    driver.get(url)
    
    button = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div/footer/div/button[2]")
    button.click()

    time.sleep(5)
    
    # Obtain button by link text and click.
    button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/main/ul[1]/li/button")
    button.click()

    time.sleep(10)
    codigo =  BeautifulSoup(driver.page_source, 'html.parser')

    with open('test.html', 'w') as f:
        f.write(codigo.prettify())
    
    return codigo


def getHTML(url):
    r = requests.get(url)
    code = BeautifulSoup(r.content,'html.parser')
    return code

def getListLinksPhotos(HTMLcode):
    HTMLcode.prettify()
    linesWithImages = HTMLcode.select(".re-DetailMultimediaImage-container > img")

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
        imagename = './data/images/FOTO_' + str(i + 1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

def cleanDataFolder(): 
    dir = './data/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((min(image.width, 500), min(image.height, 300)))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

def update(contenido, i, window,imageLinks, jsonValues):
    load_image('./data/images/' + 'FOTO_' + str(i + 1) + '.jpg', window)
    window['Prediction'].update(value='Type: ' + str(jsonValues[i]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']))    
    mirar = jsonValues[i]['response']['solutions']['re_condition']['score']
    if mirar is not None:
        window['Rate'].update(value='Rate: ' + str(mirar))
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
    puntos = 0.0
    cosas = 1
    for link in imageLinks:
        temporal = getPrediction(link)

        lista = temporal['response']['solutions']['re_features_v3']['detections']

        for element in lista:
            puntos += Features[element['label']]
            cosas += 1

        JSONvalues.append(temporal)
    
    return JSONvalues, puntos, cosas
        
def calculateThings(puntuacion, cosas):
    if cosas != 0:
        return float(puntuacion)/float(cosas)
    else:
        return 0.5

def main():
    indiceFoto = 0
    ubicacionFotos = []
    imageLinks = []
    jsonValues = []
    price = 0
    puntuacion = 0.0
    media = 0.0
    cosas = 0
    elements = [
        [sg.Input(size=(25,1), enable_events=True, key='url'), sg.Button("Search!")],
        [sg.Image(key='image')],
        [sg.Button('Prev'), sg.Button('Next')],
        [sg.Text("", size=(0,1), key='Cost')],
        [sg.Text("", size=(0,1), key='Prediction')],
        [sg.Text("", size=(0,1), key='Features')],
        [sg.Text("", size=(0,1), key='Rate')]
    ]

    window = sg.Window("RoomRate", elements, size=(500,500))
    
    while True:
        event, values = window.read()
        if event == 'Search!':
            indiceFoto = 0

            code = JQuery(values['url'])
            imageLinks = getListLinksPhotos(code)

            downloadImages(imageLinks)
            
            price = getPrice(code)
            price = price.replace('.', '')
            price = int(price)

            ubicacionFotos = os.listdir('./data/images/')   
            ubicacionFotos.sort()
            jsonValues, puntuacion, cosas = createJSON(imageLinks)

            media = calculateThings(puntuacion, cosas)

            load_image('./data/images/' + 'FOTO_' + str(indiceFoto + 1) + '.jpg', window)
            window["Cost"].update(value='Price: ' + str(price) + '€')
            window['Prediction'].update(value='Type: ' + str(jsonValues[indiceFoto]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']))
            window['Features'].update(value=str(media))
            
            mirar = jsonValues[indiceFoto]['response']['solutions']['re_condition']['score']

            if mirar is not None:
                window['Rate'].update(value='Rate: ' + str(mirar))
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
            cleanDataFolder()
            break    

if __name__ == "__main__":
    main()