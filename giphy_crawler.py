import csv
import bs4 as bs
import urllib.request
import json
from dateutil import parser
from dateutil.tz import gettz
from datetime import datetime
import config
import localdb


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


APIKEY = config.APIKEYhyperrpg  # config.APIKEYcspidermx
prefix = 'hyperrpg'
db = 'hypergifsdata.db'

with open(prefix + 'Data.csv') as csvfile:
    ldb = localdb.open(db)
    localdb.cleandata(ldb)
    reader = csv.DictReader(csvfile)
    fieldnames = ['ID', 'GIF URL', 'VIEWS', 'RATING', 'ULD', 'ULM', 'ULY', 'ULT', 'TRD', 'TRM', 'TRY', 'TRT', 'TAGS']
    csvfile2 = open(prefix + 'TAGS.csv', 'w', newline='', encoding='utf-8')
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
        idGIF, idx = __apnd(row['Gif URL'], 'https://media.giphy.com/media/', '/giphy.gif', '', 0)
        gifurl = 'https://giphy.com/gifs/' + idGIF + '/html5'
        apiurl = 'https://api.giphy.com/v1/gifs/' + idGIF + '?api_key=' + APIKEY
        if row['Is Public'] == 'true':
            try:
                sauce = urllib.request.urlopen(apiurl).read()
                metadata = json.loads(sauce)
                if 'data' in metadata:
                    if ('url' not in metadata['data']) or \
                        ('rating' not in metadata['data']) or \
                        ('import_datetime' not in metadata['data']) or \
                        ('trending_datetime' not in metadata['data']):
                            raise ValueError('Not Enough Info')
                else:
                    raise ValueError('Not Enough Info')
                gurl = metadata['data']['url']
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
            except:
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
                                datadict = {'ID': idGIF,
                                            'GIF URL': gurl,
                                            'VIEWS': int(row['View Count']),
                                            'RATING': rating,
                                            'ULD': upldate.day,
                                            'ULM': upldate.month,
                                            'ULY': upldate.year,
                                            'ULT': str(upldate.time()),
                                            'TRD': tredate.day,
                                            'TRM': tredate.month,
                                            'TRY': tredate.year,
                                            'TRT': str(tredate.time()),
                                            'TAGS': mt['content'].replace(', ', '|')}
                                print(datadict['ID'])
                                try:
                                    writer.writerow(datadict)
                                except:
                                    print(datadict['GIF URL'])
                                    datadict['TAGS'] = "ENCODINGERROR"
                                    writer.writerow(datadict)
                                localdb.insert(ldb, datadict)

        else:
            count += int(row['View Count'])
            delgifs += 1
    localdb.close(ldb)
    print({'GIF URL': 'ERASED GIFS', 'VIEWS': count, 'RATING': delgifs})
    writer.writerow({'GIF URL': 'ERASED GIFS', 'VIEWS': count, 'RATING': delgifs})
    csvfile2.close()


