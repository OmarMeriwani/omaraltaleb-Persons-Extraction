import pandas as pd
from NameFunctions import normalize2
df = pd.read_csv('OmarAlTalebSheet.csv',encoding='utf-8',header=0)
print(df.head())
NamesAndContentList = []
for i in range(0,len(df.values)):
    personName = str(df.loc[i].values[0])
    personName = personName.replace('  ', ' ')
    personTokens = df.loc[i].values[1]
    Numbers = df.loc[i].values[2]
    DeathYear = bool(df.loc[i].values[3])
    content = str(df.loc[i].values[4])
    sents = df.loc[i].values[5]
    events = df.loc[i].values[6]
    NamesAndContentList.append([personName, content])
df2 = pd.DataFrame(NamesAndContentList,columns=['name','content'])
df2.to_csv('classificationDS.csv',encoding='utf-8')