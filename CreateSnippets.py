import random

from cassandra.cluster import Cluster
from nltk import ngrams

VIRAL_ID = '720896_1'


def LongestSnippetRight(mainTab , docTab, i, k , snippet, lenMT, lenDT):
        if JaccardDistance(mainTab[i],docTab[k]) > 0.2:
            snippet += ' ' + ' '.join( str(i) for  i in docTab[k])
            if k + 10 < lenDT and i + 10 < lenMT:
                return LongestSnippetRight(mainTab,docTab,i + 10, k + 10, snippet, lenMT, lenDT)
            else:
                return snippet
        else:
            snippet += ' ' + ' '.join( str(i) for  i in docTab[k])
            return snippet

def LongestSnippetLeft(mainTab , docTab, i, k , snippet):
        if JaccardDistance(mainTab[i],docTab[k]) > 0.3:
            snippet += ' ' + ' '.join( str(i) for  i in docTab[k])
            if k - 10 > 0 and i - 10 > 0:
                return LongestSnippetLeft(mainTab,docTab,i - 10, k - 10, snippet)
            else:
                return snippet
        else:
            snippet += ' ' + ' '.join( str(i) for  i in docTab[k])
            return snippet


def JaccardDistance(a, b):
    a = set(a)
    b = set(b)
    return 1.0 * len(a&b)/len(a|b)

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

virals = session.execute("SELECT similar_pages from virals WHERE viral_id = '{}'".format(VIRAL_ID))
viralIds = []
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
                    snpRight = LongestSnippetRight(mainDoc10Grams,text10Grams,i,k,snp1,len(mainDoc10Grams),len(text10Grams))
                    snpLeft = ""
                    if i - 10 > 0 and k - 10 > 0:
                        snpLeft = LongestSnippetLeft(mainDoc10Grams,text10Grams,i - 10, k - 10, snp2)
                    snp = snpLeft + snpRight
                    snippets.append(snp)
    print(viralIds[j])
    print(max(snippets,key=len))
    print()
    snipDict[viralIds[j]] = max(snippets,key=len).replace('\'', '' ).replace('"', '')


for docID , txt in snipDict.items():
    cql = "UPDATE documents SET snippets = snippets + {{'{}' : '{}'}} WHERE doc_page_id = '{}'".format(VIRAL_ID, txt, docID)
    session.execute(cql)
