__author__ = 'PGY'

import sys
import os.path
import re
import requests
import threading

class TransCrawler:
    '''Web Crawler to get the translated word from google translation'''
    def __init__(self, inlang, outlang, theword):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent}
        self.inlang = inlang
        self.outlang = outlang
        self.theword = theword
        self.keywords ={'sl': self.inlang, 'tl': self.outlang, 'ie':'UTF-8', 'q': self.theword}
        self.url = 'http://translate.google.com/m'

    def getPage(self):
        url = self.url
        keywords = self.keywords
        try:
            response = requests.get(url, keywords, headers = self.headers)
            content = response.text
            return content
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def getWord(self):
        mark='class="t0">'
        content = self.getPage()
        if not content:
            print('Load page failed!')
            return None
        else:
            #return content
            startpos = content.index(mark)
            remaincont = content[content.find(mark)+len(mark):]
            result = remaincont.split('<')[0]
            return result

# This function is useful only when multithread is switch off
# Because multithread will destroy the order later
# If set() is slower than O(n), this can be used for the speed purpose
# def del_dups(seq):
#     '''function to delete duplicate while preserve order'''
#     seen = {}
#     newlist = []
#     for item in seq:
#         if item not in seen:
#             seen[item] = True
#             newlist.append(item)
#     return newlist
def html_decode(s):
