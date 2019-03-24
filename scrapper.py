import numpy as np
import pandas as pd
import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import nltk
import requests
import urllib.parse
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    #print(html)
    s.feed(html)
    return s.get_data()


'''Defining URLS'''
url1 = 'http://www.dr-omaraltaleb.com/KOTOB/maosoaa/01alef.htm'
#url1 = urllib.parse.quote(url1)
'''Reading URLs' content'''

Page1 = urlopen(url=url1,data=None)

Page1 = BeautifulSoup(Page1,features="html5lib")

headers = []
hdrs = Page1.find_all(lambda tag: tag and tag.name.startswith("h1"))
texts = Page1.find_all(lambda tag: tag and tag.name.startswith("p"))
for text in texts:
    print(strip_tags(str(text)))
for header in hdrs:
    cleanString = re.sub('[\n0-9-]', '', strip_tags(str(header)))
    headers.append(cleanString)
print(headers)
