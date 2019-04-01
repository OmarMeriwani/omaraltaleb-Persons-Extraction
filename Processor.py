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
familyRelations = ['اخ', 'اب']
familyRelations2 = ['عم', 'خال', 'نسيب', 'ابن عم', 'ابن خال', 'صديق', 'زوج', 'اخت', 'زوجت', 'زوجة', 'ام']


def compareNames(name1, name2, index):
    '''
    If both names were the same length
    They should be exactly the same

    If the first name is longer
    - Last and first should be the same if the last was AL- name
    - 70% should be similar

    If the first name was shorter
    - Last and first should be the same if the last was AL- name
   '''
    name1 = list(name1)
    name2 = list(name2)

    Name1Length = len(name1)
    Name2Length = len(name2)
    IsName1HasAlName = str(name1[len(name1) - 1])[:2] == 'ال'
    IsName2HasAlName = str(name2[len(name2) - 1])[:2] == 'ال'
    name1EqualsName2 = name1[0] == name2[0]
    NotTheSame = False
    if Name1Length == Name2Length:
        for i in range(0, len(name1)):
            
    score = 0

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
    if word == 'ت':
        word = word.replace('ت','')
    if word == 'ه':
        word = word.replace('ه','')
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
def fixArabicNames (tokenss):
    GodNames = ['الاله','المالك','الحسين','المطلب','لمحسن','المسيح','الحافظ','المحسن','الزهرة','الماجود','الله','الرحمن','الرحيم','الملك','القدوس','السلام','المؤمن','المهيمن','العزيز','الجبار','المتكبر','الخالق','البارئ','المصور','الغفار','القهار','الوهاب','الرزاق','الفتاح','العليم','القابض','الباسط','الخافض','الرافع','المعز','المذل','السميع','البصير','الحكم','العدل','اللطيف','الخبير','الحليم','العظيم','الغفور','الشكور','العلي','الكبير','الحفيظ','المقيت','الحسيب','الجليل','الكريم','الرقيب','المجيب','الواسع','الحكيم','الودود','المجيد','الباعث','الشهيد','الحق','الوكيل','القويّ','المتين','الولي','الحميد','المحصي','المبدئ','المعيد','المحيي','المميت','الحي','القيوم','الواجد','الماجد','الواحد','الصمد','القادر','المقتدر','المقدم','المؤخر','الاول','الاخر','الظاهر','الباطن','الوالي','المتعالي','البر','التواب','المنتقم','العفو','الرؤوف','المقسط','الجامع','الغني','المغني','المعطي','المانع','الضار','النافع','النور','الهادي','البديع','الباقي','الوارث','الرشيد','الصبور']
    Prelist2 = ['الشيخ','الحاج', 'الملا', 'السيد']

    newtokens = []
    skipNext = False
    for i in range(0, len(tokenss)):
        word = normalize(tokenss[i])
        word2 = ''
        if i + 1 < len(tokenss):
            word2 = normalize(tokenss[i + 1])
        if skipNext == True:
            skipNext = False
            continue
        if word == '\xa0':
            continue
        if  normalize(word) == 'ابو' or word ==  'آل':
            newtokens.append(''.join([word,word2]))
            skipNext = True
            continue
        if word == 'بن':
            continue
        if (word ==  'عبد' and word2 in GodNames and word2 != ''):
            newtokens.append(''.join([word, word2]))
            skipNext = True
            continue
        if word2 == 'الدين' or word2 == 'الله' :
            '''or tokenss[i + 1] == 'بك' or tokenss[i + 1] == 'اغا'''
            newtokens.append(''.join([word, word2]))
            skipNext = True
            continue
        newtokens.append(word)
    newtokens2 = []
    '''for i in range(0, len(newtokens)):
        if newtokens[i] in Prelist2:
            continue
        newtokens2.append(newtokens[i])'''
    return newtokens


NameTokens = []
NamesDataset = []
for i in range(0,len(df)):
    personName = str(df.loc[i].values[0])
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    #print('ORIGINALNAMES',tokens)
    tokens = fixArabicNames(tokens)
    #print('FIXEDNAMES', tokens)
    NameTokens.append(tokens)
    for t in tokens:
        NamesDataset.append(normalize(t.strip().replace(' ','')))

NamesDataset = unique(NamesDataset)


def findMostSimilar(name, index):
    max = 0
    articleName = ''
    postList = ['سيد','السيد','الملا','ملا']
    first = name.split(' ')
    if index < 15:
        return ''
    if (first[0] in postList):
        first = first[1:]
    for n in NameTokens:
        score = compareNames(first, n, index)
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
    personName = ' '.join(fixArabicNames([normalize(p) for p in personName.split(' ')]))
    contentTokens = fixArabicNames(contentTokens)
    print('ARTICLE', personName)
    #print('TEXT', contentTokens)
    #print(contentTokens)
    counter = 0
    while counter < len(contentTokens):
        second = ''
        original = contentTokens[counter]
        toCheck = False
        if original == '':
            counter += 1
            continue
        if len([s for s in NamesDataset if s == original]) >= 1:
            toCheck = True
            try:
                for m in range(1, 5):
                    word = str(contentTokens[counter + m])
                    ff = [x for x in NamesDataset if x == word]
                    AlName = False
                    if word[:2] == 'ال' and word[len(word) - 1] == 'ي' and len(word) > 4:
                        #print('AL-NAME',word[:2], word[len(word) - 1], len(word))
                        AlName = True
                    if len([s for s in NamesDataset if s == word]) >= 1:
                        second = second.strip() + ' '+ ff[0].strip()
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
            mostsimilar = findMostSimilar(original + ' '+ second, index=counter)
            if second[0] == ' ':
                second = second[1:]
            if mostsimilar != original +' '+ second or mostsimilar == '':
                if mostsimilar != '':
                    mostsimilar = 'ARTICLE: ' + mostsimilar
                print('NAMES',original + ' '+ second,  mostsimilar, counter)
        counter += 1
    AlWords = []
    '''for w in contentTokens:
        if w[:2] == 'ال' or w[:3] ==  'وال' and len(w) > 5:
            AlWords.append(w)
    print(personName,AlWords)'''
