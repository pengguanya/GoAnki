__author__ = 'PGY'

import sys
import os.path
import re
import requests
import threading
import urllib.parse
from bs4 import BeautifulSoup
from collections import deque

class fetch_page:
    user_agent = 'mozilla/4.0 (compatible; msie 5.5; windows nt)'
    headers = {'user-agent' : user_agent}

    @classmethod
    def getpage(cls, url, keywords):
        try:
            response = requests.get(url, keywords, headers = cls.headers)
            content = response.text
            return content
        except:
            e = sys.exc_info()
            print(e)
            return None

    @classmethod
    def getsoup(cls, content):
        if not content:
            print('Load page failed!')
            return None
        else:
            soup = BeautifulSoup(content, "lxml")
            return soup

class strformator:
    @staticmethod
    def keywordsdict(**kwargs):
        return kwargs

    @staticmethod
    def mergeurl(mainurl, path):
