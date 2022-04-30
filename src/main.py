from asyncio.base_subprocess import BaseSubprocessTransport
import requests
import re as regex
from bs4 import BeautifulSoup
import easygui
import os

def getHTML(url):
    r = requests.get(url)
    code = BeautifulSoup(r.content,'html.parser')
    with open('./data/codeHTML.html', 'w') as f:
        f.write(code.prettify())
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

    
def main():
    url = easygui.enterbox("What's your url of FOTOCASA you want to rate?")
    code = getHTML(url)
    imageLinks = getListLinksPhotos(code)
    downloadImages(imageLinks)
    cleanDataFolder()
    

if __name__ == '__main__':
    main()