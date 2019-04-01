from nltk.tag.stanford import StanfordPOSTagger
from nltk import word_tokenize
from nltk.internals import find_jars_within_path

import os

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path


_path_to_model = 'D:/stanford-postagger-2018-10-16/models/arabic-accurate.tagger'
_path_to_jar = 'D:/stanford-postagger-2018-10-16/stanford-postagger-3.9.2.jar'


#st = StanfordPOSTagger(_path_to_model, _path_to_jar,encoding='utf8')

#print(st.tag(word_tokenize('ذهب الولد إلى البيت')))

import CorenlpPOS as n
stt = n.StanfordNLP.pos('ولما التقينا كشفنا عن جماجمنا')
print(stt)