from nltk.tag.stanford import StanfordPOSTagger as POS_Tag
_path_to_model = 'D:\stanford-postagger-2018-10-16\POSTagger\models\bidirectional-distsim-wsj-0-18.tagger'
_path_to_jar = 'D:\stanford-postagger-2018-10-16\POSTagger\stanford-postagger.jar'
st = POS_Tag(_path_to_model, _path_to_jar)

