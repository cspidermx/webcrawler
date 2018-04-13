import config
import requests
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def opendriver(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    chrome_driver = os.getcwd() + "\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get(url)
    return driver


def setdrivercookies(driver, resp, c):
    dict_resp_cookies = resp.cookies.get_dict()
    response_cookies_browser = [{'name': name, 'value': value} for name, value in dict_resp_cookies.items()]
    c = [driver.add_cookie(c) for c in response_cookies_browser]


def closedriver(driver):
    driver.close()


def getdynamic(driver, url):
    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div._3y9oxKNb4mFKzXjyrg77rZ")))
    driver.implicitly_wait(35)
    data = driver.page_source
    return bs.BeautifulSoup(data, "lxml")

idGIF = '3IFFozA5bkxIsW0OjZ'
POST_LOGIN_URL = 'https://giphy.com/login'  #This URL will be the URL that your login form points to with the "action" tag.
REQUEST_URL = 'https://giphy.com/gifs/' + idGIF + '/html5'  #This URL is the page you actually want to pull down with requests.
headers = {'user-agent': config.ua, 'referer': POST_LOGIN_URL}

with requests.Session() as session:
    # Retrieve the CSRF token first
    session.get(POST_LOGIN_URL)  # sets cookie
    dyndri = opendriver(POST_LOGIN_URL)
    request_cookies_browser = dyndri.get_cookies()
    if 'csrftoken' in session.cookies:
        # Django 1.6 and up
        csrftoken = session.cookies['csrftoken']
    else:
        # older versions
        csrftoken = session.cookies['csrf']
    payload = {
        'email': config.USERgiphy,
        'password': config.PASSgiphy,
        'csrfmiddlewaretoken': csrftoken
    }
    coo = [session.cookies.set(c['name'], c['value']) for c in request_cookies_browser]
    post = session.post(POST_LOGIN_URL, data=payload, headers=headers)
    setdrivercookies(dyndri, post, coo)
    sauce = session.get(REQUEST_URL)
    soup = bs.BeautifulSoup(sauce.text, "lxml")
    for lnk in soup.find_all('link'):
        if 'rel' in lnk.attrs:
            if 'canonical' in lnk['rel']:
                # https://giphy.com/gifs/hyperrpg-game-reaction-3IFFozA5bkxIsW0OjZ/edit
                # sauce = session.get(lnk['href'] + '/edit')
                soup = getdynamic(dyndri, lnk['href'])  # bs.BeautifulSoup(sauce.text, "lxml")
                # This next part can only work with Selenium because of the pop up window
                for tbx in soup.find_all('input'):
                    print(tbx.attrs)
                    if 'placeholder' in tbx.attrs:
                        if tbx['placeholder'] == 'Add a tag':
                            print(tbx['class'])
    closedriver(dyndri)


