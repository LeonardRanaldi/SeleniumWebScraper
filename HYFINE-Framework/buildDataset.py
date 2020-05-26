from selenium.webdriver.common.keys import Keys
import compareImageName
import scrapeInsta
import scrapeFacebook
import scrapeTwitter
from random import randint
import os
import time
import collections
import writeAndReadFile
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def mergeBigDataset(d1,d2):

    d3 = collections.defaultdict(dict)
    value2 = []
    for key, value in d1.items():
        if key in d2:
            value2 = d2[key]
            valueTot = value + value2
            d3[key] = valueTot


    return d3



#elimina impurità da link face e insta
def cleanTupleList(listTuple):

    for t,f in listTuple:
        if ('?' in t) or ('?' in f):
            tNew = t.split('?')[0]
            fNew = f.split('?')[0]
            listTuple.remove((t,f))
            listTuple.append((tNew, fNew))
        if ('login' in t) or ('hashtag' in t) or ('status' in t):
            listTuple.remove((t, f))
    print(listTuple)
    return listTuple


#prende nuova lista e lista originale e vede se nella lista nuova ci sono degli account noti e li rimuove
def virginListTuple(listTuple, listTupleOriginal):

    for t,f in listTuple:
        if (t,f) in listTupleOriginal:
            listTuple.remove((t, f))


    print(listTuple)
    return listTuple

def virginList(listTuple, listOriginal):

    for t,f in listTuple:
        if t in listOriginal:
            listTuple.remove((t, f))


    print('attento perch e temporale',listTuple)
    return listTuple



def buildDatasetTwitterFacebookNoFeatures(list):

    dict = {}

    for twee, face in list:
        name = twee.split("twitter.com/")[1]
        name = name.split("?")[0]
        name = name.replace("/","")
        dicTw = scrapeTwitter.getInfoTwitter(twee,name)
        if len(dicTw)>1:
            nameTw = dicTw['name']
            imgTw = dicTw['posImg']
            print(imgTw)
            dicFace = scrapeFacebook.getInfoFacebook(face,name)
            if len(dicFace)>1:
                nameFace = dicFace['name']
                imgFace = dicFace['posImg']
                print(imgFace)

                if (nameFace != '') and (imgFace != ''):

                    compareName = compareImageName.similarityName(nameTw, nameFace)

                    dict.setdefault(name, []).append(compareName)

                    compareImg = compareImageName.similarityImage(imgTw, imgFace)

                    dict.setdefault(name, []).append(compareImg)

                    dict.setdefault(name, []).append('1')

        print(dict)

    print(dict)

    return dict


def buildDatasetTwitterManyFeatures(list):

    d = collections.defaultdict(dict)
    tweeListScraped = []


    for twee, face in list:
        if (twee not in tweeListScraped) and (twee != '') and (face != 0) and ('hashtag' not in twee):
            try:
                name = twee.split("twitter.com/")[1]
                name = name.split("?")[0]
                name = name.replace("/","")
                dicTw = scrapeTwitter.getInfoTwitter(twee,name)
                d.setdefault(name, []).append(dicTw)
                tweeListScraped.append(twee)
                print(tweeListScraped)
                print(len(tweeListScraped))
                print(d)
            except Exception:
                print('problema url:', twee)

    writeAndReadFile.writeFile(d, 'newTwitt')
    return d

def buildDatasetFacebookManyFeatures(list):

    d = collections.defaultdict(dict)
    faceListScraped = []
    for twee, face in list:
        if (face not in faceListScraped) and (twee != '') and (face != ''):
            name = twee.split("twitter.com/")[1]
            name = name.split("?")[0]
            name = name.replace("/","")
            dicFb = scrapeFacebook.getInfoFacebook(face,name)
            d.setdefault(name, []).append(dicFb)
            faceListScraped.append(face)
            print(faceListScraped)
            print(d)

    writeAndReadFile.writeFile(d, 'newFace')
    return d



def buildDatasetInstagramManyFeatures(list):

    d = collections.defaultdict(dict)
    instaListScraped = []

    for twee, insta in list:
        if (insta not in instaListScraped) and (twee != '') and (insta != '') and ('/p/' not in insta) and ('/explore/' not in insta):
            try:
                name = twee.split("twitter.com/")[1]
                name = name.split("?")[0]
                name = name.replace("/","")
                dicFb = scrapeInsta.getInfoInsta(insta,name)
                d.setdefault(name, []).append(dicFb)
                instaListScraped.append(insta)
                print(instaListScraped)
                print(d)
            except Exception:
                print('problem link: ', twee)

    writeAndReadFile.writeFile(d, 'newInta')
    return d



def buildDatasetFacebookManyFeaturesTRIPLE(list):

    d = collections.defaultdict(dict)
    faceListScraped = []
    for face, insta, twee in list:
        if (face not in faceListScraped) and (twee != '') and (face != ''):
            try:
                name = twee.split("twitter.com/")[1]
                name = name.split("?")[0]
                name = name.replace("/","")
                dicFb = scrapeFacebook.getInfoFacebook(face,name)
                d.setdefault(name, []).append(dicFb)
                faceListScraped.append(face)
                print(faceListScraped)
                print(d)
            except Exception:
                print('problema al link ',face)

    writeAndReadFile.writeFile(d, 'newFace')
    return d



def mergeDatasetTwitterFacebook(nameTw, nameFb, nameDsFinal):

    dsTw = writeAndReadFile.readFile(nameTw)
    dsFb = writeAndReadFile.readFile(nameFb)

    dsFinal = mergeBigDataset(dsTw,dsFb)

    writeAndReadFile.writeFile(dsFinal,nameDsFinal)

    return 0



def twMancanti(listTwFb, listTwInst):

    listTwMancanti = []
    for tw, inst in listTwInst:
        f = 0
        for tw1, fb in listTwFb:
            if tw == tw1:
                f = 1
        if f == 0:
            tuple = (tw, '')
            listTwMancanti.append(tuple)
    print(listTwMancanti)
    return listTwMancanti


def mancantiFields(listTuop):

    listMancanti = []
    for tw, social in listTuop:
        if len(social)<1:
            tuple = (tw, social)
            listMancanti.append(tuple)
    print(listMancanti)
    return listMancanti



#prende url di twitter e cerca corrispondenza in facebook tramite google dorks
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


def getFacebookCorrespondence(url):


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

    driver.get('http://www.google.com')

    search = driver.find_element_by_name('q')
    #searchText = name+' [site:facebook.com]'
    searchText = name + ' facebook'
    search.send_keys(searchText)
    search.send_keys(Keys.RETURN)
    time.sleep(45)

    try:
        results = driver.find_element_by_id('search')
        first = results.find_elements_by_class_name('g')[1]
        firstA = first.find_elements_by_tag_name('a')[0]
        linkFb = firstA.get_attribute('href')
        if 'facebook' not in linkFb:
            linkFb = ''
        if len(linkFb) > 40:
            linkFb = ''
        if 'tags' in linkFb:
            linkFb = ''
        if 'posts' in linkFb:
            linkFb = ''
        if 'public' in linkFb:
            linkFb = ''
    except Exception:
        print('not found')
        linkFb = ''


    return linkFb


