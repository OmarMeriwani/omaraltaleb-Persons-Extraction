import pandas as pd

df = pd.read_excel('ClassificationDS.xlsx',sheet_name='Sheet2' ,header=0)
print(df.head())
for i in range(0,len(df.values)):

    seq = str(df.loc[i].values[0])
    personName = str(df.loc[i].values[1])
    print (seq,personName)