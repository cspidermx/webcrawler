import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

url = 'https://129.158.112.190/dv/ui/home.jsp'

firefox_options = ffOptions()
firefox_options.set_headless(headless=True)
firefox_driver = os.getcwd() + "\\geckodriver.exe"
driver = webdriver.Firefox(firefox_options=firefox_options, executable_path=firefox_driver)
# https://github.com/mozilla/geckodriver/releases
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "btn_login")))
user = driver.find_element_by_id("idUser")
driver.execute_script("arguments[0].setAttribute('value', '')", user)
pasw = driver.find_element_by_id("idPassword")
driver.execute_script("arguments[0].setAttribute('value', '')", pasw)
btnlgn = driver.find_element_by_id("btn_login")
btnlgn.click()
wait = WebDriverWait(driver, 60)
wait.until(EC.visibility_of_element_located((By.ID, "openNavMenuBtnSet")))
btnnav = driver.find_element_by_id("openNavMenuBtnSet")
btnnav.click()
navitems = driver.find_elements_by_class_name("nav-items")
for itm in navitems:
    if itm.text == 'Datos' or itm.text == 'Data':
        itm.click()
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oj-table-body-row")))
tabla = driver.find_element_by_class_name("oj-table-body")
for rw in tabla.find_elements_by_xpath('.//tr'):
    hover = ActionChains(driver).move_to_element(rw)
    hover.perform()
    actionChains = ActionChains(driver)
    actionChains.context_click(rw).perform()
    actionChains = ActionChains(driver)
    actionChains.send_keys(Keys.ARROW_UP).send_keys(Keys.ARROW_UP).perform()
    actionChains = ActionChains(driver)
    actionChains.send_keys(Keys.ENTER).perform()
    time.sleep(60)
    actionChains = ActionChains(driver)
    actionChains.send_keys(Keys.ENTER).perform()
driver.close()
