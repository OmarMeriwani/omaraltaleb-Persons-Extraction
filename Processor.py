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
from ast import literal_eval
death = ['اعدام','قتل','شنق','','']
preList = ['الشيخ', 'الاستاذ', 'المفتي', 'الفنان', 'الشاعر', '', 'الحاج', 'البروفيسور', 'الملا', 'البطريرك', 'القس',
           'الكاردينال', 'الملك', 'المحافظ', 'السلطان', 'الاسطة', 'الشريف', 'السيد','القاضي']


def compareNames(name1, name2):
    '''
   First and any of the Middle
   First and Last
   First and any Middle and Last
   Pre with Last

   Execlude the Waw
   Replace the initial Lil with Al when the letters after the word are more than 2
   '''
    postList = ['بيك','اغا','افندي','','','','','','']
    familyRelations = ['اخ','اب']
    familyRelations2 = ['عم','خال','نسيب','ابن عم','ابن خال','صديق','زوج','اخت','زوجت','زوجة','ام']
    name1 = list(name1)
    name2 = list(name2)
    if name1[0] == name2[0] and name1[len(name1)-1] == name2[len(name2)-1]:
        return 1

    if name1[0] == name2[0] and name1[len(name1)-1] != name2[len(name2)-1]:
        return 1
    #if name2 in preList:
    #    if name1[0] == name2[1] ||

def normalize(word):
    word = str(word)
    word = word.replace('أ','ا')
    word = word.replace('آ','ا')
    word = word.replace('إ','ا')
    word = word.replace('ـ','')
    word = word.replace('ة','ه')
    word = word.replace('ٌ','')
    word = word.replace('ْ','')
    word = word.replace('ٍ','')
    word = word.replace('ِ','')
    word = word.replace('ٌ','')
    word = word.replace('ً','')
    word = word.replace('َ','')
    word = word.replace(' ','')
    return word
'''0, 1.cleanString, 2.tokens, 3.numbers, 4.IsDeathYear, 5.content, 6.sentences, 7.events'''
df = pd.read_csv('OmarAlTalebSheet.csv',encoding='utf-8',header=0)
print(df.head())
#df['tokens'] = df['tokens'].apply(literal_eval)
#df['numbers'] = df['numbers'].apply(literal_eval)
#df['sentences'] = df['sentences'].apply(literal_eval)
#df['events'] = df['events'].apply(literal_eval)
def unique(list1):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return  unique_list


NameTokens = []
NamesDataset = []
for i in range(0,len(df)):
    personName = str(df.loc[i].values[0])
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    NameTokens.append(tokens)
    for t in tokens:
        NameTokens.append(t)
NameTokens = unique(NameTokens)
print(len(NameTokens))
for i in range(0,len(df)):
    personName = str(df.loc[i].values[0])
    personTokens = df.loc[i].values[1]
    Numbers = df.loc[i].values[2]
    DeathYear = bool(df.loc[i].values[3])
    content = str(df.loc[i].values[4])
    sents = df.loc[i].values[5]
    events = df.loc[i].values[6]
    Numbers = str(Numbers)
    Numbers = Numbers.replace('[','')
    Numbers = Numbers.replace(']','')
    Numbers = Numbers.replace('\'','')
    Numbers = Numbers.split(',')
    try:
        Numbers = [int(n) for n in Numbers]
    except:
        Numbers = []
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    sentences = re.split(r"\.|\:|\n|\,", content)
    events = [re.split(r'([0-9]+)', s) for s in sentences if s != '']
    contentTokens = re.split(r"\.|\:|\n|\,| |\-|\)|\(|[0-9]|\?|\/\\|\t", content)
    print('ARTICLE', personName)
    #print(contentTokens)
    for j in range(0, len(contentTokens)):
        #for k in NameTokens:
        #print(contentTokens, k[0])
        f = [x for x in preList if (x) == (contentTokens[j])]

        toCheck = False
        if len(f) != 0:
            if f[0] != '':
                toCheck = True

        if toCheck:
            #print(f)
            #if contentTokens[j] in str(preList):
            second = ''
            fullSentence = ''
            try:
                for m in range(1,7):
                    word = str(contentTokens[j+m])
                    ff = [x for x in NameTokens if x == word]
                    if len(ff) != 0:
                        if ff[0] != '':
                            second = second + ' ' + ff[0]
                        else:
                            break
                    else:
                        break
                        #second = second + ' ' + word
            except:
                ss = ''
            try:
                for m in range(1, 7):
                    word = str(contentTokens[j + m])
                    fullSentence = fullSentence + ' ' + word
            except:
                ss = ''
            #if second != '':
            #    print('ARTICLE',personName)
            #    print('FULL',fullSentence)
            #    print(contentTokens[j],second)
    counter = 0
    while counter < len(contentTokens):
        second = ''
        original = contentTokens[counter]
        toCheck = False
        f2 = [x for x in NameTokens if x == contentTokens[counter]]
        if len(f2) != 0:
            if f2[0] != '':
                toCheck = True
                try:
                    for m in range(1, 6):
                        word = str(contentTokens[counter + m])
                        ff = [x for x in NameTokens if x == word]
                        if len(ff) != 0:
                            if ff[0] != '':
                                second = second + ' ' + ff[0]
                            else:
                                break
                        else:
                            break
                            # second = second + ' ' + word
                except:
                    ss = ''

                counter += 4
        if second != '':
            print('NAMES',original, second)
        counter += 1