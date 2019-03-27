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
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    # print(html)
    s.feed(html)
    return s.get_data()
Page1 = urlopen(url='http://www.dr-omaraltaleb.com/KOTOB/maosoaa/index.htm', data=None)
Page1 = BeautifulSoup(Page1, features="html5lib")
links = Page1.find_all(lambda tag: tag and tag.name.startswith("a"))
links2 = []
for link in links:
    cleanString = re.sub('[\n0-9-]', '', strip_tags(str(link)))
    if  'حرف' in cleanString:
        url = 'http://www.dr-omaraltaleb.com/KOTOB/maosoaa/' + link['href']
        print(cleanString, url )
        links2.append(url)