import nltk.tokenize.stanford_segmenter as stfd
import os
_path_to_jar = 'D:/stanford-segmenter/stanford-segmenter-3.9.2.jar'
java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
'''STANFORD_SEGMENTER'''
os.environ['STANFORD_SEGMENTER'] = 'D:/stanford-segmenter/data/arabic-segmenter-atb+bn+arztrain.ser.gz'

t = stfd.StanfordSegmenter(_path_to_jar)
t.default_config('ar')
tk = str(t.segment('ذهب الولد إلى بيته ووجد أباه. ثم خرج'.split()))
print(tk.split(' '))