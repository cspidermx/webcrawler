import os
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# firefox_options = ffOptions()
chrome_options = ChOptions()
# firefox_options.set_headless(headless=True)
# firefox_driver = os.getcwd() + "\\geckodriver.exe"
chrome_driver = os.getcwd() + "\\chromedriver.exe"
# driver = webdriver.Firefox(firefox_options=firefox_options, executable_path=firefox_driver)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
url = 'https://giphy.com/login'
driver.get(url)
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.NAME, "email")))
user = driver.find_element_by_name("email")
driver.execute_script("arguments[0].setAttribute('value', '" + config.USERgiphy + "')", user)
passw = driver.find_element_by_name("password")
driver.execute_script("arguments[0].setAttribute('value', '" + config.PASSgiphy + "')", passw)
btnlgn = driver.find_element_by_class_name("form-components__CTAButton-abosvr-3")
btnlgn.click()
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.ID, "upload-avatar")))

i = 0
with open('list.txt') as f:
    for i, l in enumerate(f):
        pass
total = i + 1

i = 1
with open('list.txt', 'r') as file:
    for line in file.readlines():
        url = line.replace('\n', '')
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "_14glt1AeSjnOdEg6jPXf4y")))
        gif = driver.find_element_by_class_name("KRS9L9BsuEdhF-ACKiX8x")
        hover = ActionChains(driver).move_to_element(gif)
        hover.perform()
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "_3VnuN1NZurY9lA0b_kRnUu")))
        btnedit = driver.find_element_by_class_name("_3VnuN1NZurY9lA0b_kRnUu")
        btnedit.click()
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Fx76GcH4nzz12sVCkdN1_")))
        addtag = driver.find_element_by_xpath("(//input[@class='Fx76GcH4nzz12sVCkdN1_ _2-GxqWYNxZ-IXQRDqN-Soq"
                                              " _1bc7yOoPoF9ZAns5laPqC0'])[2]")
        addtag.click()
        addtag.send_keys('themattacevedo')
        addtag.send_keys(' ')
        addtag.send_keys(Keys.ENTER)
        addtag.send_keys(Keys.DELETE)
        time.sleep(5)
        btnclose = driver.find_element_by_xpath("//div[@class='_2yA57V8LtMT5O9b9rPuLM1 ss-delete']")
        btnclose.click()
        print("({}/{})".format(i, total), url)
        i += 1

driver.close()
