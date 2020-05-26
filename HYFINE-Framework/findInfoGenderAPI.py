import os
import time
import correctURL
from random import randint
from selenium import webdriver
import urllib.request





chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver





def getInfoGenderAPI(url, social):


    driver = webdriver.Chrome(chromedriver)



    driver.get('https://genderapi.io/'+social)

    inputBar = driver.find_element_by_class_name('input')
    inputBar.send_keys(url)


    driver.find_element_by_class_name('input-group-append').click()

    time.sleep(2)

    dataRes = driver.find_element_by_tag_name('code').text


    if ('user not found' in dataRes) or ('errno' in dataRes):
        driver.quit()
        print(dataRes)
        return {}

    time.sleep(2)

    if 'errmsg' in dataRes:
        driver.quit()
        print(dataRes)
        return {}

    if '{' not in dataRes:
        driver.quit()
        return {}


    second = dataRes.split('{')[1]
    dat = second.replace('}','')
    datList = dat.split(',')



    driver.quit()

    dictData = {}
    try:
        for elem in datList:
            if (':0' not in elem) and ('null' not in elem):
                elem = elem.replace('"', '')
                listElem = elem.split(":")
                dictData[listElem[0]] = listElem[1]
    except Exception:
        print('problem find info')
        return {}

        #print(dictData)


    return dictData



#getInfoGenderAPI('https://www.facebook.com/matteorenziuff', 'get-facebook-gender')


