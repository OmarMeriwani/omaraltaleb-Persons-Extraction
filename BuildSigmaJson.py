import pandas as pd
from NameFunctions import compareNames, getNameFrequencies, fixname, normalize, fixArabicNames
import re
import json

df = pd.read_csv('OmarAlTalebSheet.csv',encoding='utf-8',header=0)
#cleanString,tokens,numbers,IsDeathYear,content,sentences,events

df2 = pd.read_csv('ClassificationDS.csv',encoding='utf-8',header=0)
df3 = pd.read_csv('resultsdataset.csv',encoding='utf-8',header=0).values.tolist()
#1.Name, 2.RelatedPerson, 3.SamePerson, 4.Relationship Type, 5.Relationship, 6.Connection, 7.FiveBefore

df4 = pd.read_excel('ClassificationDS.xlsx',sheet_name='Sheet2' ,header=0).values.tolist()
df5 = pd.read_csv('classPredictions.csv',encoding='utf-8',header=0).values.tolist()
df6 = pd.read_csv('ReligionPredictions.csv',encoding='utf-8',header=0).values.tolist()
df7 = pd.read_csv('PoliticsPredictions.csv',encoding='utf-8',header=0).values.tolist()

#This is to make the main nodes, that consists of a sequence and a name
namesDict = []
sequence = 0
dflist = df.values.tolist()
for i in range(0, len(dflist)):
    sequence = int(df2.loc[i][0])
    name = (str(df.loc[i][0]).strip())
    name = ' '.join(fixArabicNames([normalize(p) for p in name.split(' ')], False))
    #Adding sequences and names
    #print(name,df2.loc[i][1] )
    namesDict.append([sequence, name, str(df2.loc[i][1])])

#This is to create nodes for the names that are mentioned in the relations and that does not include confirmed connected articles
#it will be similar to creating a virtual profile of connections for persons that weren't mentioned directly in the book
relationsNodes = []
nameAliases = []
nameFrequencies = getNameFrequencies(df)
sequence += 1
for i in range(0,len(df3)):
    #name = str(df3[i][1]).strip()
    #seq = str(df3[i][0]).strip()
    relatedPerson = str(df3[i][2]).strip()
    isSamePerson = df3[i][3]
    connection = str(df3[i][6])
    isConnectionAvailable = False if  connection == '' or connection is None or connection == 'nan' else True
    #Only add the persons who're not already specified, and the persons that aren't the same person mentioned
    if isConnectionAvailable == False and isSamePerson == False:
        #In the first case the node will be added directly
        if len(relationsNodes) == 0:
            relationsNodes.append([sequence, relatedPerson])
            sequence += 1
        else:
            existingInCurrentNodes = False
            for n in relationsNodes:
                if str(relatedPerson).strip() == str(n[1]).strip():
                    existingInCurrentNodes = True
                    break
            #If there was already other nodes added, then check into each of them
            if existingInCurrentNodes == False:
                for n in relationsNodes:
                    #if str(relatedPerson).strip() == str(n).strip():

                    #If the new related person is very similar to an existing added node, then it's an alias
                    #print('compare(', relatedPerson, ',',  n[1], ')')
                    if compareNames(relatedPerson, n[1],30, nameFrequencies) >= 0.6:
                        nameAliases.append([n[0], relatedPerson])
                        break
                    else:
                        #If it wasn't similar to an existing one, and doesn't exist in aliases, then it's a new node
                        if relatedPerson not in nameAliases:
                            relationsNodes.append([sequence, relatedPerson])
                            sequence = sequence + 1
                            break


#for i in relationsNodes:
#    print('relation',i, 'aliases', [t for t in nameAliases if t[0] == i[0]])
nodes = []
edges = []
primaryNodesRelations = []
yearsDict = {}
yCounter = 20
for i in range(0,len(df)):
    events = [ int(n) for n in  re.findall(r'\d+', str(df.loc[i][6])) if int(n) > 1800 and int(n) < 2020]
    events.sort()
    #if len(events) > 0:
    #    print(events)
    lifetime = [ int(n) for n in  re.findall(r'\d+', str(df.loc[i][2]))]
    DeathYear = bool(df.loc[i].values[3])
    #print('lifetime', lifetime, DeathYear)
    seq = str(df2.loc[i][0])
    name = (str(df.loc[i][0]).strip())
    name = ' '.join(fixArabicNames([normalize(p) for p in name.split(' ')],False))
    #print(name)

    startingPoint = 0
    endPoint = 0
    allDates = events + lifetime
    if len(events) != 0:
        minDate = min([t for t in allDates if t > 1800 and t < 2020])
        maxDate = max([t for t in allDates if t > 1800 and t < 2020])
        maxEvent = max([t for t in events if t > 1800 and t < 2020])
        minEvent = max([t for t in events if t > 1800 and t < 2020])
    if len(lifetime) == 0:
        startingPoint = minDate
        endPoint = maxDate
    elif len(lifetime) == 1:
        if DeathYear == False:
            startingPoint = lifetime[0]
            if maxEvent > startingPoint:
                endPoint =  maxEvent
            else:
                endPoint = startingPoint + 50
        else:
            endPoint = lifetime[0]
            if minEvent < endPoint:
                startingPoint = minEvent
            else:
                startingPoint = endPoint
    else:
        startingPoint = min(lifetime)
        endPoint = max(lifetime)
    if startingPoint < 1800:
        startingPoint += 580
    NodeX = int((startingPoint) * 100)
    NodeY = 0
    if yearsDict.get(NodeX) == None:
        yearsDict[NodeX] = 1
        yCounter = 20 #20 is like zero
        NodeY = yCounter


    else:
        yearsDict[NodeX] = yearsDict[NodeX] + 1
        yCounter += 5
        NodeY = yCounter
    '''
    if i % 2 == 0:
        NodeY += 500
    if i % 3 == 0:
        NodeY += 500
    if i % 4 == 0:
        NodeY += 500
    if i % 2 == 0:
        NodeY = NodeY * -1
    '''
    #print(startingPoint, endPoint)
    # ====================== Classes
    classes =  [t[3] for t in df4 if t[3] != None and t[3] != '' and str(t[0]).strip() == str(seq).strip() ]
    confirmedClass = '' if len(classes) == 0 else classes[0]
    classes2 = [t[4] for t in df5 if t[4] != None and t[4] != '' and str(t[0]).strip() == str(seq).strip() ]
    predictedClass = '' if len(classes2) == 0 else classes2[0]
    class1 = predictedClass if confirmedClass == '' else confirmedClass
    ClassColorDict = [['Army', '#4b5320', 0, 1], ['Religion', '#5e5f56', 1000, 1], ['Journalism','#deb22e', 2000, 1],  ['Government','#3400ff', 3000, 1],
                      ['Jurisdiction', '#08001f', 4000, 1],
                      ['Health','#a9d9e1', 0, -1],['Education','#0095ff', 1000, -1], ['Art','#ff0000', 2000, -1],
                          ['Literature','#ffc800', 3000, -1], ['Sport','#e200ff', 4000, -1],
                          ['Business','#137aa2', 5000, -1]]
    #print(class1)
    if class1 != '':
        ClassColor = [t[1] for t in ClassColorDict if t[0] == class1][0]
        NodeY += [t[2] for t in ClassColorDict if t[0] == class1][0]
        NodeY *= [t[3] for t in ClassColorDict if t[0] == class1][0]
    else:
        ClassColor = '#dedede'
        NodeY = (NodeY + 2000) * -1
    #print(class1, ClassColor)
    # ====================== Religion
    religiousActivity1 = [t[5] for t in df4 if t[5] != None and t[5] != '' and str(t[0]).strip() == str(seq).strip()]
    confirmedClass = '' if len(religiousActivity1) == 0 else religiousActivity1[0]
    religiousActivity2 = [t[4] for t in df6 if t[4] != None and t[4] != '' and str(t[0]).strip() == str(seq).strip()]
    predictedClass = '' if len(religiousActivity2) == 0 else religiousActivity2[0]
    religiousActivity = str(predictedClass) + ':P' if str(confirmedClass) == '' else str(confirmedClass) + ':C'

    # ====================== Politics
    political1 = [t[4] for t in df4 if t[4] != None and t[4] != '' and str(t[0]).strip() == str(seq).strip()]
    confirmedClass = '' if len(political1) == 0 else political1[0]
    political2 = [t[4] for t in df7 if t[4] != None and t[4] != '' and str(t[0]).strip() == str(seq).strip()]
    predictedClass = '' if len(political2) == 0 else political2[0]
    politicalActivity = str(predictedClass) + ':P' if str(confirmedClass) == '' else str(confirmedClass) + ':C'

    # ===================== Relations
    connectionsNamesWithoutArticles = [n[2] for n in df3 if str(n[1]).strip() == name.strip()
                                       and (str(n[6]) == '' or str(n[6]) is None or str(n[6]) == 'nan')
                                       and n[3] == False]
    #Node Size
    NodeSize = len( [n[2] for n in df3 if str(n[1]).strip() == name.strip() and n[3] == False])
    node = {
        "id" : seq,
        "label" : name + ' ' + str(startingPoint),
        "x": NodeX,
        "y": NodeY,
        "color": ClassColor,
        "size": 1+ NodeSize,
        "label2": name
    }
    nodes.append(node)
    primaryNodesRelations.append([seq, NodeX, name, connectionsNamesWithoutArticles ])
#print(nodes)
yearsDict = {}
xDict = {}
yCounter = 1000
nodes2 = []
for node in relationsNodes:
    sequence = node[0]
    name = node[1]
    NodeY = 1000
    #Get the names of the people who're connected with the current node
    connectionsNamesWithoutArticles = [n[1] for n in df3 if str(n[2]).strip() == name.strip()
                                       and (str(n[6]) == '' or str(n[6]) is None or str(n[6]) == 'nan')
                                       and n[3] == False]
    #print(len(connectionsNamesWithoutArticles))
    #Eliminate duplicates
    size = len(connectionsNamesWithoutArticles)
    connectionsNamesWithoutArticles = set(connectionsNamesWithoutArticles)
    minX = 0
    for connection in connectionsNamesWithoutArticles:
        minX = min([ int(list(n.values())[2]) for n in nodes if str(list(n.values())[6]).strip() == str(connection).strip()])
    if minX / 100 < 1800:
        minX = 1800
    notstored = True
    while notstored:
        if xDict.get(minX) != None:
            minX += 5
        else:
            xDict[minX] = 1
            notstored = False
    if yearsDict.get(minX) == None:
        yearsDict[minX] = 1
        yCounter = 1000  # 20 is like zero
        NodeY = yCounter
    else:
        yearsDict[NodeX] = yearsDict[NodeX] + 1
        yCounter += 50
        NodeY = yCounter
    if i % 2 == 0:
        NodeY += 100
    if i % 3 == 0:
        NodeY += 100
    if i % 4 == 0:
        NodeY += 100
    node = {
        "id": sequence,
        "label": name,
        "x": minX,
        "y": NodeY,
        "size": size
    }
    nodes2.append(node)
#print(nodes2)
edgeId = 1
edges = []
for node in nodes:
    seq1 = int(list(node.values())[0])
    name = str(list(node.values())[6])
    connectionsNamesWithoutArticles = [n[2] for n in df3 if str(n[1]).strip() == name.strip()
                                       and (str(n[6]) == '' or str(n[6]) is None or str(n[6]) == 'nan')
                                       and n[3] == False]
    #print(seq1, name, connectionsNamesWithoutArticles)
    seqs2 = [n for n in relationsNodes if str(n[1]).strip() in [str(m).strip() for m in connectionsNamesWithoutArticles]]
    #print(seqs2)
    if len(seqs2) != 0:
        for s in seqs2:
            edge = {
                "id": edgeId,
                "source": seq1,
                "size": 3,
                "target": s[0]
            }
            edgeId += 1
            edges.append(edge)
#print(edges)
edges2 = []
for node in nodes:
    seq1 = int(list(node.values())[0])
    name = str(list(node.values())[6])
    connectionsNamesArticles = [n[2] for n in df3 if str(n[1]).strip() == name.strip()
                                       and (str(n[6]) != '' or str(n[6]) is not None or str(n[6]) != 'nan')
                                       and n[3] == False]
    #print(seq1, name, connectionsNamesArticles)
    seqs2 = [n for n in namesDict if str(n[1]).strip() in [str(m).strip() for m in connectionsNamesArticles]]
    #print(seqs2)
    if len(seqs2) != 0:
        for s in seqs2:
            edge = {
                "id": edgeId,
                "source": seq1,
                "size": 3,
                "target": s[0]
            }
            edgeId += 1
            edges2.append(edge)
    #print(sequence, name,minX, NodeY, size)
#print(edges2)
#print(nodes + nodes2)
#print(edges + edges2)
data = {}
data['nodes'] = nodes #+ nodes2
data['edges'] = edges2 #+ edges
json_data = json.dumps(data, ensure_ascii=False)
with open('finalrelations.json', 'w', encoding='utf-8') as my_data_file:
    my_data_file.write(json_data)
    my_data_file.close()
# ====================== Connections
#1.Name, 2.RelatedPerson, 3.SamePerson, 4.Relationship Type, 5.Relationship, 6.Connection, 7.FiveBefore
'''
   
    {
  "nodes": [
    {
      "id": "n0",
      "label": "A node",
      "x": 0,
      "y": 0,
      "size": 3
    }
  ],
  "edges": [
    {
      "id": "e0",
      "source": "n0",
      "target": "n1"
    }
  ]
}

    '''