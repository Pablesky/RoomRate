from asyncio.base_subprocess import BaseSubprocessTransport
import requests
import re as regex
from bs4 import BeautifulSoup

url = 'https://www.fotocasa.es/es/comprar/vivienda/palma-de-mallorca/aire-acondicionado-calefaccion-terraza-ascensor/163304622/d'

r = requests.get(url)
soup = BeautifulSoup(r.content,'html.parser')
with open('test.txt','w') as f:
    f.write(soup.prettify())


list = soup.find_all("img", class_="re-DetailMosaicPhoto")
lista = []
for i in list :
    paraula = regex.search(r'src=\"(.*?)\"', str(i)).group(1)
    lista.append(paraula)

print(lista)

for i, imagen in enumerate(lista):
    # open image link and save as file
    response = requests.get(imagen)
    
    imagename = './fotos/FOTO ' + str(i+1) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(response.content)
