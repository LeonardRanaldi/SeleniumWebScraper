import os
import time
from random import randint
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys






chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
#driver = webdriver.Chrome(chromedriver)


def getNewProfileTwitter(url):

    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    listNew = []

    time.sleep(2)

    try:
        driver.execute_script("window.scrollTo(0,1000)")
        boxUsers = driver.find_element_by_class_name('RelatedUsers')
        print(boxUsers)
        relatedUsers = boxUsers.find_element_by_class_name('RelatedUsers-users')
        print(relatedUsers)
        content = relatedUsers.find_elements_by_class_name('content')
        print(content)

        for elem in content:
            a = elem.find_element_by_tag_name('a')
            print(a.get_attribute('href'))

            listNew.append(a.get_attribute('href'))

    except Exception:
        print('Problemm')


    if len(listNew) == 0:
        listNew = ['']
    for numProfile in range(0,20):

        print(len(listNew))
        randomProfile = randint(1,len(listNew)-1)
        print(randomProfile)
        print(listNew[randomProfile])
        driver.execute_script("window.open('');")
        #switch new window
        driver.switch_to.window(driver.window_handles[1])
        driver.get(listNew[randomProfile])

        try:
            boxUsers = driver.find_element_by_class_name('RelatedUsers')
            relatedUsers = boxUsers.find_element_by_class_name('RelatedUsers-users')
            content = relatedUsers.find_elements_by_class_name('content')

            for elem in content:
                a = elem.find_element_by_tag_name('a')
                newLink = a.get_attribute('href')
                if newLink not in listOneFinale:
                    listNew.append(a.get_attribute('href'))
            print(listNew)

        except Exception:
            print('Problemm')

        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)

    driver.close()

    listNew = list(set(listNew))

    return listNew



#prende url di twitter e cerca corrispondenza in facebook tramite google dorks
def getFacebookCorrespondence(url):


    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    time.sleep(2)

    try:

        info_profile = driver.find_element_by_class_name('ProfileSidebar')

        profileName = info_profile.find_element_by_class_name('ProfileHeaderCard-name')
        name = profileName.find_element_by_tag_name('a').text

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
        name = emoji_pattern.sub(r'', name)
        name = name.replace("#","")
        name = name.replace("\n","")


        try:
            linkTextFace = info_profile.find_element_by_class_name('ProfileHeaderCard-url').text
        except Exception:
            linkTextFace = ''

    except Exception:
        print('Exp')

    #driver.close()

    if 'face' in linkTextFace:
        print(linkTextFace)
        linkFace = info_profile.find_element_by_class_name('ProfileHeaderCard-url')
        hrefFace = linkFace.find_element_by_tag_name('a').get_attribute('href')
        driver.get(hrefFace)
        time.sleep(2)
        linkFace = driver.current_url

    else:

        driver.get('http://www.google.com')

        search = driver.find_element_by_name('q')
        searchText = name+' [site:facebook.com]'
        #searchText = name + ' facebook'
        search.send_keys(searchText)
        search.send_keys(Keys.RETURN)
        time.sleep(5)  # sleep for 5 seconds so you can see the results

        try:
            results = driver.find_element_by_id('search')
            first = results.find_elements_by_class_name('g')[0]
            firstA = first.find_elements_by_tag_name('a')[0]
            linkFace = firstA.get_attribute('href')
            if len(linkFace) > 55:
                linkFace = ''
        except Exception:
            print('not found')
            linkFace = ''

            if ('Informazioni su questa pagina' in driver.page_source):

                try:
                    driver.get('https://duckduckgo.com')
                    search = driver.find_element_by_name('q')
                    searchText = name + ' facebook'
                    search.send_keys(searchText)
                    search.send_keys(Keys.RETURN)
                    results = driver.find_element_by_id('links')
                    link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
                    linkFace = link
                    time.sleep(5)  # sleep for 5 seconds so you can see the results

                except Exception:
                    print('not found')
                    linkFace = ''

    print(linkFace)

    if '/public/' in linkFace:

        driver.close()
        return 0

    if '?' in linkFace:
        linkFace = linkFace.split('?')[0]


    toupleTwitterFace = (url, linkFace)

    driver.close()


    return toupleTwitterFace


#prende url di twitter e cerca corrispondenza in facebook tramite google dorks
def getFacebookAndInstaCorrespondence(url):


    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    time.sleep(2)

    try:

        info_profile = driver.find_element_by_class_name('ProfileSidebar')

        profileName = info_profile.find_element_by_class_name('ProfileHeaderCard-name')
        name = profileName.find_element_by_tag_name('a').text

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
        name = emoji_pattern.sub(r'', name)
        name = name.replace("#","")
        name = name.replace("\n","")


        try:
            linkTextFace = info_profile.find_element_by_class_name('ProfileHeaderCard-url').text
        except Exception:
            linkTextFace = ''

    except Exception:
        print('Exp')
        linkTextFace = ''

    #driver.close()

    if len(name)>2:

        driver.get('http://www.google.com')

        search = driver.find_element_by_name('q')
        #searchText = name+' [site:facebook.com]'
        searchText = name + ' facebook'
        search.send_keys(searchText)
        search.send_keys(Keys.RETURN)
        time.sleep(5)  # sleep for 5 seconds so you can see the results

        try:
            results = driver.find_element_by_id('search')
            first = results.find_elements_by_class_name('g')[0]
            firstA = first.find_elements_by_tag_name('a')[0]
            linkFace = firstA.get_attribute('href')
            if len(linkFace) > 55:
                linkFace = ''
        except Exception:
            print('not found')
            linkFace = ''

            if ('Informazioni su questa pagina' in driver.page_source):

                try:
                    driver.get('https://duckduckgo.com')
                    search = driver.find_element_by_name('q')
                    searchText = name + ' facebook'
                    search.send_keys(searchText)
                    search.send_keys(Keys.RETURN)
                    results = driver.find_element_by_id('links')
                    link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
                    linkFace = link
                    time.sleep(5)  # sleep for 5 seconds so you can see the results

                except Exception:
                    print('not found')
                    linkFace = ''
    else:
        linkFace = ''

    print(linkFace)

    if '/public/' in linkFace:
        linkFace = ''

    if '?' in linkFace:
        linkFace = linkFace.split('?')[0]



    toupleTwitterFace = (url, linkFace)

    if len(name)>2:

        driver.get('http://www.google.com')

        search = driver.find_element_by_name('q')
        searchText = name+' instagram.com'
        search.send_keys(searchText)
        search.send_keys(Keys.RETURN)
        time.sleep(5)  # sleep for 5 seconds so you can see the results

        try:
            results = driver.find_element_by_id('search')
            first = results.find_elements_by_class_name('g')[0]
            firstA = first.find_elements_by_tag_name('a')[0]
            linkInsta = firstA.get_attribute('href')
            if len(linkInsta) > 55:
                linkInsta = ''
            if 'tags' in linkInsta:
                linkInsta = ''
        except Exception:
            print('not found')
            linkInsta = ''

        if ('Informazioni su questa pagina' in driver.page_source):

            try:
                driver.get('https://duckduckgo.com')
                search = driver.find_element_by_name('q')
                searchText = name + ' instagram.com'
                search.send_keys(searchText)
                search.send_keys(Keys.RETURN)
                results = driver.find_element_by_id('links')
                link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
                linkInsta = link
                time.sleep(5)  # sleep for 5 seconds so you can see the results
                # results = driver.find_element_by_id('links_wrapper')
                # results1 = results.find_element_by_class_name('results--main')
                # link = results1.find_element_by_id('links')
                # linkInsta = link.find_element_by_id('r1-0').text
            except Exception:
                print('not found')
                linkInsta = ''

            print(linkInsta)

        if ('/public/' in linkInsta) or ('explore' in linkInsta) or ('/p/' in linkInsta) or (linkInsta == 'https://www.instagram.com/'):

            linkInsta = ''

        if '?hl' in linkInsta:
            linkInsta = linkInsta.split('?hl')[0]

        if 'instagram' not in linkInsta:
            print('link errato', linkInsta)
            linkInsta = ''

        if linkInsta == 'https://www.instagram.com/':
            linkInsta = ''
    else:
        linkInsta = ''



    toupleTwitterInsta = (url, linkInsta)

    driver.close()


    return toupleTwitterFace,toupleTwitterInsta






#prende url di twitter e cerca corrispondenza in Insta tramite google dorks
def getInstaCorrespondence(url):


    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    time.sleep(2)

    try:

        info_profile = driver.find_element_by_class_name('ProfileSidebar')

        profileName = info_profile.find_element_by_class_name('ProfileHeaderCard-name')
        name = profileName.find_element_by_tag_name('a').text

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
        name = emoji_pattern.sub(r'', name)
        name = name.replace("#","")
        name = name.replace("\n","")


        try:
            linkTextInsta = info_profile.find_element_by_class_name('ProfileHeaderCard-url').text
        except Exception:
            linkTextInsta = ''

    except Exception:
        print('Exp')

    #driver.close()

    if 'insta' in linkTextInsta:
        print(linkTextInsta)
        linkInsta = info_profile.find_element_by_class_name('ProfileHeaderCard-url')
        hrefInsta = linkInsta.find_element_by_tag_name('a').get_attribute('href')
        driver.get(hrefInsta)
        time.sleep(2)
        linkInsta = driver.current_url

    else:

        driver.get('http://www.google.com')

        search = driver.find_element_by_name('q')
        searchText = name+' [site:instagram.com]'
        search.send_keys(searchText)
        search.send_keys(Keys.RETURN)
        time.sleep(5)  # sleep for 5 seconds so you can see the results

        try:
            results = driver.find_element_by_id('search')
            first = results.find_elements_by_class_name('g')[0]
            firstA = first.find_elements_by_tag_name('a')[0]
            linkInsta = firstA.get_attribute('href')
            if len(linkInsta) > 55:
                linkInsta = ''
            if 'tags' in linkInsta:
                linkInsta = ''
        except Exception:
            print('not found')
            linkInsta = ''

        if ('Informazioni su questa pagina' in driver.page_source):

            try:
                driver.get('https://duckduckgo.com')
                search = driver.find_element_by_name('q')
                searchText = name + ' instagram.com'
                search.send_keys(searchText)
                search.send_keys(Keys.RETURN)
                results = driver.find_element_by_id('links')
                link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
                linkInsta = link
                time.sleep(5)  # sleep for 5 seconds so you can see the results
                # results = driver.find_element_by_id('links_wrapper')
                # results1 = results.find_element_by_class_name('results--main')
                # link = results1.find_element_by_id('links')
                # linkInsta = link.find_element_by_id('r1-0').text
            except Exception:
                print('not found')
                linkInsta = ''

    print(linkInsta)

    if ('/public/' in linkInsta) or ('explore' in linkInsta) or ('/p/' in linkInsta) or (linkInsta == 'https://www.instagram.com/'):

        linkInsta = ''
        driver.close()
        return 0

    if '?hl' in linkInsta:
        linkInsta = linkInsta.split('?hl')[0]

    if 'instagram' not in linkInsta:
        print('link errato', linkInsta)
        linkInsta = ''

    toupleTwitterInsta = (url, linkInsta)

    driver.close()


    return toupleTwitterInsta

#prende lista touple e ritorna lista con el touple convertiti
def reverseTouple(listT):

    listReversed = []

    for a,b in listT:

        touple = (b, a)
        listReversed.append(touple)

    print(listReversed)
    return listReversed


#prende url di insta e cerca corrispondenza in Tweeter tramite google dorks
def getTweetCorrespondenceFromInsta(url):


    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    time.sleep(2)

    try:
        header = driver.find_element_by_tag_name('header')
        description_container = header.find_element_by_class_name('-vDIg')
        profileName = description_container.find_element_by_class_name('rhpdm').text


    except Exception:
        print('Exp')
        return 0

    #driver.close()

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
    profileName = emoji_pattern.sub(r'', profileName)

    driver.get('http://www.google.com')

    search = driver.find_element_by_name('q')
    searchText = profileName+' twitter'
    search.send_keys(searchText)
    search.send_keys(Keys.RETURN)
    time.sleep(5)  # sleep for 5 seconds so you can see the results

    try:
        results = driver.find_element_by_id('search')
        first = results.find_elements_by_class_name('g')[0]
        firstA = first.find_elements_by_tag_name('a')[0]
        linkTw = firstA.get_attribute('href')
        if len(linkTw) > 55:
            linkTw = ''
        if 'tags' in linkTw:
            linkTw = ''
    except Exception:
        print('not found')
        linkTw = ''

    if ('Informazioni su questa pagina' in driver.page_source):

        try:
            driver.get('https://duckduckgo.com')
            search = driver.find_element_by_name('q')
            searchText = profileName + ' twitter.com'
            search.send_keys(searchText)
            search.send_keys(Keys.RETURN)
            results = driver.find_element_by_id('links')
            link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
            linkTw = link
            time.sleep(5)  # sleep for 5 seconds so you can see the results

        except Exception:
            print('not found')
            linkTw = ''

    print(linkTw)

    if ('/hashtag/' in linkTw) or ('explore' in linkTw):

        linkTw = ''
        driver.close()
        return 0

    if 'twi' not in linkTw:
        linkTw = ''

    if '?lang' in linkTw:
        linkTw = linkTw.split('?lang')[0]

    toupleTwInsta = (linkTw, url)

    driver.close()


    return toupleTwInsta

#build dict from list of touple
def listTouleToDict(listT):

    test = dict(listT)
    print(test)
    return test


#prende url di insta e cerca corrispondenza in Face tramite google dorks
def getFaceCorrespondenceFromInsta(url):


    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    time.sleep(1)

    try:
        header = driver.find_element_by_tag_name('header')
        description_container = header.find_element_by_class_name('-vDIg')
        profileName = description_container.find_element_by_class_name('rhpdm').text


    except Exception:
        print('Exp')
        return 0

    #driver.close()

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
    profileName = emoji_pattern.sub(r'', profileName)

    driver.get('http://www.google.com')

    search = driver.find_element_by_name('q')
    searchText = profileName+' facebook'
    search.send_keys(searchText)
    search.send_keys(Keys.RETURN)
    time.sleep(1)  # sleep for 5 seconds so you can see the results

    try:
        results = driver.find_element_by_id('search')
        first = results.find_elements_by_class_name('g')[0]
        firstA = first.find_elements_by_tag_name('a')[0]
        linkFb = firstA.get_attribute('href')
        if len(linkFb) > 55:
            linkFb = ''
        if 'tags' in linkFb:
            linkTw = ''
    except Exception:
        print('not found')
        linkFb = ''

    if ('Informazioni su questa pagina' in driver.page_source):

        try:
            driver.get('https://duckduckgo.com')
            search = driver.find_element_by_name('q')
            searchText = profileName + ' facebook'
            search.send_keys(searchText)
            search.send_keys(Keys.RETURN)
            results = driver.find_element_by_id('links')
            link = results.find_element_by_id('r1-0').find_element_by_class_name('result__a').get_attribute('href')
            linkFb = link
            time.sleep(1)  # sleep for 5 seconds so you can see the results

        except Exception:
            print('not found')
            linkFb = ''

    print(linkFb)

    if ('public' in linkFb) or ('explore' in linkFb):

        linkFb = ''
        driver.close()
        return 0

    if 'face' not in linkFb:
        linkFb = ''

    if '?lang' in linkFb:
        linkFb = linkFb.split('?')[0]

    toupleFbInsta = (linkFb, url)

    driver.close()


    return toupleFbInsta

#input lista non vergine output lista vergine
def makeVirginList(listNoVirgin):

    for el in listNoVirgin:
        if el in listOneFinale:
            listNoVirgin.remove(el)

    print(listNoVirgin)
    return listNoVirgin

