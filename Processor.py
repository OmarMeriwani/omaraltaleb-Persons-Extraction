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
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag
import os
from nltk.internals import find_jars_within_path
from nltk.parse.stanford import StanfordDependencyParser
from stanfordcorenlp import StanfordCoreNLP

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
_path_to_model = 'D:/stanford-postagger-2018-10-16/POSTagger/models/bidirectional-distsim-wsj-0-18.tagger'
_path_to_jar = 'D:/stanford-postagger-2018-10-16/POSTagger/stanford-postagger.jar'
host='http://localhost'
port=9000
scnlp =StanfordCoreNLP(host, port=port,lang='ar', timeout=30000)

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
    postList = ['سيد','اغا','ملا']
    for p in postList:
        if p == name1[0]:
            name1 = name1.pop(0)
    familyRelations = ['اخ','اب']
    familyRelations2 = ['عم','خال','نسيب','ابن عم','ابن خال','صديق','زوج','اخت','زوجت','زوجة','ام']
    name1 = list(name1)
    name2 = list(name2)
    score = 0
    if name1[0] == name2[0] and name1[len(name1)-1] == name2[len(name2)-1]:
        score += 0.6
    if name1[0] == name2[0] and name1[1] == name2[1] and score==0 and len(name1) <4:
        score += 0.6

    similarity = 0
    for i in range(0,len(name1) - 1):
        if 'عبد' == name1[i]:
            score -= 0.2
    for i in range(0,len(name1) - 1):
        ff = [x for x in name2 if x == name1[i]]
        if len(ff) > 0:
            if ff[0] != '':
                similarity += 1
    similarity = similarity / len(name1)
    score += 0.4 * similarity
    return score

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
    return word
'''0, 1.cleanString, 2.tokens, 3.numbers, 4.IsDeathYear, 5.content, 6.sentences, 7.events'''
df = pd.read_csv('OmarAlTalebSheet.csv',encoding='utf-8',header=0)
print(df.head())
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
        NamesDataset.append(t.strip().replace(' ',''))
NamesDataset = unique(NamesDataset)

def findMostSimilar(name):
    max = 0
    articleName = ''
    for n in NameTokens:
        score = compareNames(str(name).split(' '), n)
        if score > max:
            max = score
            articleName = n
    if max > 0.6:
        return ' '.join(articleName)
    else:
        return ''
print(len(NameTokens))
for i in range(0,len(df)):
    personName = str(df.loc[i].values[0])
    personName = personName.replace('  ',' ')
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
    #contentTokens = re.split(r"\.|\:|\n|\,| |\-|\)|\(|[0-9]|\?|\/\\|\t", content)
    contentTokens = scnlp.word_tokenize(content)

    print('ARTICLE', personName)
    #print(contentTokens)
    counter = 0
    while counter < len(contentTokens):
        second = ''
        original = contentTokens[counter]
        toCheck = False
        original = original.replace('  ',' ')
        if original == '':
            counter += 1
            continue
        if original[0] == 'و':
            original = original[1:]
            contentTokens[counter] = contentTokens[counter][1:]
        f2 = [x for x in NamesDataset if x == contentTokens[counter]]
        if len(f2) != 0:
            if f2[0] != '':
                toCheck = True
                try:
                    for m in range(1, 10):
                        word = str(contentTokens[counter + m])
                        ff = [x for x in NamesDataset if x == word]
                        AlName = False
                        if word[:2] == 'ال' and word[len(word) - 1] == 'ي' and len(word) > 4:
                            #print('AL-NAME',word[:2], word[len(word) - 1], len(word))
                            AlName = True
                        if len(ff) != 0:
                            if ff[0] != '':
                                second = second.strip() + ' '+ ff[0].strip()
                            else:
                                if AlName == True:
                                    second = second + ' '+ word
                                else:
                                    break
                        else:
                            if AlName == True:
                                second = second + ' '+ word
                            else:
                                break
                            # second = second + ' ' + word
                except:
                    ss = ''

                counter += 10
        if second != '':
            mostsimilar = findMostSimilar(original + ' '+ second)
            if second[0] == ' ':
                second = second[1:]
            if mostsimilar != original +' '+ second or mostsimilar == '':
                if mostsimilar != '':
                    mostsimilar = 'ARTICLE: ' + mostsimilar
                #print('NAMES',original + ' '+ second,  mostsimilar)
        counter += 1
    AlWords = []
    for w in contentTokens:
        if w[:2] == 'ال' or w[:3] ==  'وال' and len(w) > 5:
            AlWords.append(w)
    print(personName,AlWords)
