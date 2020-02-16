import pandas as pd
from NameFunctions import normalize2
from stanfordcorenlp import StanfordCoreNLP
import os
import re
import string
import nltk.stem.isri
import tensorflow

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import tensorflow as tf
from tfevaluation import f1
from keras.layers import Dense, Dropout, Input, Concatenate
from keras.models import Sequential
import tensorflow.keras
from keras.models import Model
import keras
import numpy as np
import scipy as sp

#Number of classes
numOfClasses = 2

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
_path_to_model = 'D:/stanford-postagger-2018-10-16/POSTagger/models/bidirectional-distsim-wsj-0-18.tagger'
_path_to_jar = 'D:/stanford-postagger-2018-10-16/POSTagger/stanford-postagger.jar'
host='http://localhost'
port=9000
scnlp =StanfordCoreNLP(host, port=port,lang='ar', timeout=30000)

stemmer = nltk.stem.isri.ISRIStemmer()
print('Read sheet..')
df = pd.read_excel('relationsAnnotation.xlsx',sheet_name='Sheet1' ,header=0)
df_stopwords = pd.read_csv('arabicStopWords')
stopwords = []

for i in df_stopwords.values:
    stopwords.append(normalize2(str(i[0])))
print(stopwords)

def createModel(dim):
    model = Sequential()
    model.add(Dense(1400, activation='relu', input_dim=dim)) #64396
    model.add(Dropout(0.8))
    model.add(Dense(600))
    model.add(Dropout(0.8))
    model.add(Dense(numOfClasses, activation='softmax'))
    model.compile(optimizer='adam',
                  loss=tf.compat.v1.keras.losses.categorical_crossentropy,
                  metrics=[f1])
    return model
def createModelForRelations(dim, dim2):
    input = Input(shape=(dim[0],))
    model = Dense(1400, activation='relu')(input) #64396
    model = Dropout(0.5)(model)
    model = Dense(600)(model)
    model = Dense(20)(model)
    #modelFull = Model(input, model)
    #model.add(Dense(600))
    #model.add(Dropout(0.5))
    '''model = Sequential()
    model.add(Dense(1400, input_dim=dim, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation="relu"))'''

    '''model2 = Sequential()
    model2.add(Dense(20, input_dim=dim, activation="relu"))
    #model.add(Dropout(0.5))
    model2.add(Dense(20))'''
    input2 = Input(dim2)
    model2  = Dense(20)(input2)
    model2  = Dense(20)(model2)
    #model2Full = Model(input2, model2)
    #concat = Concatenate(axis=1, name='concatLayer')([model, model2])
    concat = keras.layers.Concatenate()([model, model2])
    x = Dense(4, activation="relu")(concat)
    x = Dense(1, activation="linear")(x)

    model3 = Model(inputs=[input, input2], outputs=x)
    model3.compile(loss="mean_absolute_percentage_error", optimizer='adam')

    #output = Dense(units=numOfClasses, activation=tf.keras.activations.softmax)(concat)
    #full_model = tf.keras.Model(inputs=[model.input, model2.input], outputs=[output])

    #full_model.compile(optimizer='adam',
    #              loss=tf.compat.v1.keras.losses.categorical_crossentropy,
    #              metrics=[f1])
    return model3
def findLargestValIndex(listA):
    largestindex = 0
    largestVal = -1
    #print(listA[0])
    for i in range(0,len(listA[0])):
        if listA[0][i] > largestVal:
            largestVal = listA[0][i]
            largestindex = i
    return  largestindex


stemmed = []
nonstemmed = []
classes = []
sequences = []
statisticalFeatures = []
def preprocess(df, istraining):
    #0.SEQ	1.PERSON	2.RELATEDPERSON	3.SAMEPERSON	4.LINK	5.CONTENT	6.RELATIONSHIPTYPE2

    for i in range(0,len(df.values)):
        seq = str(df.loc[i].values[0])
        personName = str(df.loc[i].values[1])
        personName2 = str(df.loc[i].values[2])
        samePerson = str(df.loc[i].values[3])
        if samePerson == 'TRUE':
            continue
        PersonTokens = [t[0] for t in scnlp.pos_tag(personName)]
        PersonTokens2 = [t[0] for t in scnlp.pos_tag(personName2)]
        Name2InName1 = len([t for t in PersonTokens2 if t in PersonTokens])
        content = str(df.loc[i].values[5])
        class1 = str(df.loc[i].values[6])
        if class1 != '' and class1 != 'nan' and class1 is not None:
            if istraining == False:
                continue
        else:
            if istraining == True:
                continue
        #preprocessSingle(content)
        s = re.sub("\d", " ", content)
        s = s.translate(str.maketrans('', '', string.punctuation))
        postags = scnlp.pos_tag(s)
        #tokens = [t[0] for t in postags]
        #tokens = [normalize2(t) for t in tokens]
        #tokens = [t for t in tokens if t not in stopwords]
        #print(' '.join( tokens))
        tokens = s.split(' ')
        nonstemmed.append( ' '.join( tokens))
        statisticalFeatures.append(Name2InName1)
        tokens = [stemmer.stem(t) for t in tokens]
        stemmed.append(' '.join(tokens))
        if istraining == True:
            classes.append(class1)
def preprocessSingle(sentence):
    s = re.sub("\d", " ", sentence)
    s = s.translate(str.maketrans('', '', string.punctuation))
    #postags = scnlp.pos_tag(s)
    #tokens = [t[0] for t in postags]
    tokens = s.split(' ')
    tokens = [normalize2(t) for t in tokens]
    #tokens = [t for t in tokens if t not in stopwords]
    # print(' '.join( tokens))
    nonstemmedSent = ' '.join(tokens)
    tokens = [stemmer.stem(t) for t in tokens]
    stemmedSent = ' '.join(tokens)
    return nonstemmedSent, stemmedSent
def AddColumnToTFIDF(tfidfSparse, addedColumn):
    newArray = np.zeros(shape=(tfidfSparse.toarray().shape[0], tfidfSparse.toarray().shape[1] + 1))
    for i in range(0, tfidfSparse.toarray().shape[0]):
        newArray[i] = np.append(tfidfSparse.toarray()[i],addedColumn[i])
    return newArray

preprocess(df, True)
tfidf = TfidfVectorizer(analyzer='word',  ngram_range=(1,1), max_features=500000)
tfidf = tfidf.fit(nonstemmed)
vocab = tfidf.vocabulary_
tfidfdata = tfidf.fit_transform(nonstemmed)

tfidfdata = AddColumnToTFIDF(tfidfdata,statisticalFeatures )

encoder = LabelEncoder()
y = encoder.fit_transform(classes)
print(encoder.classes_)
numOfClasses = len(encoder.classes_)
x_train, x_test, y_train, y_test = train_test_split(tfidfdata, y, test_size=0.3)
#x_trainStatistical, x_testStatistical, _, _ = train_test_split(statisticalFeatures, y, test_size=0.1)
y_test = np_utils.to_categorical(y_test, num_classes=numOfClasses)
y_train = np_utils.to_categorical(y_train, num_classes=numOfClasses)

#model = createModel(tfidfdata.shape[1])
#model.fit(x_train, y_train, epochs=30, verbose=2, validation_data=(x_test, y_test))
model = createModel(tfidfdata.shape[1])
model.fit((x_train), y_train, epochs=30, verbose=2, validation_data=(x_test, y_test))
loss, acc = model.evaluate(x_test, y_test, verbose=0)
ypred = model.predict(x_test)
print('Training Accuracy: %f' % (acc * 100))
print('Training F-Score: ', f1(y_test, ypred)*100)

#Labeling unseen data,
#first creating a new dataset with unseen values COMMENTED FOR RELATIONS CLASSIFIER

#df = pd.read_excel('ClassificationDS.xlsx',sheet_name='Sheet1' ,header=0)

df = pd.read_excel('relationsAnnotation.xlsx',sheet_name='Sheet1' ,header=0)
#preprocess(df, False)
df2 = pd.DataFrame(columns=['seq','name','content','class'])
df2 = pd.DataFrame(columns=['seq','name', 'name2','content','isconfirmed','class'])
counter = 0
tfidf = TfidfVectorizer(analyzer='word',  ngram_range=(1,1), max_features=500000, vocabulary=vocab)

for i in range(0,len(df.values)):
    seq = str(df.loc[i].values[0])
    personName = str(df.loc[i].values[1])
    personName2 = str(df.loc[i].values[2])

    samePerson = str(df.loc[i].values[4])
    originalContent = str(df.loc[i].values[5])
    if str(personName).strip() == str(personName2).strip():
        df2.loc[counter] = [seq, personName, personName2, originalContent, True, 'SAME PERSON']
        counter = counter + 1
        continue
    PersonTokens = [t[0] for t in scnlp.pos_tag(personName)]
    PersonTokens2 = [t[0] for t in scnlp.pos_tag(personName2)]
    Name2InName1 = len([t for t in PersonTokens2 if t in PersonTokens])
    if samePerson == 'TRUE':
        continue
    class1 = str(df.loc[i].values[6])
    if class1 != '' and class1 != 'nan' and class1 is not None:
        df2.loc[counter] = [seq, personName,personName2, originalContent, True, class1]
        counter = counter + 1
        continue

    content = preprocessSingle(str(df.loc[i].values[5]))[0]
    x = tfidf.fit_transform([content])
    x = AddColumnToTFIDF(x,[Name2InName1])
    y = model.predict(x)
    #print(y)
    class1 =  encoder.classes_[findLargestValIndex(y)]
    df2.loc[counter] = [seq, personName,personName2,originalContent, False, class1]
    print(seq, personName,personName2, originalContent, class1)
    counter = counter + 1
df2.to_csv('RelationsPredictions.csv', encoding='utf-8')

'''
preprocess(df2, False)
print (y)
df3 = pd.DataFrame(columns=['seq','name','content','class'])
counter = 0
for i in range(0,len(df2.values)):
    seq = str(df.loc[i].values[0])
    personName = str(df.loc[i].values[1])
    content = str(df.loc[i].values[2])
    print(seq, personName, content, class1)
    df3.loc[counter] = [seq, personName, content, class1]
    counter = counter + 1

'''