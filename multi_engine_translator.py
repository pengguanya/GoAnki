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
        return urllib.parse.urljoin(mainurl, path)

class google:
    def __init__(self, inlang, outlang, theword):
        self.inlang = inlang
        self.outlang = outlang
        self.theword = theword
        # --------------------------
        self.mainurl = 'http://translate.google.com/'
        self.path = 'm'
        self.keywords = strformator.keywordsdict(sl = self.inlang, tl = self.outlang, ie = 'UTF-8', q = self.theword)
        # -------------------------
        self.url = strformator.mergeurl(self.mainurl, self.path)
        self.page = fetch_page.getpage(self.url, self.keywords)

    def getanswer(self):
        mark='class="t0">'
        content = self.page
        if not content:
            print('Load page failed!')
            return None
        else:
            startpos = content.index(mark)
            remaincont = content[content.find(mark)+len(mark):]
            result = remaincont.split('<')[0]
            return result

    def format_inword(self):
        inwordfull = self.theword
        return inwordfull

class linguee:
    def __init__(self, inlang, outlang, theword):
        self.inlang = inlang
        self.outlang = outlang
        self.theword = theword
        # --------------------------
        self.mainurl = 'http://www.linguee.com/'
        self.path = '/'.join(('-'.join((inlang, outlang)), 'search'))
        self.keywords = strformator.keywordsdict(source = 'auto', query = self.theword)
        # -------------------------
        self.url = strformator.mergeurl(self.mainurl, self.path)
        self.page = fetch_page.getpage(self.url, self.keywords)
        self.soup = fetch_page.getsoup(self.page)
        self.genderdict = {
                'masculine' : 'der',
                'feminine'  : 'die',
                'neuter'    : 'das',
                'plural'    : 'die',
                'X'         : ''
                }

    def getinword_frompage(self):
        try:
            inword_tag = self.soup.find('span', class_ = 'dictTerm').string
        except AttributeError as e:
            inword_tag = self.theword
        return inword_tag

    def getanswer(self):
        answer_tag_list = self.soup.find_all('a', class_ = 'dictLink')
        if answer_tag_list and len(answer_tag_list) > 1:
            short_tag_list = answer_tag_list[:2]
            answerstr = '; '.join([tag.string for tag in short_tag_list])
        else:
            try:
                answerstr = answer_tag_list[0].string
            except IndexError:
                answerstr = None
        return answerstr

    def gettype(self):
        try:
            typestr = self.soup.find('span', class_ = 'tag_wordtype').string
        except AttributeError:
            typestr = None
        return typestr

    def format_inword(self):
        inword = self.getinword_frompage()
        typestr = self.gettype()
        if typestr and 'noun' in typestr:
            wordtype = typestr.split(',')[0].strip()
            noun_gender = typestr.split(',')[-1].strip()
            noun_gender_mark = self.genderdict.get(noun_gender, 'X')
            inwordfull = '{} {} ({})'.format(noun_gender_mark, inword, wordtype)
        elif typestr and ',' in typestr:
            wordtype = typestr.split(',')[0].strip()
            inwordfull = '{} ({})'.format(inword, wordtype)
        elif typestr:
            wordtype = typestr
            inwordfull = '{} ({})'.format(inword, wordtype)
        else:
            inwordfull = inword
        return inwordfull

class TransCrawler:
    '''Web Crawler to get the translated word from google translation'''
    def __init__(self, inlang, outlang, theword):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent}
        self.inlang = inlang
