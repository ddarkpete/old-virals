import random

from cassandra.cluster import Cluster
from nltk import ngrams

VIRAL_ID = '720896_1'


def LongestSnippetRight(mainTab , docTab, i, k , snippet, lenMT, lenDT, density):
    iMax = i
    if JaccardDistance(mainTab[i],docTab[k]) > 0.2:
        snippet += ' ' + ' '.join( str(x) for x in docTab[k])
        #print(type(density))
        if i in density:
            density[i] += 1
        else:
            density[i] = 1
        if k + 10 < lenDT and i + 10 < lenMT:
            return LongestSnippetRight(mainTab,docTab,i + 10, k + 10, snippet, lenMT, lenDT,density)
        else:
            return [snippet,density, iMax]
    else:
        snippet += ' ' + ' '.join( str(x) for x in docTab[k])
        if i in density:
            density[i] += 1
        else:
            density[i] = 1
            iMax = i
        return [snippet , density, iMax]

def LongestSnippetLeft(mainTab , docTab, i, k , snippet,density):
        iMin = i
        if JaccardDistance(mainTab[i],docTab[k]) > 0.3:
            snippet += ' ' + ' '.join( str(x) for x in docTab[k])
            if i in density:
                density[i] += 1
            else:
                density[i] = 1
            if k - 10 > 0 and i - 10 > 0:
                return LongestSnippetLeft(mainTab,docTab,i - 10, k - 10, snippet, density)
            else:
                return [snippet, density, iMin]
        else:
            snippet += ' ' + ' '.join( str(x) for x in docTab[k])
            if i in density:
                density[i] += 1
            else:
                density[i] = 1
            return [snippet , density, iMin]


def JaccardDistance(a, b):
    a = set(a)
    b = set(b)
    return 1.0 * len(a&b)/len(a|b)

def LongestDocSnippet(i, start, end, ranges, maxLen):
    maxLen = end - start

    if i + 1 >= len(ranges):
        #print('dupa {} {} {}'.format(start, end, maxLen))
        tab = [start , end, maxLen]
        print(tab)
        return tab

    nextPair = ranges[i + 1]

    if nextPair[0] > end:
        #print('dupa {} {} {}'.format(start, end, maxLen))
        tab = [start , end, maxLen]
        print(tab)
        return tab
    elif nextPair[0] >= start and nextPair[0] <= end and nextPair[1] >= end:
        end = nextPair[1]
        return LongestDocSnippet(i + 1, start, end, ranges, maxLen)
    else:
        return LongestDocSnippet(i + 1, start, end, ranges, maxLen)

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

virals = session.execute("SELECT similar_pages from virals WHERE viral_id = '{}'".format(VIRAL_ID))
viralDensity = {}
viralIds = []
snpRanges = []

for v in virals:
    for s in v.similar_pages:
        viralIds.append(s)

viralIds = list(set(viralIds))
viralIdsStr = str(viralIds)[1:-1]

snipDict ={}


documents = session.execute("SELECT page_text from documents WHERE doc_page_id IN ({})".format(viralIdsStr))
docTexts = []
for d in documents:
    docTexts.append(d.page_text)
mainTextRow = session.execute("SELECT page_text from documents WHERE doc_page_id = '{}'".format(VIRAL_ID))
mainDoc10Grams = []
for m in mainTextRow:
        mainDoc10Grams = list(ngrams(m.page_text.split(), 10))


for j in range(0,len(docTexts)):
    text10Grams = list(ngrams(docTexts[j].split(), 10))
    snippets = []
    for i in range(0,len(mainDoc10Grams)):
            for k in range(0,len(text10Grams)):
                if JaccardDistance(mainDoc10Grams[i],text10Grams[k]) > 0.8:
                    '''
                    print(' '.join( str(i) for  i in text10Grams[k-50]) + ' '.join( str(i) for  i in text10Grams[k-40]) + ' '.join( str(i) for  i in text10Grams[k-30]) + ' '.join( str(i) for  i in text10Grams[k-20]) + ' '.join( str(i) for  i in text10Grams[k-10]) + ' '.join( str(i) for  i in text10Grams[k]) + ' '.join( str(i) for  i in text10Grams[k+10]))
                    print()
                    #break
                    '''
                    snp1=""
                    snp2=""
                    rightData = LongestSnippetRight(mainDoc10Grams,text10Grams,i,k,snp1,len(mainDoc10Grams),len(text10Grams), viralDensity)
                    snpRight = rightData[0]
                    viralDensity = rightData[1]
                    snpMaxI = rightData[2]
                    snpLeft = ""
                    snpMinI = 0
                    if i - 10 > 0 and k - 10 > 0:
                        leftData = LongestSnippetLeft(mainDoc10Grams,text10Grams,i - 10, k - 10, snp2, viralDensity)
                        snpLeft = leftData[0]
                        viralDensity = leftData[1]
                        snpMinI = leftData[2]
                        snpRange = [snpMinI, snpMaxI]
                        snp = snpLeft + snpRight
                        snpRanges.append(snpRange)
                        #print(snp)
                        snippets.append(snp)
    #print(viralIds[j])
    #print(max(snippets,key=len))
    #print()
    snipDict[viralIds[j]] = max(snippets,key=len).replace('\'', '' ).replace('"', '')

sortedViralDensity = sorted(viralDensity.items(), key=lambda kv: kv[1],reverse = True)
#print(sortedViralDensity)

snpRanges = sorted(snpRanges, key= lambda x: x[0])
maxLen = 0
beg = 0
end = 0
print(snpRanges)
for i in range(0,len(snpRanges)):
    res = LongestDocSnippet(i,snpRanges[i][0],snpRanges[i][1], snpRanges, maxLen)
    print(res)
    if res[2] > maxLen:
        maxLen = res[2]
        beg = res[0]
        end = res[1]

#print("{} {} {}".format(beg,end,maxLen))

bigSnippet = ' '.join( str(x) for x in mainDoc10Grams[beg])
for i in range(beg + 1, end):
    bigSnippet += ' ' + mainDoc10Grams[i][-1]

#print(bigSnippet)

bigSnippet = bigSnippet.replace('\'', '' ).replace('"', '')

cql = "UPDATE virals SET snippet = '{}' WHERE viral_id = '{}'".format(bigSnippet, VIRAL_ID)
session.execute(cql)


for docID , txt in snipDict.items():
    cql = "UPDATE documents SET snippets = snippets + {{'{}' : '{}'}} WHERE doc_page_id = '{}'".format(VIRAL_ID, txt, docID)
    session.execute(cql)
