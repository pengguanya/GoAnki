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
