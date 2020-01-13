import pandas as pd
from NameFunctions import compareNames, findMostSimilar, normalize, normalize2, unique, fixArabicNames, combineRelations, getRelation, getFiveBefore, getFiveAfter

testCases = pd.read_csv('testcases.csv',encoding='cp1256', header=0).values.tolist()
resultsDataset = pd.read_csv('resultdataset.csv',encoding='cp1256', header=0).values.tolist()
counts = {}
testCounts = {}
for result in resultsDataset:
    if  counts.get(result[0]) == None:
        counts[result[0]] = 1
    else:
        counts[result[0]] = counts[result[0]] + 1
for result in testCases:
    if  testCounts.get(result[0]) == None:
        testCounts[result[0]] = 1
    else:
        testCounts[result[0]] = testCounts[result[0]] + 1
print('Number of retrieved names: ', counts)
print('Numbers in test cases: ', testCounts)

'''Check cases counts'''
LinksRecall = []
SamePersonRecall = []
MentionsRecall = []
MentionsPrecision = []
RelationsRecall = []
RelationsPrecision = []
PreviousArticle = ''
print(resultsDataset)
for result in testCases:
    ArticleName = result[0]
    if ArticleName != PreviousArticle:
        print(f'Testing {ArticleName}...')
        AvailableCases = [n for n in resultsDataset if n[0].strip() == ArticleName.strip()]
        print(f'Found {len(AvailableCases)}')
        OriginalCases = [n[5] for n in testCases if n[0].strip() == ArticleName.strip()]
        print(f'Original cNameFrequenciesases {len(OriginalCases)}')
        print(f'Retrival rate: {len(AvailableCases) / len(OriginalCases) * 100}%')

        OriginalLinkCases = [n[5] for n in testCases if n[0].strip() == ArticleName.strip()  and n[5] is not None]
        AvailableLinkCases = [n[5] for n in testCases if n[0].strip() == ArticleName.strip()
                              and n[5] is not None
                              and n[5] in [m[5] for m in AvailableCases if m[5] is not None]]
        if len(OriginalLinkCases) != 0:
            Recall = round(len(AvailableLinkCases) / len(OriginalLinkCases), 2) * 100
            LinksRecall.append(Recall)
            print(f'Links {len(AvailableLinkCases)}, Recall:{Recall}% Cases found: {AvailableLinkCases}')
        else:
            print(f'Links 0')

        SamePersonCases = [n[5] for n in testCases if n[0].strip() == ArticleName.strip()  and n[2] == True]
        SamePersonDetected = [n[2] for n in AvailableCases if n[2] == True]
        if len(SamePersonCases) != 0:
            Recall = round(len(SamePersonDetected) / len(SamePersonCases), 2) * 100
            SamePersonRecall.append(Recall)
            print(f'Same Person Cases {len(SamePersonDetected)}, Recall:{Recall}% original count: {len(SamePersonCases)}')
        else:
            print(f'Same Person Cases 0')

        OriginalMentionCases = [n for n in testCases if n[0].strip() == ArticleName.strip()]
        MentionsDetected = 0
        RelationsDetected = 0
        Mentions = []
        Relations = []
        for case in AvailableCases:
            for test in OriginalMentionCases:
                if case is not None and test is not None:
                    if compareNames(case[1], test[1],30, NameFrequencies) >= 0.4:
                        MentionsDetected += 1
                        Mentions.append(case)
                        if case[3] == test[3]:
                            Relations.append(case[3])
                            RelationsDetected += 1
                        break
        if len(AvailableCases) > 0:
            precMentions = round((MentionsDetected) / len(AvailableCases), 2) * 100
            precRelations = round((RelationsDetected) / len(AvailableCases), 2) * 100
        else:
            precRelations = 0
            precMentions = 0
            if len(OriginalCases) > 0:
                MentionsRecall.append(0)
                MentionsPrecision.append(0)
                RelationsRecall.append(0)
                RelationsPrecision.append(0)
        if OriginalMentionCases != 0:
            Recall = round((MentionsDetected) / len(OriginalMentionCases), 2) * 100
            MentionsRecall.append(Recall)
            MentionsPrecision.append(precMentions)
            print(f'Mentions {(MentionsDetected)}, Recall:{Recall}% Precision: {precMentions}% original count: {len(OriginalMentionCases)}, cases:{[n[1] for n in Mentions]}')
            Recall = round((RelationsDetected) / len(OriginalMentionCases), 2) * 100
            RelationsRecall.append(Recall)
            RelationsPrecision.append(precRelations)
            print(f'Relations {(RelationsDetected)}, Recall:{Recall}% Precision: {precRelations}% original count: {len(OriginalMentionCases)}, cases:{Relations}')
        print('-----------------------------------------------------------------------')
    else:
        continue
    PreviousArticle = ArticleName
import statistics
print(f'Average links recall: {round(statistics.mean(LinksRecall),2)}')
print(f'Average same person recall: {statistics.mean(SamePersonRecall)}')
print(f'Average mentions recall: {statistics.mean(MentionsRecall)}')
print(f'Average mentions precision: {statistics.mean(MentionsPrecision)}')
print(f'Average relations recall: {statistics.mean(RelationsRecall)}')
print(f'Average relations precision: {statistics.mean(RelationsPrecision)}')
print('============================= TOTAL RESULTS ============================')
AvailableCases = [n for n in resultsDataset]
OriginalCases = [n[5] for n in testCases]
OriginalLinkCases = [n[5] for n in testCases if  n[5] is not None]
AvailableLinkCases = [n[5] for n in testCases if n[5] is not None
                      and n[5] in [m[5] for m in AvailableCases if m[5] is not None]]
if len(OriginalLinkCases) != 0:
    Recall = round(len(AvailableLinkCases) / len(OriginalLinkCases), 2) * 100
    LinksRecall.append(Recall)
    print(f'Recall:{Recall}% , Links {len(AvailableLinkCases)} Cases')
SamePersonCases = [n[5] for n in testCases if  n[2] == True]
SamePersonDetected = [n[2] for n in AvailableCases if n[2] == True]
if len(SamePersonCases) != 0:
    Recall = round(len(SamePersonDetected) / len(SamePersonCases), 2) * 100
    SamePersonRecall.append(Recall)
    print(f'Same person Recall:{Recall}%, Same Person Cases {len(SamePersonDetected)}, original count: {len(SamePersonCases)}')
else:
    print(f'Same Person Cases 0')

OriginalMentionCases = [n for n in testCases]
MentionsDetected = 0
RelationsDetected = 0
Mentions = []
Relations = []
for case in AvailableCases:
    for test in OriginalMentionCases:
        if case is not None and test is not None:
            if compareNames(case[1], test[1], 30, NameFrequencies) >= 0.4:
                MentionsDetected += 1
                Mentions.append(case)
                if case[3] == test[3]:
                    Relations.append(case[3])
                    RelationsDetected += 1
                break
if len(AvailableCases) > 0:
    precMentions = round((MentionsDetected) / len(AvailableCases), 2) * 100
    precRelations = round((RelationsDetected) / len(AvailableCases), 2) * 100
else:
    precRelations = 0
    precMentions = 0
    if len(OriginalCases) > 0:
        MentionsRecall.append(0)
        MentionsPrecision.append(0)
        RelationsRecall.append(0)
        RelationsPrecision.append(0)
if OriginalMentionCases != 0:
    Recall = round((MentionsDetected) / len(OriginalMentionCases), 2) * 100
    MentionsRecall.append(Recall)
    MentionsPrecision.append(precMentions)
    print(f'Mentions {(MentionsDetected)}, Recall:{Recall}% Precision: {precMentions}% original count: {len(OriginalMentionCases)}, cases:{[n[1] for n in Mentions]}')
    Recall = round((RelationsDetected) / len(OriginalMentionCases), 2) * 100
    RelationsRecall.append(Recall)
    RelationsPrecision.append(precRelations)
    print(f'Relations {(RelationsDetected)}, Recall:{Recall}% Precision: {precRelations}% original count: {len(OriginalMentionCases)}, cases:{Relations}')
