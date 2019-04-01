for j in range(0, len(contentTokens)):
    # for k in NameTokens:
    # print(contentTokens, k[0])
    f = [x for x in preList if (x) == (contentTokens[j])]

    toCheck = False
    if len(f) != 0:
        if f[0] != '':
            toCheck = True

    if toCheck:
        # print(f)
        # if contentTokens[j] in str(preList):
        second = ''
        fullSentence = ''
        try:
            for m in range(1, 7):
                word = str(contentTokens[j + m])
                ff = [x for x in NamesDataset if x == word]
                if len(ff) != 0:
                    if ff[0] != '':
                        second = second + ' ' + ff[0]
                    else:
                        break
                else:
                    break
                    # second = second + ' ' + word
        except:
            ss = ''
        try:
            for m in range(1, 7):
                word = str(contentTokens[j + m])
                fullSentence = fullSentence + ' ' + word
        except:
            ss = ''
        # if second != '':
        #    print('ARTICLE',personName)
        #    print('FULL',fullSentence)
        #    print(contentTokens[j],second)

def compareNames(name1, name2, index):
    score = 0
    if name1[0] == name2[0] and name1[len(name1)-1] == name2[len(name2)-1]:
        score += 0.6
    if name1[0] == name2[0] and name1[1] == name2[1] and score==0:
        if len(name1) == 2:
            score += 0.8
        if len(name1) == 3:
            score += 0.5
        if len(name1) == 4:
            score += 0.3
    similarity = 0
    for i in range(0,len(name1) - 1):
        if 'عبد' == name1[i]:
            score -= 0.2
    for i in range(0,len(name1) - 1):
        ff = [x for x in name2 if x == name1[i]]
        if len(ff) > 0:
            if ff[0] != '':
                similarity += 1
    similarity = similarity / len(name1)
    score += 0.4 * similarity
    return score
