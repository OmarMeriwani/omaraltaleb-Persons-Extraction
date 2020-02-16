import pandas as pd
from NameFunctions import normalize2
from stanfordcorenlp import StanfordCoreNLP
import os
import re
import string
import nltk.stem.isri
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import tensorflow as tf
from tfevaluation import f1
from keras.layers import Dense, Dropout
from keras.models import Sequential

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

df = pd.read_excel('ClassificationDS.xlsx',sheet_name='Sheet2' ,header=0)
df_stopwords = pd.read_csv('arabicStopWords')
stopwords = []
for i in df_stopwords.values:
    stopwords.append(normalize2(str(i[0])))
print(stopwords)

def createModel(dim):
    model = Sequential()
    model.add(Dense(1400, activation='relu', input_dim=dim)) #64396
    model.add(Dropout(0.5))
    #model.add(Dense(600))
    #model.add(Dropout(0.5))
    model.add(Dense(numOfClasses, activation='softmax'))
    model.compile(optimizer='adam',
                  loss=tf.compat.v1.keras.losses.categorical_crossentropy,
                  metrics=[f1])
    return model

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
#sequences = []
statisticalFeatures = []
#for i in range(0, len(df.values)):
#    sequences.append(df.loc[i].values[0])
def preprocess(df, istraining):
    for i in range(0,len(df.values)):
        seq = str(df.loc[i].values[0])
        content = str(df.loc[i].values[2])
        if istraining == True:
            class1 = str(df.loc[i].values[5])
            politics = int(df.loc[i].values[4])
            religion = int(df.loc[i].values[5])
            military = int(df.loc[i].values[6])
        #print (seq,personName)
        s = re.sub("\d", " ", content)
        s = s.translate(str.maketrans('', '', string.punctuation))
        tokens = scnlp.pos_tag(s)
        tokens = [t[0] for t in tokens]
        tokens = [normalize2(t) for t in tokens]
        tokens = [t for t in tokens if t not in stopwords]
        #print(' '.join( tokens))
        nonstemmed.append( ' '.join( tokens))
        statisticalFeatures.append([len(tokens), ])
        tokens = [stemmer.stem(t) for t in tokens]
        stemmed.append(' '.join(tokens))
        if istraining == True:
            classes.append(class1)

preprocess(df, True)
tfidf = TfidfVectorizer(analyzer='word',  ngram_range=(1,1), max_features=500000)
tfidf = tfidf.fit(stemmed)
vocab = tfidf.vocabulary_
tfidfdata = tfidf.fit_transform(stemmed)

encoder = LabelEncoder()
y = encoder.fit_transform(classes)
print(encoder.classes_)
numOfClasses = len(encoder.classes_)
x_train, x_test, y_train, y_test = train_test_split(tfidfdata, y, test_size=0.1)
y_test = np_utils.to_categorical(y_test, num_classes=numOfClasses)
y_train = np_utils.to_categorical(y_train, num_classes=numOfClasses)

#model = createModel(tfidfdata.shape[1])
#model.fit(x_train, y_train, epochs=30, verbose=2, validation_data=(x_test, y_test))
model = createModel(tfidfdata.shape[1])
model.fit(x_train, y_train, epochs=30, verbose=2, validation_data=(x_test, y_test))
loss, acc = model.evaluate(x_test, y_test, verbose=0)
ypred = model.predict(x_test)
print('Training Accuracy: %f' % (acc * 100))
print('Training F-Score: ', f1(y_test, ypred)*100)

#Labeling unseen data,
#first creating a new dataset with unseen values COMMENTED FOR RELATIONS CLASSIFIER

df = pd.read_excel('ClassificationDS.xlsx',sheet_name='Sheet1' ,header=0)
df2 = pd.DataFrame(columns=['seq','name','content','class'])
counter = 0
tfidf = TfidfVectorizer(analyzer='word',  ngram_range=(1,1), max_features=500000, vocabulary=vocab)

for i in range(0,len(df.values)):
    seq = str(df.loc[i].values[0])
    personName = str(df.loc[i].values[1])
    personName2 = str(df.loc[i].values[2])
    samePerson = str(df.loc[i].values[4])
    if samePerson == 'TRUE':
        continue
    content = str(df.loc[i].values[5])
    #if seq in sequences:
    #   continue
    x = tfidf.fit_transform([content])
    y = model.predict(x)
    #print(y)
    class1 =  encoder.classes_[findLargestValIndex(y)]
    df2.loc[counter] = [seq, personName, content, class1]
    print(seq, personName, content, class1)
    counter = counter + 1
df2.to_csv('ReligionPredictions.csv', encoding='utf-8')

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