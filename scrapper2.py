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


'''Defining URLS'''
url1 = 'http://www.dr-omaraltaleb.com/KOTOB/maosoaa/01alef.htm'
# url1 = urllib.parse.quote(url1)
'''Reading URLs' content'''
def getNextInside(num, node):
    for i in range(0, num):
        print('NEXT ', i, ' FOR ', node)
        node = node.next_element
    return node

def getNextAdjacent(num,node,type):
    result = ''
    CurrentName = re.sub('[\n]', '', strip_tags(str(node)))
    prevText = ''
    for i in range(0, num):

        node2 = node.find_previous('h1')
        NextName = re.sub('[\n]', '', strip_tags(str(node2)))

        if (CurrentName != NextName and NextName != 'None'):
            print('Names:', CurrentName, NextName)
            break
        node = node.find_next(type)
        result = result + prevText
        prevText = re.sub('[\n]', '', strip_tags(str(node)))
    return result


def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


Page1 = urlopen(url=url1, data=None)

Page1 = BeautifulSoup(Page1, features="html5lib")
# print(elements)
headers = []
headersAll = []
paragraphs = []
hdrs = Page1.find_all(lambda tag: tag and tag.name.startswith("h1"))


# texts = Page1.find_all(lambda tag: tag and tag.name.startswith("p"))
# for text in texts:
#    cleanString = re.sub('[\n]', '', strip_tags(str(text)))
#    paragraphs.append(cleanString)
for header in hdrs[:5]:
    print(header.next_element.name)
    foundNext = False
    #current = header.next_element.next_element
    content = ''
    #print('NEXT 5 ELEMENTS', getNextInside(5, header))
    cleanString = re.sub('[\n0-9-]', '', strip_tags(str(header)))
    if cleanString.strip() != '':
        content = getNextAdjacent(20, header, 'p')
        headersAll.append(header)
        headers.append(cleanString)
        print('HEADER', cleanString)
        print('CONTENT', content)
lines = str(Page1.get_text()).split('\n')
prev = ''
