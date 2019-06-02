from cassandra.cluster import Cluster
from nltk import ngrams
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
import random
'''
def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude
'''

def checkIfVirExist(viralID):
    rows = session.execute("SELECT * FROM virals WHERE viral_id = '{}'".format(viralID))
    if not rows:
        return False
    else:
        return True

def insertOrUpdateViral(p, p2):
    if checkIfVirExist(p.doc_page_id + '_TFIDF'):
        session.execute("UPDATE virals SET similar_pages = similar_pages + ['{}'] WHERE viral_id = '{}'".format(p.doc_page_id, p2.doc_page_id))
    else:
        session.execute("INSERT INTO virals (viral_id,page_id, similar_pages, status, method_name, page_title)VALUES ('{}','{}',['{}'],'{}','{}','{}')".format(p.doc_page_id + '_TFIDF', p.doc_page_id, p2.doc_page_id,NEW_STATUS,METHOD_NAME, p.doc_title))


tokenize = lambda doc: doc.lower().split(' ')
sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

METHOD_NAME = "TFIDF"
NEW_STATUS = "NEW"

#docs = session.execute('SELECT doc_page_id from documents')


docIDs =[]
'''
for doc in docs:
    docIDs.append(doc.doc_page_id)
    #print(doc.doc_id)
'''

tag = session.execute("SELECT documents FROM tags WHERE tagname = '{}'".format("JAKPODAJA"))
for t in tag:
    for pagid in t.documents:
        docIDs.append(pagid)


docIDs = list(set(docIDs))
random.shuffle(docIDs)
lenDocIDs = len(docIDs)
print(lenDocIDs)
for i in range(0,lenDocIDs - 1):
    page1 = session.execute("SELECT doc_id , doc_page_id , page_text , doc_title from documents WHERE doc_page_id = '{}' ALLOW FILTERING".format(docIDs[i]))
    for p in page1:
        document_0 = p.page_text.replace('/', '')
        document_0 = ' '.join([word for word in document_0.split() if len(word) > 1])
        document_0_title = p.doc_title
    for j in range( i + 1, lenDocIDs):
        page2 = session.execute("SELECT doc_id , doc_page_id , page_text , doc_title from documents WHERE doc_page_id = '{}' ALLOW FILTERING".format(docIDs[j]))
        for p2 in page2:
            document_1 = p2.page_text.replace('/', '')
            document_1 = ' '.join([word for word in document_1.split() if len(word) > 1])
            document_1_title = p2.doc_title
            if document_0_title == document_1_title:
                break
            all_documents = [document_0 ,document_1]
            tfidf = sklearn_tfidf.fit_transform(all_documents)
            similarityMatrix = cosine_similarity(tfidf)
            #print(similarityMatrix[0][1])
            if similarityMatrix[0][1] > 0.2:
                print('insert {}'.format(similarityMatrix[0][1]))
                #print(similarityMatrix[0][1])
                insertOrUpdateViral(p, p2)
            #exit()
            '''
            tfidf_comparisons = []
            for count_0, doc_0 in enumerate(tfidf.toarray()):
                for count_1, doc_1 in enumerate(tfidf.toarray()):
                    tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
            
            for x in sorted(tfidf_comparisons, reverse = True):
                print(x)
            '''



