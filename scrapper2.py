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
import csv

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

def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


'''Defining URLS'''
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
    print(CurrentName)
    prevText = ''
    beginning = True
    NextName = None
    node2 = None
    for i in range(0, num):
        if node != None:
            if re.sub('[\n]', '', strip_tags(str(node))) == "الموسوعة":
                break
            node2 = node.find_previous('h1')
            if beginning == True:
                beginning = False
            else:
                NextName = re.sub('[\n]', '', strip_tags(str(node2)))

            if (CurrentName != NextName and NextName != 'None' and NextName != None):
                #print('Names:', CurrentName, NextName)
                break
            node = node.find_next(type)
        result = result + prevText
        prevText = re.sub('[\n]', '', strip_tags(str(node)))
    return result

def getAllLinks():
    Page1 = urlopen(url='http://www.dr-omaraltaleb.com/KOTOB/maosoaa/index.htm', data=None)
    Page1 = BeautifulSoup(Page1, features="html5lib")
    links = Page1.find_all(lambda tag: tag and tag.name.startswith("a"))
    links2 = []
    for link in links:
        cleanString = re.sub('[\n0-9-]', '', strip_tags(str(link)))
        if 'حرف' in cleanString:
            url = 'http://www.dr-omaraltaleb.com/KOTOB/maosoaa/' + link['href']
            print(cleanString, url)
            links2.append(url)
    return links2
def ArchivePage(url1):
    Page1 = urlopen(url=url1, data=None)
    Page1 = BeautifulSoup(Page1, features="html5lib")
    # print(elements)
    headers = []
    headersAll = []
    paragraphs = []
    hdrs = Page1.find_all(lambda tag: tag and tag.name.startswith("h1"))
    with open('OmarAlTalebSheet.csv', 'a', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['cleanString', 'tokens', 'numbers', 'IsDeathYear', 'content', 'sentences', 'events'])
        for header in hdrs:
            print(header.next_element.name)
            foundNext = False
            content = ''
            cleanString = re.sub('[\n0-9-]', '', strip_tags(str(header)))
            stringwithnumbers = re.sub('[\n]', '', strip_tags(str(header)))
            if cleanString.strip() != '':
                content = getNextAdjacent(20, header, 'p')
                content = content.replace(u'\xa0',u'')
                headersAll.append(header)
                headers.append(cleanString)
                IsDeathYear = False
                if 'ت' in cleanString.split(' '):
                    IsDeathYear = True
                tokens = [s for s in cleanString.split(' ') if s != '' and s != 'ت']
                sentences = re.split(r"\.|\:|\n|\,", content)
                events = [re.split(r'([0-9]+)',s) for s in sentences if s != '']
                numbers = re.findall(r'\d+', stringwithnumbers)
                print('NUMBERS',numbers)
                print('HEADER', cleanString)
                print('TOKENIZED', tokens)
                print('DEAD', IsDeathYear)
                print('CONTENT', content)
                print('SENTENCES', sentences)
                print('EVENTS', events)
                row = [cleanString, tokens, numbers, IsDeathYear, content, sentences, events]
                writer.writerow(row)
    csvFile.close()
links  = getAllLinks()
for link in links:
    ArchivePage(link)