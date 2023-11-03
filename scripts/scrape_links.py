## IMPORT LIBRARIES
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import warnings
warnings.filterwarnings('ignore')
import asyncio
from tqdm.notebook import tqdm



# OPTIONS FOR THE WEBDRIVER

opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
opciones.add_argument('--start-maximized')         # comienza maximizado
#opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
#opciones.add_extension('driver_folder/adblock.crx')       # adblocker
opciones.add_argument('--incognito')




# GET THE URLs OF THE CATEGORIES BESTSELLER

driver = webdriver.Chrome(opciones)
url = 'https://www.amazon.es/gp/bestsellers'

driver.get(url)

time.sleep(2)

# Cookies
aceptar = driver.find_element(By.XPATH, '//*[@id="sp-cc-rejectall-link"]')
aceptar.click()
time.sleep(2)

# Locate the div element by its class and ID
div_element = driver.find_element(By.CLASS_NAME, "_p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv")
link_elements = div_element.find_elements(By.TAG_NAME, 'a')
links = [link.get_attribute('href') for link in link_elements]

print(links)
driver.quit()