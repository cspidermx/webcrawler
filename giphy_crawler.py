import csv
import bs4 as bs
import urllib.request
import json
from dateutil import parser
from dateutil.tz import gettz
from datetime import datetime


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
    fieldnames = ['GIF URL', 'VIEWS', 'RATING', 'ULD', 'ULM', 'ULY', 'ULT', 'TRD', 'TRM', 'TRY', 'TRT', 'TAGS']
    csvfile2 = open('hyperrpgTAGS.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)
    writer.writeheader()
    gifurl=''
    data = list(reader)
    row_count = len(data)
    csvfile.seek(0)
    reader = csv.DictReader(csvfile)
    i = 0
    count = 0
    delgifs = 0
    tzinfos = {"CST": gettz("America/Mexico_City")}
    for row in reader:
        i += 1
        print('(', i, '/', row_count, ')')
        idGIF = __apnd(row['Gif URL'], 'https://media.giphy.com/media/', '/giphy.gif', '', 0)
        gifurl = 'https://giphy.com/gifs/' + idGIF[0] + '/html5'
        apiurl = 'https://api.giphy.com/v1/gifs/' + idGIF[0] + '?api_key=8I9MzBtUTMD4ObOS7BqF9DqnYS7MGZ9k'
        if row['Is Public'] == 'true':
            try:
                sauce = urllib.request.urlopen(apiurl).read()
                metadata = json.loads(sauce)
                rating = metadata['data']['rating']
                upload = metadata['data']['import_datetime']
                upload = parser.parse(upload, tzinfos=tzinfos).strftime('%d/%m/%Y %H:%M:%S')
                upldate = datetime.strptime(upload, '%d/%m/%Y %H:%M:%S')
                trend = metadata['data']['trending_datetime']
                try:
                    trend = parser.parse(trend, tzinfos=tzinfos).strftime('%d/%m/%Y %H:%M:%S')
                    tredate = datetime.strptime(trend, '%d/%m/%Y %H:%M:%S')
                except:
                    tredate = datetime(2000, 1, 1)
            except urllib.error.URLError:
                sauce = None
                count += int(row['View Count'])
                delgifs += 1
            if sauce is not None:
                try:
                    sauce = urllib.request.urlopen(gifurl).read()
                    soup = bs.BeautifulSoup(sauce, "lxml")
                except urllib.error.URLError:
                    soup = None
                if soup is not None:
                    exists = "TRUE"
                else:
                    exist = "FALSE"

                if soup is not None:
                    for mt in soup.find_all('meta'):
                        if 'name' in mt.attrs:
                            if mt['name'] == 'keywords':
                                # ['GIF URL', 'VIEWS', 'RATING',
                                # 'ULD', 'ULM', 'ULY', 'ULT',
                                # 'TRD', 'TRM', 'TRY', 'TRT',
                                # 'TAGS']
                                print({'GIF URL': row['Gif URL'],
                                       'VIEWS': row['View Count'],
                                       'RATING': rating,
                                       'ULD': upldate.day,
                                       'ULM': upldate.month,
                                       'ULY': upldate.year,
                                       'ULT': str(upldate.time()),
                                       'TRD': tredate.day,
                                       'TRM': tredate.month,
                                       'TRY': tredate.year,
                                       'TRT': str(tredate.time()),
                                       'TAGS': mt['content'].replace(', ', '|')})
                                writer.writerow({'GIF URL': row['Gif URL'],
                                                 'VIEWS': row['View Count'],
                                                 'RATING': rating,
                                                 'ULD': upldate.day,
                                                 'ULM': upldate.month,
                                                 'ULY': upldate.year,
                                                 'ULT': str(upldate.time()),
                                                 'TRD': tredate.day,
                                                 'TRM': tredate.month,
                                                 'TRY': tredate.year,
                                                 'TRT': str(tredate.time()),
                                                 'TAGS': mt['content'].replace(', ', '|')})
        else:
            count += int(row['View Count'])
            delgifs += 1
    print({'GIF URL': 'ERASED GIFS', 'VIEWS': count, 'RATING': delgifs})
    writer.writerow({'GIF URL': 'ERASED GIFS', 'VIEWS': count, 'RATING': delgifs})
    csvfile2.close()

