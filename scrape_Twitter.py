import os
import time
import urllib
from selenium import webdriver
import re
from bs4 import BeautifulSoup as bs




chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
PATH = 'img/twitter/'



def extract_tweets(page_source):

    soup = bs(page_source, 'html.parser')


    tweets = []
    for li in soup.find_all("li", class_='js-stream-item'):

        # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
        if 'data-item-id' not in li.attrs:
            continue

        else:
            tweet = {
                'user_screen_name': None,
                'user_name': None,
                'text': None,
                'shares': 0,
                'likes': 0,
                'comments': 0
            }

            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()

            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_screen_name'] = user_details_div['data-screen-name']
                tweet['user_name'] = user_details_div['data-name']


            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['shares'] = int(retweet_span[0]['data-tweet-stat-count'])

            # Tweet Likes
            like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if like_span is not None and len(like_span) > 0:
                tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])

            # Tweet Replies
            reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
            if reply_span is not None and len(reply_span) > 0:
                tweet['comments'] = int(reply_span[0]['data-tweet-stat-count'])

            tweets.append(tweet)

    return tweets



def getInfoTwitter(url,nameImg):

    driver = webdriver.Chrome(chromedriver)

    try:
        driver.get(url)
    except Exception:
        driver.close()
        return {}

    dicData = {}


    contentNotAvailable = 'non è disponibile'
    doLoginAlert = 'Spiacenti'
    accountPrivate = 'Tweet di questo account sono protetti'
    accountSosp = 'Account sospeso'


    if (contentNotAvailable not in driver.page_source) and (doLoginAlert not in driver.page_source) and (accountPrivate not in driver.page_source) and (accountSosp not in driver.page_source):

        dicData['url'] = url
        try:

            img = driver.find_element_by_class_name('ProfileAvatar')
            img_profile = img.find_element_by_tag_name('img').get_attribute('src')
            info_profile = driver.find_element_by_class_name('ProfileSidebar')


            profileName = info_profile.find_element_by_class_name('ProfileHeaderCard-name')
            name = profileName.find_element_by_tag_name('a').text
            dicData['name'] = name

            try:
                pageSource = driver.page_source
                listTweet = extract_tweets(pageSource)
                dicData['interactions'] = listTweet

            except Exception:
                print('interactions not found')


            try:
                bio = info_profile.find_element_by_class_name('ProfileHeaderCard-bio').text

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
                dicData['info'] = emoji_pattern.sub(r'', bio)


            except Exception:
                dicData['info'] = ''

            try:
                location = info_profile.find_element_by_class_name('ProfileHeaderCard-location').text
                dicData['country'] = location
            except Exception:
                dicData['country'] = ''

        except Exception:
            print('Exception')

        #download img profile twitter in path img/twitter/
        urllib.request.urlretrieve(img_profile, 'img/twitter/'+nameImg+'Twit.jpg')
        dicData['posImg'] = str(PATH+nameImg+'Twit.jpg')

    else:
        print('not found page')

    driver.quit()


    return dicData




#print(getInfoTwitter('https://twitter.com/jeffdean', 'jeffdean'))



#print(getInfoTwitter('https://twitter.com/berlusconi', 'silvio'))