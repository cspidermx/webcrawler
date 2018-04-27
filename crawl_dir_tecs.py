import bs4 as bs
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os

def getdynamic(url):
    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-web-security")
    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    chrome_driver = os.getcwd() + "\\chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get(url)

    elem = Select(driver.find_element_by_name("idtipoinstitucion"))
    elem.select_by_value('5')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.NAME, "idinstitucion")))
    inst = Select(driver.find_element_by_name("idinstitucion"))
    elem = driver.find_element_by_name("idinstitucion")
    for i in range(1, len(inst.options)):
        inst.select_by_index(i)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "telefonos")))
        data = driver.page_source
        soup = bs.BeautifulSoup(data, "lxml")
        for dv in soup.find_all('div'):
            if 'id' in dv.attrs:
                if dv['id'] == 'datos':
                    print(dv.find_all('font')[0])
        # inst.deselect_by_index(i)

    data = driver.page_source
    driver.close()

    return bs.BeautifulSoup(data, "lxml")

baseURL = 'http://intranet.dgest.gob.mx/telecom/directorio/'
# try:
sauce = getdynamic(baseURL)
# except:
    # print('Error getting: ', baseURL)
