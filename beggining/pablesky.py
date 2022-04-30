# import module
from selenium import webdriver
import time
from bs4 import BeautifulSoup
  
# Create the webdriver object. Here the 
# chromedriver is present in the driver 
# folder of the root directory.
driver = webdriver.Chrome(r"./chromedriver")
  
# get https://www.geeksforgeeks.org/
driver.get("https://www.fotocasa.es/es/comprar/vivienda/barcelona-capital/calefaccion-no-amueblado/162876006/d")

# Maximize the window and let code stall 
# for 10s to properly maximise the window.
driver.maximize_window()
time.sleep(10)
  
# Obtain button by link text and click.
button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/main/ul[1]/li/button")
button.click()

time.sleep(10)
htmlCode = BeautifulSoup(driver.page_source, 'html.parser')

with open('test.html', 'w') as f:
    f.write(htmlCode.prettify())

