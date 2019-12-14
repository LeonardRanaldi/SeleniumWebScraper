import os
import time
from random import randint
from selenium import webdriver
import urllib.request
from selenium.webdriver import ActionChains
import re





chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
PATH = 'img/instagram/'



def extract_posts(url):

    driver = webdriver.Chrome(chromedriver)

    driver.get(url)

    posts = []

    post = {
        'user_screen_name': None,
        'user_name': None,
        'text': None,
        'likes': 0,
        'shares': 0,
        'comments':0
    }

    time.sleep(2)

    if url[-1] == '/':
        url = url[:-1]
    profileName = url.split('.com/')[1]
    #print(profileName)

    contPhoto = driver.find_element_by_class_name('_2z6nI')


    photos = contPhoto.find_elements_by_class_name('_9AhH0')
    numPostInPage = len(photos)

    if numPostInPage > 5:
        numPostInPage = 5
    if numPostInPage < 1:
        return {}
    try:

        for i in range(0, numPostInPage):

            try:
                post['user_name'] = profileName
                photo = contPhoto.find_elements_by_class_name('_9AhH0')[i]
                photo.click()
                time.sleep(2)
                text = driver.find_element_by_class_name('C4VMK').text
                text = text.replace('\n','').replace(profileName,'')[:-3].replace('Verificato','')
                #print(text)
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
                                           u"\u2063"
                                           "]+", flags=re.UNICODE)
                text = emoji_pattern.sub(r'', text)
                post['text'] = text
                post['user_screen_name'] = profileName
                time.sleep(2)
                # numLike = driver.find_element_by_class_name('Nm9Fw').text
                # numLike = re.findall(r'\d+', numLike)[0]
                # print(numLike)
                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
            except Exception:
                print('problem to open post', i)
            try:

                element_to_hover_over = contPhoto.find_element_by_class_name('qn-0x')
                hover = ActionChains(driver).move_to_element(element_to_hover_over)
                hover.perform()
                logoHover = element_to_hover_over.text

                likes = logoHover.split()[0]
                comments = logoHover.split()[1]
                if (',' in likes) and ('mila' in likes):
                    likes = likes.replace(',','').replace('mila', '00')
                if (',' in likes) and ('mil' in likes):
                    likes = likes.replace(',','').replace('mil', '00000')
                if 'mila' in likes:
                    likes = likes.replace('mila', '000')
                if 'mil' in likes:
                    likes = likes.replace('mil','000000')
                post['likes'] = likes
                if (',' in comments) and ('mila' in comments):
                    comments = comments.replace(',','').replace('mila', '00')
                if (',' in comments) and ('mil' in comments):
                    comments = comments.replace(',','').replace('mil', '00000')
                if 'mila' in comments:
                    comments = comments.replace('mila', '000')
                if 'mil' in comments:
                    comments = comments.replace('mil','000000')
                post['comments'] = comments

            except Exception:
                print('problem with hover')

            #print(post)
            posts.append(post.copy())

    except Exception:
        return {}

    driver.close()
    print(posts)
    return posts



def getInfoInsta(url,nameImg):


    driver = webdriver.Chrome(chromedriver)

    try:
        driver.get(url)
    except Exception:
        driver.close()
        return {}

    dicData = {}

    time.sleep(1)

    contentNotAvailable = 'Spiacenti'
    doLoginAlert = 'Devi effettuare'

    if (contentNotAvailable not in driver.page_source) and (doLoginAlert not in driver.page_source):

        dicData['url'] = url
        dicData['country'] = ''
        header = driver.find_element_by_tag_name('header')
        img_profile = header.find_element_by_tag_name('img').get_attribute('src')

        #download img profile twitter in path img/instagram/
        urllib.request.urlretrieve(img_profile, 'img/instagram/'+nameImg+'Insta.jpg')
        dicData['posImg'] = str(PATH+nameImg+'Insta.jpg')

        try:
            description_container = header.find_element_by_class_name('-vDIg')
            profileName = description_container.find_element_by_class_name('rhpdm').text
            description = description_container.find_element_by_tag_name('span').text

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
            dicData['info'] = emoji_pattern.sub(r'', description.replace('\n', '.'))

            dicData['name'] = emoji_pattern.sub(r'', profileName.replace('\n', '.'))

        except Exception:
            print('description not found')

        try:
            posts = extract_posts(url)

            dicData['interactions'] = posts
        except Exception:
            print('post not found')

        time.sleep(1)

    else:
        print('problem')

    driver.quit()


    print(dicData)

    return dicData



#getInfoInsta('https://www.instagram.com/seencgi/')


#getInfoInsta('https://www.instagram.com/salvosottile_/','salvosottile_')
