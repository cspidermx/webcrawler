import bs4 as bs
import urllib.request
import os


def getdynamic(url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    chrome_driver = os.getcwd() + "\\chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "sidebar-mycinema")))
    # calendarbtn = driver.find_element_by_name("date")
    # for option in calendarbtn.find_elements_by_tag_name('option'):
    #     if option.get_attribute('value') == '20180409':
    #         option.click()  # select() in earlier versions of webdriver
    #         time.sleep(5)
    #         break

    data = driver.page_source
    driver.close()

    return bs.BeautifulSoup(data, "lxml")


def getmovies(cinelink):
    soup = getdynamic(cinelink)
    for dv in soup.find_all('div'):
        if 'id' in dv.attrs:
            if dv['id'] == 'sidebar-mycinema':
                for movielst in dv.find_all('div'):
                    if 'class' in movielst.attrs:
                        if movielst['class'][0] == 'mycinema-li':
                            movie = movielst.find_all('div')
                            cts = ''
                            for s in movie[0].find_all('span'):
                                cts += s.text + "| "
                            hrs = ''
                            for h in movie[0].find_all('a'):
                                hrs += h.text + ", "
                            print('    - ', movielst.a.text, movielst.span.text, cts, hrs)  # movielst.div.span.text)


baseURL = 'https://cinemex.com'
try:
    sauce = urllib.request.urlopen(baseURL + '/cines').read()
except urllib.error.URLError as e:
    print(e.reason, " -- ", baseURL + '/cines')
soup = bs.BeautifulSoup(sauce, "lxml")

for cbx in soup.find_all('select'):
    if 'id' in cbx.attrs:
        if cbx['id'] == "cinemas-select-city":
            for opt in cbx.find_all('option'):
                print(opt.text + " - " + opt['value'])
                try:
                    sauce = urllib.request.urlopen(baseURL + '/cines/' + opt['value']).read()
                except urllib.error.URLError as e:
                    print(e.reason, " -- ", baseURL + '/cines/' + opt['value'])
                soup2 = bs.BeautifulSoup(sauce, "lxml")
                for lis in soup2.find_all('li'):
                    if 'class' in lis.attrs:
                        if lis['class'][0] == "cinema-item":
                            x, y = lis['data-pos'].split(',')
                            addr = lis['data-address']
                            cine = lis.a.text
                            link = lis.a.get('href')
                            print("  - ", x, y, cine, link, addr)
                            getmovies(baseURL + link)
            break
