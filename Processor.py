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
from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter
from NameFunctions import compareNames, findMostSimilar, normalize, normalize2, unique, fixArabicNames, combineRelations, getRelation, getFiveBefore, getFiveAfter

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
_path_to_model = 'D:/stanford-postagger-2018-10-16/POSTagger/models/bidirectional-distsim-wsj-0-18.tagger'
_path_to_jar = 'D:/stanford-postagger-2018-10-16/POSTagger/stanford-postagger.jar'
host='http://localhost'
port=9000
scnlp =StanfordCoreNLP(host, port=port,lang='ar', timeout=30000)


death = ['اعدام','قتل','شنق','','']
preList = ['الشيخ', 'الاستاذ', 'المفتي', 'الفنان', 'الشاعر', '', 'الحاج', 'البروفيسور', 'الملا','فضيله', 'البطريرك', 'القس',
           'الكاردينال', 'الملك', 'المحافظ', 'السلطان', 'الاسطة', 'الشريف', 'السيد','القاضي','المرحوم']
familyRelations = ['اخ', 'اب']
familyRelations2 = ['عم', 'خال', 'نسيب', 'ابن عم', 'ابن خال', 'صديق', 'زوج', 'اخت', 'زوجت', 'زوجة', 'ام']
GodNames = ['الاله', 'الامير', 'المنعم', 'المالك', 'الحسين', 'المطلب', 'لمحسن', 'المسيح', 'الحافظ', 'المحسن', 'الزهرة',
            'الماجود', 'الله', 'الرحمن', 'الرحيم', 'الملك', 'القدوس', 'السلام', 'المؤمن', 'المهيمن'
    , 'العزيز', 'الجبار', 'المتكبر', 'الخالق', 'البارئ', 'المصور', 'الغفار', 'القهار', 'الوهاب', 'الرزاق', 'الفتاح',
            'الستار', 'المقصود',
            'العليم', 'القابض', 'الباسط', 'الخافض', 'الرافع', 'المعز', 'المذل', 'السميع', 'البصير', 'الحكم', 'العدل',
            'اللطيف', 'الخبير', 'الحليم', 'العظيم', 'الغفور', 'الشكور',
            'العلي', 'الكبير', 'الحفيظ', 'المقيت', 'الحسيب', 'الجليل', 'الكريم', 'الرقيب', 'المجيب', 'الواسع', 'الحكيم',
            'الودود', 'المجيد', 'الباعث', 'الشهيد', 'الحق', 'الوكيل',
            'القويّ', 'المتين', 'الولي', 'الحميد', 'المحصي', 'المبدئ', 'المعيد', 'المحيي', 'المميت', 'الحي', 'القيوم',
            'الواجد', 'الماجد', 'الواحد', 'الصمد', 'القادر', 'المقتدر',
            'المقدم', 'المؤخر', 'الاول', 'الاخر', 'الظاهر', 'الباطن', 'الوالي', 'المتعالي', 'البر', 'التواب', 'المنتقم',
            'العفو', 'الرؤوف', 'المقسط', 'الجامع', 'الغني', 'المغني', 'المعطي'
    , 'المانع', 'الضار', 'النافع', 'النور', 'الهادي', 'البديع', 'الباقي', 'الوارث', 'الرشيد', 'الصبور']

combineRelations()
'''
Create a list of worship-indicating names by using the list of god names
'''
def addGodNames():
    for i in GodNames:
        NamesDataset.append('عبد' + i)

'''======================================= PARSING PROCESS ========================================='''
'''0, 1.cleanString, 2.tokens, 3.numbers, 4.IsDeathYear, 5.content, 6.sentences, 7.events'''
df = pd.read_csv('OmarAlTalebSheet.csv',encoding='utf-8',header=0)
print(df.head())

'''
Tokenize names, fix the names with spaces, remove unwanted single characters, and add them into a list
'''
NameTokens = []
NamesDataset = []
for i in range(0,len(df)):
    personName = str(df.loc[i].values[0])
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    tokens = fixArabicNames(tokens,False)
    NameTokens.append(tokens)
    for t in tokens:
        NamesDataset.append(normalize(t.strip().replace(' ','')))

'''Add the [son of] to the list of the names to insure bringing old writing style names'''
NamesDataset.append('ابن')
NamesDataset.append('بن')

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(NamesDataset)
print(vectorizer.get_feature_names())
NameFrequencies = [(n/len(vectorizer.get_feature_names())) for n in X.toarray().sum(axis=0)]
NameFrequencies2 = []
for i in range(0, len(vectorizer.get_feature_names())):
    NameFrequencies2.append([vectorizer.get_feature_names()[i], round(NameFrequencies[i],5)])
NameFrequencies2 = NameFrequencies2[1:]
NameFrequencies2 = sorted(NameFrequencies2, key=itemgetter(1))
NameFrequencies = []
for i in range(0,len(NameFrequencies2),100):
    for j in range(i, i+100):
        try:
            NameFrequencies.append([NameFrequencies2[j][0],i/100])
        except:
            break
print(NameFrequencies)

frequencies = {}
for n in NamesDataset:
    frequencies[n] =  NamesDataset.count(n)/len(NamesDataset)

NamesDataset = unique(NamesDataset)
print(len(NameTokens))
resultsDataset = []
testCases = pd.read_csv('testcases.csv',encoding='cp1256', header=0).values.tolist()
istest = True

personscount = len(df.values)
if istest == True:
    personscount = 400
for i in range(0,personscount):
#for i in range(0, 5):
    #Get values from the CSV
    personName = str(df.loc[i].values[0])
    personName = personName.replace('  ',' ')
    personTokens = df.loc[i].values[1]
    Numbers = df.loc[i].values[2]
    DeathYear = bool(df.loc[i].values[3])
    content = str(df.loc[i].values[4])
    sents = df.loc[i].values[5]
    events = df.loc[i].values[6]

    #Get and correct the numbers
    Numbers = str(Numbers)
    Numbers = Numbers.replace('[','')
    Numbers = Numbers.replace(']','')
    Numbers = Numbers.replace('\'','')
    Numbers = Numbers.split(',')
    try:
        Numbers = [int(n) for n in Numbers]
    except:
        Numbers = []

    #Tokenize person name
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    #Sentences splitting
    sentences = re.split(r"\.|\:|\n|\,", content)
    #Get numbers of years from setnences
    events = [re.split(r'([0-9]+)', s) for s in sentences if s != '']
    #contentTokens = re.split(r"\.|\:|\n|\,| |\-|\)|\(|[0-9]|\?|\/\\|\t", content)

    #Tokenize the content of each author
    contentTokens = scnlp.word_tokenize(content)
    #Normalize person name and fix Arabic names
    personName = ' '.join(fixArabicNames([normalize(p) for p in personName.split(' ')],False))

    if istest == True:
        if personName.strip() not in [n[0] for n in testCases]:
            continue

    #Apply the fix process on the content
    contentTokens = fixArabicNames(contentTokens,True)
    counter = 0

    #For each token in each content text of the authors
    while counter < len(contentTokens):
        fiveBefore = ''
        fiveAfter = ''
        relationss = ''
        second = ''
        original = contentTokens[counter]

        #This flag is used to execlude some cases from checking ******************
        toCheck = False
        if original == '':
            counter += 1
            continue
        #If the token was a title (Mrs, Priest, Shiekh..etc) then skip it
        if original in preList:
            original = contentTokens[counter + 1]
            counter += 1
            toCheck = True
        if original in preList:
            original = contentTokens[counter + 1]
            counter += 1
            toCheck = True
        #If the token was available in the names dataset or if there was a signal to check next because there was a title that indicates the existance of a next word
        if len([s for s in NamesDataset if s == original]) >= 1 or toCheck == True:
            toCheck = True
            step = ''
            try:
                step = 'Get five words before'
                #print(step)
                fiveBefore = getFiveBefore(contentTokens, counter)
                f = fiveBefore
                step = 'Get relations'
                #print(step)
                relationss = getRelation(f, counter)
                m = 1
                #Loop in the next 5 words, as there is no name that is longer than 5 words
                step = 'Loop in the next 5 words'
                #print(step)
                while m <= 5:
                    #Get the next word from within the 5 words loop
                    word = str(contentTokens[counter + m])
                    #If a specific punctuation or conjuction came then break the 5 words loop
                    if word == '،' or word == 'و' or word == '.' or word == '،':
                        break
                    #Normalize the selected word
                    word = normalize2(word)
                    #Check if the word exists in the names dataset
                    ff = [x for x in NamesDataset if x == word]
                    AlName = False
                    #Check if the word is one of the AL- names
                    if word[:2] == 'ال' and word[len(word) - 1] == 'ي' and len(word) > 4:
                        #print('AL-NAME',word[:2], word[len(word) - 1], len(word))
                        AlName = True
                    #If the word exists in the names dataset and it is not an AL- name then add it to the rest of the name sentence
                    if len(ff) >= 1 and AlName == False:
                        second = second.strip() + ' '+ ff[0].strip()
                        m += 1
                    #Else, if the word was Al- name then add it to the rest of the name
                    elif AlName == True:
                        second = second.strip() + ' '+ word
                        m += 1
                        break
                    else:
                        break
                #Add the value of (m) which is < 5 to the counter
                counter += m
            except Exception as e:
                print(e)
                ss = ''
            #Get the five words after
            fiveAfter = getFiveAfter(contentTokens, counter)
        #Strip sentences from the name sentence
        if second.strip() != '':
            if second[0] == ' ':
                second = second[1:]
            #Add the second name/s to the first name
            newname = original + ' '+ second
            #Find the most similar name from the names in the book and connect it with the article of the similar name
            mostsimilar = findMostSimilar(newname, index=counter,personNametokens = tokens, NameTokens=NameTokens, NameFrequencies=NameFrequencies)
            #if  mostsimilar != '':
            #    mostsimilar = mostsimilar
            tt = []
            #After normalizing the title tokens, find the similarity between the title tokens and the detected name if the similarity is more than 0.4 then it is the same
            for i in tokens:
                tt.append(normalize(i))
            IsItTheSameArticleOwnerName = compareNames(newname.split(' '), tt,30, NameFrequencies)
            if IsItTheSameArticleOwnerName < 0.4:
                if counter < 15 and fiveBefore == '':
                    print('PERSON', personName, ';NAME: SAME PERSON', newname, ';BEFORE', fiveBefore)
                    resultsDataset.append([personName, personName, True, None, None, None, fiveBefore])
                else:
                    if relationss != '':
                        relationsss = 'RELATION:' + relationss[0] + ':' + relationss[1]
                    print('PERSON',personName,';NAME',newname,relationsss,';CONNECTION',mostsimilar,';BEFORE', fiveBefore)
                    if len(relationss) != 0:
                        resultsDataset.append([personName, newname, False, relationss[0], relationss[1], mostsimilar if mostsimilar != '' else None,fiveBefore])
                    else:
                        resultsDataset.append([personName, newname, False, None, None, mostsimilar if mostsimilar != '' else None, fiveBefore])
                #print('NAMES',newname,  mostsimilar)
                #print('AFTER', fiveAftere)
            else:
                print('PERSON', personName, ';NAME: SAME PERSON', newname, ';BEFORE', fiveBefore)
                resultsDataset.append([personName, personName, True, None, None, None, fiveBefore])

        counter += 1
    AlWords = []
#resultsDataset = pd.DataFrame(resultsDataset).to_csv('resultsdataset.csv')
'''for w in contentTokens:
    if w[:2] == 'ال' or w[:3] ==  'وال' and len(w) > 5:
        AlWords.append(w)
    print(personName,AlWords)'''
from itertools import groupby
'''Check counts'''
