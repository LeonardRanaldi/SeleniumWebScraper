import os
import time
from itertools import islice

import correctURL
from random import randint
from selenium import webdriver
import urllib.request
import findInfoGenderAPI
import re
from bs4 import BeautifulSoup as bs
import requests






chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
PATH = 'img/facebook/'





def extract_posts(page_source):

    soup = bs(page_source, 'html.parser')

    posts = []

    post = {
        'user_screen_name': None,
        'user_name': None,
        'text': None,
        'likes': 0,
        'shares': 0,
        'comments':0
    }


    # try:
    #     divPrincipal = soup.select('div.PagesProfileHomePrimaryColumnPagelet')
    # except Exception:
    #     print('errore dio porco')
    #     return {}
    try:
        divs = soup.select('div._5pbx.userContent._3576')
    except Exception:
        print('dio cane')
        return {}

    for div in divs:
        p = div.find_all('p')
        #print(p)
        #print(type(p))
        p = str(p)
        #print(type(p))
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U0001F1F2-\U0001F1F4"  # Macau flag
                                   u"\U0001F1E6-\U0001F1FF"  # flags
                                   u"\U0001F600-\U0001F64F"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U0001F1F2"
                                   u"\U0001F1F4"
                                   u"\U0001F620"
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   "]+", flags=re.UNICODE)
        p = emoji_pattern.sub(r'', p)
        cleantext = bs(p, 'html.parser').text

        #print(cleantext.replace('[','').replace(']',''))
        cleantext = cleantext.replace('[', '').replace(']', '')
        #text = p[0].text.encode('utf-8')
        post['text'] = cleantext
        posts.append(post.copy())

    numlike = soup.find_all('span', attrs={'class':'_3dlh _3dli'})
    listLike = []
    for el in numlike:
        co = el.find_all('span')
        co = co[0].text
        co = co.replace('.','')
        listLike.append(int(float(co)))

    while len(listLike) < len(posts):
        listLike.append('null')

    i = 0
    for post in posts:
        if post['likes'] == 0:
            post['likes'] = listLike[i]
            i = i+1

    numCom = soup.find_all('a' , attrs={'class':'_3hg- _42ft'})
    listComm = []
    for el in numCom:
        #print(el.text)
        comments = el.text.replace('Commenti: ','').replace('.','')
        listComm.append(int(comments))
    while len(listComm) < len(posts):
        listComm.append('null')

    i = 0
    for post in posts:
        if post['comments'] == 0:
            post['comments'] = listComm[i]
            i = i+1

    numCod = soup.find_all('a' , attrs={'class':'_3rwx _42ft'})
    sharesList = []
    for el in numCod:
        #print(el.text)
        shares = el.text.replace('Condivisioni: ', '').replace('.','')
        sharesList.append(int(shares))

    while len(sharesList) < len(posts):
        sharesList.append('null')

    i = 0
    for post in posts:
        if post['shares'] == 0:
            post['shares'] = sharesList[i]
            i = i+1


    try:

        nome_screen = soup.find_all('a' , attrs={'class':'_64-f'})[0]
        nome = soup.find_all('a', attrs={'class': '_2wmb'})[0]

    except Exception:
        return {}

    for post in posts:
        post['user_screen_name'] = nome_screen.text
        post['user_name'] = nome.text



    print(posts)
    return posts


def getInfoFacebook(url,nameImg):


    driver = webdriver.Chrome(chromedriver)

    urlIni = url

    dictData = {}

    if url[-1] != '/':
        url = url +'/'

    try:
        driver.get(url)
        try:
            sourceUrl = driver.page_source
            posts = extract_posts(sourceUrl)
            dictData['interactions'] = posts
        except Exception:
            print('posts not found')

    except Exception:
        return {}

    try:
        if 'about' not in url:
            driver.get(url+'about')
        else:
            driver.get(url)
    except Exception:
        driver.close()
        return {}


    time.sleep(2)

    contentNotAvailable = ' non è disponibile'
    doLoginAlert = 'Devi effettuare'

    if (contentNotAvailable not in driver.page_source) and (doLoginAlert not in driver.page_source):

        gender = ''
        location = ''
        if 'Uomo' in driver.page_source:
            gender = 'Uomo'
        elif 'uomo' in driver.page_source:
            gender = 'Uomo'
        elif 'Donna' in driver.page_source:
            gender = 'Donna'
        elif 'donna' in driver.page_source:
            gender = 'Donna'

        dictData['gender'] = gender

        dictData['url'] = url

        try:
            fbcover = driver.find_element_by_id('fbProfileCover')
            img_profile = fbcover.find_element_by_tag_name('img').get_attribute('src')
            info_img = fbcover.find_element_by_tag_name('img').get_attribute('alt')
            nameProfile = fbcover.find_element_by_id('fb-timeline-cover-name').text
            dictData['name'] = nameProfile
            print('pro')

            try:
                location = driver.find_element_by_id('hometown').text
                dictData['country'] = location
            except Exception:
                try:
                    location = driver.find_element_by_xpath('//*[@id="PagesProfileAboutInfoPagelet_171674879510966"]/div[2]/div/div/div/div[2]/div[2]/div[2]/span').text
                    print(location)
                    dictData['country'] = location
                except Exception:
                    location = ''
                    dictData['country'] = location

        except Exception:

            try:
                fbSidebar = driver.find_element_by_id('entity_sidebar')
                img_profile = fbSidebar.find_element_by_tag_name('img').get_attribute('src')
                try:
                    location = driver.find_element_by_xpath('//*[@id="PagesProfileAboutInfoPagelet_171674879510966"]/div[2]/div/div/div/div[2]/div[2]/div[2]/span').text
                    print(location)
                    dictData['country'] = location
                except Exception:
                    try:
                        location = driver.find_element_by_id('hometown').text
                        dictData['country'] = location
                    except Exception:
                        location = ''
                        dictData['country'] = location

                try:
                    nameProfile = fbSidebar.find_element_by_id('seo_h1_tag').text
                    dictData['name'] = nameProfile
                except Exception:

                    try:
                        nameProfile = fbSidebar.find_element_by_class_name('_64-f').text
                        dictData['name'] = nameProfile
                    except Exception:
                        dictData['name'] = ''


                try:
                    bio = driver.find_element_by_class_name('_4bl9._5m_o').text
                    emoji_pattern = re.compile("["
                                               u"\U0001F600-\U0001F64F"  # emoticons
                                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                                               u"\U0001F1E6-\U0001F1FF"  # flags
                                               u"\U0001F600-\U0001F64F"
                                               u"\U00002702-\U000027B0"
                                               u"\U000024C2-\U0001F251"
                                               u"\U0001f926-\U0001f937"
                                               u"\U0001F1F2"
                                               u"\U0001F1F4"
                                               u"\U0001F620"
                                               u"\u200d"
                                               u"\u2640-\u2642"
                                               "]+", flags=re.UNICODE)
                    dictData['info'] = emoji_pattern.sub(r'', bio)

                except Exception:
                    bio = ''

            except Exception:
                print('Exception')
                return {}


        ##download img profile twitter in path img/facebook/
        urllib.request.urlretrieve(img_profile, 'img/facebook/' + nameImg + 'Face.jpg')
        dictData['posImg'] = str(PATH+ nameImg + 'Face.jpg')

    else:
        print('page not found')

    driver.quit()

    print(dictData)

    return dictData




print(getInfoFacebook('https://www.facebook.com/foxlifeitalia/', 'prova'))

#driver.quit()

