#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json


class Insta_Image_Links_Scraper:

    def getlinks(self, hashtag, url):

        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        print ('Scraping links with #' + hashtag+"...........")
        for post in data['entry_data']['TagPage'][0]['graphql'
                ]['hashtag']['edge_hashtag_to_media']['edges']:
            image_src = post['node']['thumbnail_resources'][1]['src']
            hs = open(hashtag + '.txt', 'a')
            hs.write(image_src + '\n')
            hs.close()

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        hashtag = 'youtube'
        self.getlinks(hashtag,'https://www.instagram.com/explore/tags/'+ hashtag + '/')


if __name__ == '__main__':
    obj = Insta_Image_Links_Scraper()
    obj.main()
