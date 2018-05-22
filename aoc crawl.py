import bs4 as bs
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as ffOptions
import time

url = 'https://129.158.112.190/dv/ui/home.jsp'

    # instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
chrome_driver = os.getcwd() + "\\chromedriver.exe"

firefox_options = ffOptions()
firefox_options.set_headless(headless=True)
firefox_driver = os.getcwd() + "\\geckodriver.exe"
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver = webdriver.Firefox(firefox_options=firefox_options, executable_path=firefox_driver)
# https://github.com/mozilla/geckodriver/releases
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "btn_login")))
    # calendarbtn = driver.find_element_by_name("date")
    # for option in calendarbtn.find_elements_by_tag_name('option'):
    #     if option.get_attribute('value') == '20180409':
    #         option.click()  # select() in earlier versions of webdriver
    #         time.sleep(5)
    #         break

data = driver.page_source
driver.close()

soup = bs.BeautifulSoup(data, "lxml")