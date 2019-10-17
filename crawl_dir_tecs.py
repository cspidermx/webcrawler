import bs4 as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import time


def processurl(url):
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

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.NAME, "idinstitucion")))
    except TimeoutException:
        pass
    inst = Select(driver.find_element_by_name("idinstitucion"))
    # elem = driver.find_element_by_name("idinstitucion")
    tot = len(inst.options)
    f = open('workfile.csv', 'w')
    for i in range(1, len(inst.options)):
        inst.select_by_index(i)
        try:
            wait = WebDriverWait(driver, 30)
            wait.until(EC.visibility_of_element_located((By.ID, "telefonos")))
        except TimeoutException:
            pass
        data = driver.page_source
        soup = bs.BeautifulSoup(data, "lxml")
        for dv in soup.find_all('div'):
            if 'id' in dv.attrs:
                if dv['id'] == 'datos':
                    f.write(dv.find_all('font')[0].get_text() + '\n')
                    print('({}/{})'.format(i, tot), dv.find_all('font')[0].get_text())
                    tbl = dv.find_all('table')
                    for row in tbl[0].find_all('tr'):
                        line = ''
                        for dt in row.find_all('td'):
                            line = line + str(dt.get_text()).replace(',', '.') + ','
                        line = line[:-1]
                        # print(line)
                        f.write(line + '\n')
        inst.select_by_index(0)
        time.sleep(5)
        # inst.deselect_by_index(i)
    f.close()


baseURL = 'http://intranet.dgest.gob.mx/telecom/directorio/'
processurl(baseURL)
