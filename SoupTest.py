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
    result = regex.match('src=";(.*)"',i)
    lista.append(result.group(1))

print(lista)
