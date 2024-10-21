from selenium import webdriver
import base64
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, requests, random
from selenium.webdriver.chrome.options import Options
from string import ascii_letters, digits
from flask import Flask
from flask_cors import CORS, cross_origin
import os
import sys

# Redirigir sys.stdout y sys.stderr si están en None
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')


apping = Flask(__name__)

CORS(apping)
def browser_pag(prompt):
    print(prompt)
    conf = Options()
    conf.add_argument("--headless=old") 
    d_link = []
    driver = webdriver.Chrome('C:\driver_chrome\chromedriver.exe', options=conf)
    driver.get("https://copyter.com/generador-de-imagen-ia")
    path = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div/div/div/form/div/div[1]/div/div/div[2]/div[3]/div/div/textarea"))
    )
    path.send_keys(prompt)
    click = WebDriverWait(driver,7).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div/div/div/form/div/div[1]/div/div/div[3]/div/div/button"))
    )
    click.send_keys(Keys.ENTER)
    downl = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sorting_1"))
    )
    
    direct = downl.find_elements(By.TAG_NAME, 'a')
    for link in direct:
        d_link.append(link.get_attribute('href'))
    for opt_link in d_link:
        if 'speechson.s3.us-west-2.amazonaws.com' in opt_link:
            return image_load(opt_link)
    driver.quit()

def image_load(uri):
    letter_s = ascii_letters + digits
    
    send = requests.get(url=uri)
    image = base64.b64encode(send.content).decode('utf-8')
    
    return {'generated': "realizada con exito", 'image': image}

@cross_origin
@apping.route('/generate/image/prompt=<string:prompt>')
def image_generate(prompt):
    print("Ejecutando api")
    return browser_pag(prompt.replace('+', ' '))


if __name__ == "__main__":
    apping.run(use_reloader=False,port=9080)
