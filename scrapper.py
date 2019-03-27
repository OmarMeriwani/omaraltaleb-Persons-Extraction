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
def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element

Page1 = urlopen(url=url1,data=None)

Page1 = BeautifulSoup(Page1,features="html5lib")
#print(elements)
headers = []
headersAll = []
paragraphs = []
hdrs = Page1.find_all(lambda tag: tag and tag.name.startswith("h1"))
texts = Page1.find_all(lambda tag: tag and tag.name.startswith("p"))
for text in texts:
    cleanString = re.sub('[\n]', '', strip_tags(str(text)))
    paragraphs.append(cleanString)
for header in hdrs:
    cleanString = re.sub('[\n0-9-]', '', strip_tags(str(header)))
    if cleanString.strip() != '':
        headersAll.append(header)
        headers.append(cleanString)
lines = str(Page1.get_text()).split('\n')
prev = ''
for i in range(0,len(lines)-1):
    line = lines[i]
    headerfound = False
    for h in headers:
        if h[:10] in line[:15] and len(line) < 50 and  prev == '' and str(lines[i+2]).strip() == '':
            print('[HEADER]', line)
            print('[HEADERTEXT]', h)
            headerfound = True
            break
    if headerfound == False:
        print('[PARAGRAPH]',line)
    prev = ''
