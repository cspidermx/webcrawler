import csv
import bs4 as bs
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def getdynamic(url):
    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    chrome_driver = os.getcwd() + "\\chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    try:
        driver.get(url)
        data = driver.page_source
        driver.close()
        return bs.BeautifulSoup(data, "lxml")
    except:
        return None


def __apnd (txt, frst, scnd, epty, start):
    idx = txt.find(frst, start) + len(frst)
    idx2 = 0
    val = epty
    if idx != -1:
        idx2 = txt.find(scnd, idx)
        if idx2 != -1:
            val = txt[idx:idx2].replace('\\r\\n', '\r\n')
            val = val.replace('\\n', '')
            val = val.strip()
        else:
            idx2 = 0
    return val, idx2


with open('hyperrpg20180411.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = ['GIF URL', 'VIEWS', 'TAGS']
    csvfile2 = open('hyperrpgTAGS.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)
    writer.writeheader()
    gifurl=''
    data = list(reader)
    row_count = len(data)
    csvfile.seek(0)
    reader = csv.DictReader(csvfile)
    i=0
    for row in reader:
        i += 1
        print('(', i, '/', row_count, ')')
        idGIF = __apnd(row['Gif URL'], 'https://media.giphy.com/media/', '/giphy.gif', '', 0)
        # gifurl = row['Gif URL']
        gifurl = 'https://giphy.com/gifs/' + idGIF[0] + '/html5'
        apiurl = 'https://api.giphy.com/v1/gifs/' + idGIF[0] + '?api_key=8I9MzBtUTMD4ObOS7BqF9DqnYS7MGZ9k'
        if row['Is Public'] == 'true':
            try:
                sauce = urllib.request.urlopen(apiurl).read()
            except urllib.error.URLError:
                sauce = None
            if sauce is not None:
                try:
                    # soup = getdynamic(gifurl)
                    sauce = urllib.request.urlopen(gifurl).read()
                    soup = bs.BeautifulSoup(sauce, "lxml")
                except urllib.error.URLError:
                    soup = None
                if soup is not None:
                    exists = "TRUE"
                else:
                    exist = "FALSE"
                # print(idGIF[0], row['View Count'], gifurl, exists)  # Gif URL	Is Public	View Count
                if soup is not None:
                    for mt in soup.find_all('meta'):
                        if 'name' in mt.attrs:
                            if mt['name'] == 'keywords':
                                # ['GIF URL', 'VIEWS', 'TAGS']
                                print({'GIF URL': row['Gif URL'], 'VIEWS': row['View Count'], 'TAGS': mt['content'].replace(', ', '|')})
                                writer.writerow({'GIF URL': row['Gif URL'], 'VIEWS': row['View Count'], 'TAGS': mt['content'].replace(', ', '|')})
                                # print(mt['content'].replace(', ', '|'))
    csvfile2.close()


