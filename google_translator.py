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
