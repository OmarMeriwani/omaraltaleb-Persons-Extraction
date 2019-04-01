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
