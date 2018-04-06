import bs4 as bs
import urllib.request

baseURL = 'https://cinemex.com'
sauce = urllib.request.urlopen(baseURL + '/cines').read()
soup = bs.BeautifulSoup(sauce, "lxml")

for cbx in soup.find_all('select'):
    if 'id' in cbx.attrs:
        if cbx['id'] == "cinemas-select-city":
            for opt in cbx.find_all('option'):
                print(opt.text + " - " + opt['value'])
                sauce = urllib.request.urlopen(baseURL + '/cines/' + opt['value']).read()
                soup2 = bs.BeautifulSoup(sauce, "lxml")
                for lis in soup2.find_all('li'):
                    if 'class' in lis.attrs:
                        # print(lis['class'])
                        if lis['class'][0] == "cinema-item":
                            x, y = lis['data-pos'].split(',')
                            addr = lis['data-address']
                            print(x, y, lis.a.text, lis.a.get('href'), addr)
