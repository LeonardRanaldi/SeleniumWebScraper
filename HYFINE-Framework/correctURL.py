import os
import re
import time
from random import randint
#import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException




chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)





def getChannelFromVideoYoutube(url):


    driver = webdriver.Chrome(chromedriver)

    try:
        driver.get(url)
    except Exception:
        driver.get('https://'+url)


    time.sleep(2)

    #video pause

    try:

        videoPause = driver.find_element_by_xpath("//button[@class='ytp-play-button ytp-button']").click()

        time.sleep(3)
    except Exception:
        print('pause')
        pass

    try:
    #click channel
        metaContent = driver.find_element_by_id('meta-contents')
        metaContent.find_element_by_class_name('yt-simple-endpoint').click()

        time.sleep(3)

        urlCurrent = driver.current_url

        time.sleep(3)

    except Exception:
        print('url not retrive')
        urlCurrent = ''
        pass

    try:
        driver.close()

    except Exception:
        pass

    return urlCurrent



#corregge gli URL se sorreggibili altrimenti return 0
def correctUrlChannel(url):

    print(url)


    if 'linktr.ee' in url:

        return url


    if 'm.youtube.com' in url:
        url = url.replace('m.', 'www.')


    if 'www.youtube.com/channel/' in url:
        return url

    if 'www.youtube.com/c/' in url:
        return url

    if 'www.youtube.com/user/' in url:
        return url


    elif 'youtu.be/' in url:

        url = url.replace('youtu.be/', 'https://www.youtube.com/watch?v=')
        print(url)
        url = getChannelFromVideoYoutube(url)

        print('New..',url)

        try:
            driver.close()

        except Exception:
            pass

        return url


    elif 'watch?' in url:
        url = getChannelFromVideoYoutube(url)
        print(url)

        try:
            driver.close()

            time.sleep(5)

        except Exception:
            pass

        time.sleep(3)

        return url


    elif '?view_as' in url:
        url = url.split('?view_as')[0]
        print(url)
        return url

    elif '?app' in url:
        url = url.split('?app')[0]
        print(url)
        return url

    elif '?sub_confirmation=1%2F' in url:
        url = url.split('?sub_confirmation=1%2F')[0]
        print(url)
        return url

    elif '#youtubers' in url:
        return ''

    elif '#youtube'  in url:
        return ''

    elif '#youtubeitalia' in url:
        return ''

    elif 'www.youtube.com/user/' in url:
        return url

    elif len(url) > 60:
        return ''

    elif '' in url:
        return ''

    time.sleep(5)

    return ''


def getLinktr(url):

    listSocial = []

    if 'https://' in url:

        try:
            driver.get(url)
        except Exception:
            pass
    else:
        try:
            driver.get('https://'+url)
        except Exception:
            pass
    try:

        links = driver.find_elements_by_class_name('link')

        for link in links:

            linkA = link.find_element_by_tag_name('a')

            listSocial.append(linkA.get_attribute('href'))
    except Exception:
        pass


    return listSocial

def getSocialFromYoutubeChannel(url):

    listSocial = []

    print('questo è il link....', url)


    if url == '' or url is None:
        print('url nullo...')
        return ''

    if 'linktr.ee' in url:
        listSocial = getLinktr(url)
        return listSocial


    if 'https://' in url:
        try:
            driver.get(url + '/about')
            urlNew = driver.current_url
        except Exception:
            print('-------------> Problem link connect!!', urlNew)
            return ''

    else:
        try:
            driver.get('https://'+url+'/about')
            urlNew = driver.current_url
        except Exception:
            print('-------------> Problem link connect!!', urlNew)
            return ''


    print('questo è il link nuovo ', urlNew)


    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


    time.sleep(randint(2,4))

    try:

        state = driver.find_element_by_id('links-container')

    except Exception:

        print('links container non trovato')
        return ''


    print(state)

    if state is None:
        return ''

    try:
        linkList = state.find_element_by_id('link-list-container')

    #except NoSuchElementException:
    except Exception:
        print('-------------> Problem link container not present!!')
        return ''

    try:

        links = linkList.find_elements_by_tag_name('yt-formatted-string')
        for link in links:

            #substring = ['Instagram', 'INSTAGRAM', 'instagram']

            #if not any(textLink in link.text for textLink in substring):

            print(link.text)

            try:
                link.click()
                # Switch to the new window
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10) 

                listSocial.append(driver.current_url)
                time.sleep(2)
                driver.close()
                # Switch to the old window
                driver.switch_to.window(driver.window_handles[0])
            except Exception:
                print('problema al link', link.text)

    except Exception:
        print('link social non trovati')
        pass

    return listSocial



def getNewChannelsFromChannel(linkUser):

    listNewChannel = []

    if linkUser == '':
        print('link user null')
        return ''
    elif 'https://' not in linkUser:
        linkUser = 'https://'+linkUser

    try:
        driver.get(linkUser)

    except Exception:
        print(linkUser, 'link not found')
        return ''

    try:
        verticalSections = driver.find_elements_by_tag_name('ytd-vertical-channel-section-renderer')

    except Exception:
        print('Vertical Bar non trovata')
        return ''

    for section in verticalSections:

        items = section.find_element_by_id('items')
        channelsInfos = items.find_elements_by_tag_name('ytd-mini-channel-renderer')

        for channel in channelsInfos:

            user = channel.find_element_by_id('channel-info')
            listNewChannel.append(user.get_attribute('href'))

    return listNewChannel




# driver.quit()
