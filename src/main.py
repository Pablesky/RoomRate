from curses import mouseinterval
from turtle import update
import PySimpleGUI as sg
from PIL import Image, ImageTk
import requests
import re as regex
from bs4 import BeautifulSoup
import os
import requests
import time
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import cv2
import dlib

#LINKS muestra
#https://www.fotocasa.es/es/comprar/vivienda/palma-de-mallorca/aire-acondicionado-terraza-ascensor/163373875/d
#https://www.fotocasa.es/es/comprar/vivienda/palma-de-mallorca/aire-acondicionado-trastero-internet/163372395/d
#https://www.fotocasa.es/es/comprar/vivienda/palma-de-mallorca/aire-acondicionado-calefaccion-jardin-terraza-patio/163370729/d


N_MAX = 15

Features = {'beamed_ceiling':0.7,
            'carpet':0.9,
            'ceiling_fan': 0.6,
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
            'water_view':0.2,
            'natural_light':0.9
            }
""""
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
"""
def JQuery(url):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    
    driver.get(url)
    
    button = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div/div/footer/div/button[2]")
    button.click()

    time.sleep(5)

    button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/main/ul[1]/li/button")
    button.click()

    time.sleep(10)
    codigo =  BeautifulSoup(driver.page_source, 'html.parser')

    codigo.prettify()
    
    return codigo


def getHTML(url):
    r = requests.get(url)
    code = BeautifulSoup(r.content,'html.parser')
    return code

def getListLinksPhotos(HTMLcode):
    HTMLcode.prettify()
    linesWithImages = HTMLcode.select(".re-DetailMultimediaImage-container > img")[:N_MAX]

    imagesLinks = []
    for linia in linesWithImages:
        link = regex.search(r'src=\"(.*?)\"', str(linia)).group(1)
        imagesLinks.append(link)

    return imagesLinks

def getPrice(HTMLcode):
    HTMLcode.prettify()
    linesWithImages = HTMLcode.find_all("span", class_="re-DetailHeader-price")
    return regex.search(r'>(.*?) €<',str(linesWithImages[0])).group(1)

def downloadImages(imageLinks):
    for i, imagen in enumerate(imageLinks):
        response = requests.get(imagen)
        imagename = './data/FOTO_' + str(i + 1) + '.jpg'
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
    load_image('./data/' + 'FOTO_' + str(i + 1) + '.jpg', window)
    window['Prediction'].update(value='Type: ' + str(jsonValues[i]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']))    
    mirar = jsonValues[i]['response']['solutions']['re_condition']['score']
    if mirar is not None:
        window['Rate'].update(value='Rate: ' + str(mirar))
    else:
        window['Rate'].update(value="")

def getPrediction(ubicacionFoto):
    url = 'https://api-eu.restb.ai/vision/v2/multipredict'
    payload = {
        'client_key': 'KEY',
        'model_id': 're_roomtype_global_v2,re_features_v3,re_appliances_v2,re_condition',
        'image_url': ubicacionFoto
    }

    time.sleep(1)
    response = requests.get(url, params=payload)

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

def faceAge():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        if k%256 == 32:
            img_name = "data/face.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            break

    cam.release()

    cv2.destroyAllWindows()

    img = cv2.imread('data/face.png')
    img = cv2.resize(img, (720, 640))
    frame = img.copy()
    
    age_weights = "models/age_deploy.prototxt"
    age_config = "models/age_net.caffemodel"
    age_Net = cv2.dnn.readNet(age_config, age_weights)
    
    ageList = ['1', '5', '10', '17',
            '29', '41', '50', '80']
    model_mean = (78.4263377603, 87.7689143744, 114.895847746)
    
    fH = img.shape[0]
    fW = img.shape[1]
    
    Boxes = []  # to store the face co-ordinates
    mssg = 'Face Detected'  # to display on image
    
    face_detector = dlib.get_frontal_face_detector()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector(img_gray)

    if faces:
        for face in faces:
            x = face.left()  # extracting the face coordinates
            y = face.top()
            x2 = face.right()
            y2 = face.bottom()
    
            box = [x, y, x2, y2]
            Boxes.append(box)
            cv2.rectangle(frame, (x, y), (x2, y2), 
                        (00, 200, 200), 2)
    
        for box in Boxes:
            face = frame[box[1]:box[3], box[0]:box[2]]
    
            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), model_mean, swapRB=False)
    
            age_Net.setInput(blob)
            age_preds = age_Net.forward()
            age = ageList[age_preds[0].argmax()]
    return age

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
        [sg.Text("", size=(0,1), key='Rate'), sg.Text("", size=(0,1), key='Age')],
        [sg.Button('Face Compatibility'), sg.Text("", size=(0,1), key='Recomendation')]
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

            ubicacionFotos = os.listdir('./data/')   
            ubicacionFotos.sort()
            jsonValues, puntuacion, cosas = createJSON(imageLinks)

            media = calculateThings(puntuacion, cosas) * 100

            load_image('./data/' + 'FOTO_' + str(indiceFoto + 1) + '.jpg', window)
            window["Cost"].update(value='Price: ' + str(price) + '€')
            window['Prediction'].update(value='Type: ' + str(jsonValues[indiceFoto]['response']['solutions']['re_roomtype_global_v2']['top_prediction']['label']))
            window['Features'].update(value='Object points: ' + str(media))
            
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

        if event == 'Face Compatibility':
            age = faceAge()
            window['Age'].update(value='Aprox. age: ' + str(age))
            if media != 0.0:
                window['Recomendation'].update(value = 'Accuracy: ' + str(100.0 - abs(int(age) - media)))


if __name__ == "__main__":
    main()