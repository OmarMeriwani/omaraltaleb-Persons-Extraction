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

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
_path_to_model = 'D:/stanford-postagger-2018-10-16/POSTagger/models/bidirectional-distsim-wsj-0-18.tagger'
_path_to_jar = 'D:/stanford-postagger-2018-10-16/POSTagger/stanford-postagger.jar'
host='http://localhost'
port=9000
scnlp =StanfordCoreNLP(host, port=port,lang='ar', timeout=30000)


death = ['اعدام','قتل','شنق','','']
preList = ['الشيخ', 'الاستاذ', 'المفتي', 'الفنان', 'الشاعر', '', 'الحاج', 'البروفيسور', 'الملا', 'البطريرك', 'القس',
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
    score = 0
    Name1Length = len(name1)
    Name2Length = len(name2)
    Last1 = str(name1[len(name1) - 1])
    Last2 = str(name2[len(name2) - 1])
    IsName1HasAlName = str(name1[len(name1) - 1])[:2] == 'ال'
    IsName2HasAlName = str(name2[len(name2) - 1])[:2] == 'ال'
    name1EqualsName2 = name1[0] == name2[0]
    lastsEqual = Last1 == Last2
    first1 = name1[0]
    first2 = name2[0]
    firstsEqual = first1 == first2
    TheSame = True
    shorter = 0
    if Name1Length > Name2Length:
        shorter = Name2Length
    elif Name2Length >= Name1Length:
        shorter = Name1Length

    if Name1Length == Name2Length:
        for i in range(0, len(name1)):
            if name1[i] != name2[i]:
                TheSame = False
                break
    else:
        TheSame = False
    if TheSame == True:
        return 1

    if firstsEqual:
        score += 0.3
        if lastsEqual:
            score += 0.25
            #print('NAME1', name1, 'NAME2', name2)
            if Name1Length == 2 or Name2Length == 2:
                score += 0.1
                return score
        if Name1Length == 2 and Name2Length == 3:
            if name1[1] == name2[1]:
                score += 0.3
        if Name1Length > 2:
            part = []
            part2 = []
            if Name2Length < Name1Length:
                part = name1[1:Name1Length-1]
                part2 = name2[1:Name2Length - 1]
            else:
                part = name2[1:Name2Length-1]
                part2 = name1[1:Name1Length - 1]

            for p in part:
                if p in part2:
                    score += 0.15
    return score


'''This method gives numerical similarity scores from 0 to 1, the score 1 means that the two names are totally the same
It compares specific word with all the names in the encyclopedia
 But in the beginning, it checks a set of titles that gets confused with person names such as (Shiekh, Mulla..etc), if the 
 title existed then it would be removed from the name. After that, the method relies on the previos method of compareNames which gives the scores'''
def findMostSimilar(name, index, personNametokens):
    max = 0
    articleName = ''
    postList = ['سيد','السيد','الملا','الشيخ','شيخ','ملا']
    first = name.split(' ')

    if index < 15:
        return ''
    if (first[0] in postList):
        first = first[1:]
    first = [s for s in first if s != '']

    if len(first) == 1:
        return ''

    for n in NameTokens:
        score = compareNames(first, n, index)
        if score > max:
            max = score
            articleName = n
    if max >= 0.6:
        return ' '.join(articleName)
    else:
        return ''
#This method normalizes headline titles in the Encyclopedia, which contains specific unwanted letters such as (ت) which refers to the death year of the person
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
#This method normalizes normal words in the text of the encyclopedia.
def normalize2(word):
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
#This method is used to create
def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return  unique_list

'''
Remove spaces from the names that consists of two words which are mainly the names with (دين) or the names that indicates worshiping (عبد) which mean slave of X where X is one of the names of God, Juesus or Muslim holy figures 
'''
def fixArabicNames (tokenss, isText):
    Prelist2 = ['الشيخ','الحاج', 'الملا', 'السيد']

    newtokens = []
    skipNext = False
    tokenss = [a for a in tokenss if a != ')' and a != '(' ]
    for i in range(0, len(tokenss)):

        word = ''
        if isText == True:
            word = normalize2(tokenss[i])
        else:
            word = normalize(tokenss[i])
        word2 = ''
        if i + 1 < len(tokenss):
            if isText == True:
                word2 = normalize2(tokenss[i + 1])
            else:
                word2 = normalize(tokenss[i + 1])
        if skipNext == True:
            skipNext = False
            continue
        if word == '\xa0':
            continue
        if  word == 'ابو' or word ==  'آل':
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


'''Relations terms'''
familyRelations3 = ['اب','ابو', 'ام', 'اخ','اخوت','الاخ','اخو','ابا','اخا', 'اخت', 'عم', 'خال', 'خال', 'خالة','خالت', 'جد','جدة','جدت','حفيد','حفيدة','حفيدت','نسيب','نسيبة','نسيبت','حما','حمو','والد','والدة','والدت','زوج','زوجة','زوجت','كنت','شقيق','شقيقة','شقيقت','ابن','ابنة','ابنت','قرابة','زواج','ابناء','أولاد','اخوة','عمومة']
familyRelations4 = ['زوجة اب','زوجت اب','زوج ام','ابن خال','ابن خالة','ابن خالت','ابن عم','ابن عمة','ابن عمت','ابن اخي','ابن اخو','بنت اخي','بنت اخو','بنت اخت','ابن اخت']
friendship = ['حليف','حليفت','صداقت','صاحبت','رفيقة','زميل','زميلة','صداقة','حلف','صحبة','رفقة','زمالة','علاقة']
friendship2 = ['صاحب','صديق','رفيق']
study = ['أستاذ','تلامذت','أستاذة','درسنا','شيخ','معلم','معلمة','مدرس','مدرسة','تلميذ','مريد','اشراف','متعلم','تعلم','درس','تتلمذ','تعلم','تلامذة','قرأ','اجيز','أجاز']
study2 = ['مدرسة','دروس','دراسة','مدير المدرسة','احتضن','الاجازة','إجازة','طلبة','دراسة']
study3 = ['طالب']
government = ['والي','ملك','وزير','الوالي','الملك','الوزير']
government2 = ['رئيس الجمهورية','رئيس الوزراء']
work = ['مدير','لصالح','حزب','مخرج','المخرج','ادارة','وظيفة','وظائف','مسؤول','زعامه','جريدة','معمل','مصنع','صحيفة','مجلة','معمل','دائرة','مدرسة','جامع','مسجد','كنيسة','كاتدرائية','ثانوية','إعدادية','وزارة','جريدة','صحيفة','مجلة','وزارة','مشرف','رئيس','زعيم','موظف','عامل','مرافق','مراسل']
work2 = ['رئيس تحرير','رقا ه','ولا ه','ول اه','عين ه','مدير مدرسه','مدير المدرسه']
companions = ['شراكة','يلازم','رابطه','معية','اتصل','مساهمة','مشترك','مشارك','مشاركين','المشاركون','المشاركين','مشاركون','مشاركة','مشتركة','اشترك','ساهم','اشتراك','الاشتراك','اشتراك','مشترك','مساهم' ]
companions2 = ['كان من بين','واحد من','واحدا من']
mention = ['مدح','قال','ذكر','أشار','يقول','يذكر','يشير']
mention2 = ['كتب ل','كتب عن','قال عن']
idiology = ['متأثرا ب','يشبه','يشابه في','الاتجاه','تأثير']
books = ['رواية','كتاب','قصة']
help2 = ['ب فضل']
help = ['توسط','بواسطة','بفضل','رعاية','رعا','يرعى','رعى']
hate = ['عادى','كره','حقد','عداء']
competition = ['منافسه','نافس']
relations = []
relations2 = []

'''
Setting the priorities, relation classes, number of words for each relation, Is it require object pronoun after it?
Then combine them all into one array
'''
def combineRelations():
    '''[Word, Class, Number of Words, Is it require object pronoun after it]'''
    for i in familyRelations3:
        relations.append([i,'FAMILY',1,False])
    for i in familyRelations4:
        relations.append([i, 'FAMILY', 2,False])
    for i in government2:
        relations.append([i, 'GOVERNMENT', 2,False])
    for i in friendship:
        relations.append([i, 'FRIENDSHIP', 1, False])
    for i in friendship2:
        relations.append([i, 'FRIENDSHIP', 1, True])
    for i in government:
        relations.append([i, 'GOVERNMENT', 1, False])
    for i in study:
        relations.append([i, 'STUDY', 1, False])
    for i in study2:
        relations.append([i, 'STUDY', 1, False])
    for i in study3:
        relations.append([i, 'STUDY', 1, True])
    for i in work:
        relations.append([i, 'WORK', 1, False])
    for i in work2:
        relations.append([i, 'WORK', 1, False])
    for i in companions:
        relations.append([i, 'COMPANY', 1, False])
    for i in companions2:
        relations.append([i, 'COMPANY', 2, False])
    for i in mention:
        relations.append([i, 'MENTION', 1, False])
    for i in help:
        relations.append([i, 'HELP', 1, False])
    for i in hate:
        relations.append([i, 'HATERD', 1, False])
    for i in competition:
        relations.append([i, 'COMPETITION', 1, False])
    for i in relations:
        relations2.append([normalize2(i[0]),i[1],i[2],i[3]])


combineRelations()
ObjectPronouns = ['ه','ي','هم']
'''
According to the words before the name, find the relations based on:
* The complete match between one of the relations and one of the words before the name
'''
def getRelation(wordsbefore, index):
    if index < 4:
        return ''
    relation = ''
    relationsset = []
    #The complete match between one of the relations and one of the words before for two-word relations
    for i in [f for f in relations2 if f[2] == 2]:
        rel = i[0]
        place = wordsbefore.find(rel)
        if place != -1:
            relationsset.append([i,place])
    #Match between one of the words that require object pronoun that is followed by an object pronoun
    for i in [f for f in relations2 if f[3] == True]:
        try:
            rel = i[0]
            wordsbeforeArray = wordsbefore.split(' ')
            place = wordsbeforeArray.index(rel)
            if place != -1 and wordsbeforeArray[place + 1] in ObjectPronouns:
                relationsset.append([i,place])
        except Exception as e:
            continue
    #The occurence of one word relation that doesn't require object pronoun
    for i in [f for f in relations2 if f[3] == False and f[2] == 1]:
        rel = i[0]
        wordsbeforeArray = wordsbefore.split(' ')
        try:
            place = -1
            place = wordsbeforeArray.index(rel)
        except Exception as e:
            #print(e.args)
            continue
        if place != -1:
            relationsset.append([i,place])
    minn = 0
    #For each relation from the above, the place and the word were stored, then in the following step, only the nearest to the name will be considered
    for i in relationsset:
        rela = i[0]
        place = i[1]
        type = rela[1]
        count = i[2]
        #if count == 2:
        #    relation = type + ':' + rel
        #    break
        rel = rela[0]
        if place > minn:
            relation = type + ':' + rel
    return relation

'''
Create a list of worship-indicating names by using the list of god names
'''
def addGodNames():
    for i in GodNames:
        NamesDataset.append('عبد' + i)

#A method to get five words before any detected name
def getFiveBefore(contentTokens, index):
    if index < 4:
        return ''
    wordsbefore = ''
    for i in range(1,30):
        try:

            if contentTokens[index - i] == '.' and contentTokens[index - i - 1] != 'د':
                break
            wordsbefore = contentTokens[index - i] + ' '+  wordsbefore
        except:
            continue
    return wordsbefore

#A method that returns a number of words after the detected name
def getFiveAfter(contentTokens, index):
    wordsAfter = ''
    for i in range(0,14):
        try:
            wordsAfter = wordsAfter +' '+ contentTokens[index + i]
        except:
            continue
    return wordsAfter

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


frequencies = {}
for n in NamesDataset:
    frequencies[n] =  NamesDataset.count(n)/len(NamesDataset)

NamesDataset = unique(NamesDataset)
print(len(NameTokens))
for i in range(0,len(df)):
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
        #If the token was available in the names dataset
        if len([s for s in NamesDataset if s == original]) >= 1 or toCheck == True:
            step = ''
            try:
                step = 'Get five words before'
                fiveBefore = getFiveBefore(contentTokens, counter)
                f = fiveBefore
                step = 'Get relations'
                relationss = getRelation(f, counter)
                m = 1
                while m <= 5:
                    word = str(contentTokens[counter + m])
                    #if word == 'رفعت':
                    #    print(word)
                    if word == '،' or word == 'و' or word == '.' or word == '،':
                        #m += 1
                        break
                    word = normalize2(word)
                    ff = [x for x in NamesDataset if x == word]
                    AlName = False

                    if word[:2] == 'ال' and word[len(word) - 1] == 'ي' and len(word) > 4:
                        #print('AL-NAME',word[:2], word[len(word) - 1], len(word))
                        AlName = True
                    if len(ff) >= 1 and AlName == False:
                        second = second.strip() + ' '+ ff[0].strip()
                        m += 1
                    else:
                        if AlName == True:
                            second = second + ' '+ word
                            m += 1
                            break
                        else:
                            #m += 1
                            break
                    #print(m)
                counter += m
                    #counter += 1
                        # second = second + ' ' + word
            except Exception as e:
                #print(step, e.args)
                ss = ''
            #counter += 5
            fiveAfter = getFiveAfter(contentTokens, counter)

        if second.strip() != '':
            if second[0] == ' ':
                second = second[1:]
            newname = original + ' '+ second
            mostsimilar = findMostSimilar(newname, index=counter,personNametokens = tokens)
            if  mostsimilar != '':
                mostsimilar = 'ARTICLE: ' + mostsimilar
            tt = []
            for i in tokens:
                tt.append( normalize(i))
            IsItTheSameArticleOwnerName = compareNames(newname.split(' '), tt,30)
            if IsItTheSameArticleOwnerName < 0.4:
                if counter < 15 and fiveBefore == '':
                    print('PERSON', personName, ';NAME: SAME PERSON', newname, ';BEFORE', fiveBefore)
                else:
                    if relationss != '':
                        relationss = 'RELATION:' + relationss
                    print('PERSON',personName,';NAME',newname,relationss,';CONNECTION',mostsimilar,';BEFORE', fiveBefore)
                #print('NAMES',newname,  mostsimilar)
                #print('AFTER', fiveAftere)
            else:
                print('PERSON', personName, ';NAME: SAME PERSON', newname, ';BEFORE', fiveBefore)
        counter += 1
    AlWords = []
    '''for w in contentTokens:
        if w[:2] == 'ال' or w[:3] ==  'وال' and len(w) > 5:
            AlWords.append(w)
    print(personName,AlWords)'''
