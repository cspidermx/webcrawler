import config
import requests
import bs4 as bs

idGIF = '3IFFozA5bkxIsW0OjZ'
POST_LOGIN_URL = 'https://giphy.com/login'  #This URL will be the URL that your login form points to with the "action" tag.
REQUEST_URL = 'https://giphy.com/gifs/' + idGIF + '/html5'  #This URL is the page you actually want to pull down with requests.
headers = {'user-agent': config.ua, 'referer': POST_LOGIN_URL}

with requests.Session() as session:
    # Retrieve the CSRF token first
    session.get(POST_LOGIN_URL)  # sets cookie
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
    post = session.post(POST_LOGIN_URL, data=payload, headers=headers)
    sauce = session.get(REQUEST_URL)
    soup = bs.BeautifulSoup(sauce.text, "lxml")
    for lnk in soup.find_all('link'):
        if 'rel' in lnk.attrs:
            if 'canonical' in lnk['rel']:
                # https://giphy.com/gifs/hyperrpg-game-reaction-3IFFozA5bkxIsW0OjZ/edit
                sauce = session.get(lnk['href'] + '/edit')
                soup = bs.BeautifulSoup(sauce.text, "lxml")
                # This next part can only work with Selenium because of the pop up window
                for tbx in soup.find_all('input'):
                    print(tbx.attrs)
                    if 'placeholder' in tbx.attrs:
                        if tbx['placeholder'] == 'Add a tag':
                            print(tbx['class'])


