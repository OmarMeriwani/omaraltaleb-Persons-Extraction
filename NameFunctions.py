from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter
def compareNames(name1, name2, index, NameFrequencies):
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
        frequency = [n[1] for n in NameFrequencies if n[0] == first1]
        if len(frequency) != 0:
            if frequency[0] <= 6:
                score += 1 / 10 - frequency[0]
        if lastsEqual:
            score += 0.25
            #print('NAME1', name1, 'NAME2', name2)
            if Name1Length == 2 or Name2Length == 2:
                score += 0.1
                return score
        if Name1Length >= 2 and Name2Length == Name1Length + 1:
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

'''This method gives numerical similarity scores from 0 to 1, the score 1 means that the two names are totally the same
It compares specific word with all the names in the encyclopedia
 But in the beginning, it checks a set of titles that gets confused with person names such as (Shiekh, Mulla..etc), if the 
 title existed then it would be removed from the name. After that, the method relies on the previos method of compareNames which gives the scores'''
def findMostSimilar(name, index, personNametokens, NameTokens, NameFrequencies):
    max = 0
    articleName = ''
    first = name.split(' ')
    if index < 15:
        return ''
    if len(first) == 1:
        return ''

    for n in NameTokens:
        score = compareNames(first, n, index, NameFrequencies)
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

#This method is used to create a unique list of names
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
        if word == 'بن' or word == 'ابن':
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

def fixname (name):
    personName = str(name)
    personName = personName.replace('  ',' ')
    tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
    tokens = fixArabicNames(tokens, False)
    return ' '.join(tokens)

def getNameFrequencies(df):
    NameTokens = []
    NamesDataset = []
    for i in range(0, len(df)):
        personName = str(df.loc[i].values[0])
        tokens = [s for s in personName.split(' ') if s != '' and s != 'ت']
        tokens = fixArabicNames(tokens, False)
        NameTokens.append(tokens)
        for t in tokens:
            NamesDataset.append(normalize(t.strip().replace(' ', '')))

    '''Add the [son of] to the list of the names to insure bringing old writing style names'''
    NamesDataset.append('ابن')
    NamesDataset.append('بن')

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(NamesDataset)
    print(vectorizer.get_feature_names())
    NameFrequencies = [(n / len(vectorizer.get_feature_names())) for n in X.toarray().sum(axis=0)]
    NameFrequencies2 = []
    for i in range(0, len(vectorizer.get_feature_names())):
        NameFrequencies2.append([vectorizer.get_feature_names()[i], round(NameFrequencies[i], 5)])
    NameFrequencies2 = NameFrequencies2[1:]
    NameFrequencies2 = sorted(NameFrequencies2, key=itemgetter(1))
    NameFrequencies = []
    for i in range(0, len(NameFrequencies2), 100):
        for j in range(i, i + 100):
            try:
                NameFrequencies.append([NameFrequencies2[j][0], i / 100])
            except:
                break
    print(NameFrequencies)

    frequencies = {}
    for n in NamesDataset:
        frequencies[n] = NamesDataset.count(n) / len(NamesDataset)
    return NameFrequencies

'''Relations terms'''
familyRelations3 = ['اب','ابو', 'ام', 'اخ','اخوت','الاخ','اخو','ابا','اخا', 'اخت', 'عم', 'خال', 'خال', 'خالة','خالت', 'جد','جدة','جدت','حفيد','حفيدة','حفيدت','نسيب','نسيبة','نسيبت','حما','حمو','والد','والدة','والدت','زوج','زوجة','زوجت','كنت','شقيق','شقيقة','شقيقت','ابن','ابنة','ابنت','قرابة','زواج','ابناء','أولاد','اخوة','عمومة']
familyRelations4 = ['زوجة اب','زوجت اب','زوج ام','ابن خال','ابن خالة','ابن خالت','ابن عم','ابن عمة','ابن عمت','ابن اخي','ابن اخو','بنت اخي','بنت اخو','بنت اخت','ابن اخت']
friendship = ['حليف','حليفت','صداقت','صاحبت','رفيقة','زميل','زميلة','صداقة','حلف','صحبة','رفقة','زمالة','علاقة']
friendship2 = ['صاحب','صديق','رفيق']
study = ['أستاذ','تلامذت','أستاذة','درسنا','شيخ','معلم','معلمة','مدرس','مدرسة','تلميذ','مريد','اشراف','متعلم','تعلم','درس','تتلمذ','تعلم','تلامذة','قرأ','اجيز','أجاز','جامعه','كليه']
study2 = ['مدرسة','دروس','دراسة','مدير المدرسة','احتضن','الاجازة','إجازة','طلبة','الاجازه','دراسة']
study3 = ['طالب']
government = ['والي','ملك','وزير','الوالي','الملك','الوزير']
government2 = ['رئيس الجمهورية','رئيس الوزراء']
work = ['مدير','لصالح','حزب','مخرج','المخرج','ادارة','وظيفة','وظائف','مسؤول','زعامه','جريدة','معمل','مصنع','صحيفة','مجلة','معمل','دائرة','مدرسة','جامع','مسجد','كنيسة','كاتدرائية','ثانوية','إعدادية','وزارة','جريدة','صحيفة','مجلة','وزارة','مشرف','رئيس','زعيم','موظف','عامل','مرافق','مراسل']
work2 = ['رئيس تحرير','رقا ه','ولا ه','ول اه','عين ه','مدير مدرسه','مدير المدرسه']
companions = ['شراكة','يلازم','رابطه','معية','اتصل','مساهمة','مشترك','مشارك','مشاركين','المشاركون','المشاركين','مشاركون','مشاركة','مشتركة','اشترك','ساهم','اشتراك','الاشتراك','اشتراك','مشترك','مساهم' ]
companions2 = ['كان من بين','واحد من','واحدا من']
contact = ['مراسلات','راسل','اتصل']
mention = ['مدح','قال','ذكر','أشار','يقول','يذكر','يشير']
mention2 = ['كتب ل','كتب عن','قال عن']
idiology = ['متأثرا ب','يشبه','يشابه في','الاتجاه','تأثير','معجب']
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
        relations.append([i, 'WSTUDY', 1, False])
    for i in study2:
        relations.append([i, 'WSTUDY', 1, False])
    for i in study3:
        relations.append([i, 'WSTUDY', 1, True])
    for i in work:
        relations.append([i, 'WSTUDY', 1, False])
    for i in work2:
        relations.append([i, 'WSTUDY', 1, False])
    for i in companions:
        relations.append([i, 'COMPANY', 1, False])
    for i in companions2:
        relations.append([i, 'COMPANY', 2, False])
    for i in contact:
        relations.append([i, 'CONTACT', 1, False])
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


'''
According to the words before the name, find the relations based on:
* The complete match between one of the relations and one of the words before the name
'''
ObjectPronouns = ['ه','ي','هم']
def getRelation(wordsbefore, index):
    if index < 4:
        return ''
    relation = ''
    relationsset = []
    step = ''
    #The complete match between one of the relations and one of the words before for two-word relations
    try:
        step = 'Relations: complete match check'
        for i in [f for f in relations2 if f[2] == 2]:
            rel = i[0]
            place = wordsbefore.find(rel)
            if place != -1:
                relationsset.append([i,place])
        #Match between one of the words that require object pronoun that is followed by an object pronoun
        step = 'Relations: object pronouns check'
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
        step = 'Relations: one word match check'
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
        step = 'Relations: get nearest relation'
        for i in relationsset:
            rela = i[0]
            place = i[1]
            type = rela[1]
            #count removed
            rel = rela[0]
            if place > minn:
                relation = (type , rel)
            if type == '' or type is None:
                relation = ('MISC' , '')
        if len(relationsset) == 0:
            relation = ('MISC', '')
    except Exception as e:
        print('Step: ', step,e)
    return relation

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
