from cassandra.cluster import Cluster
from nltk import ngrams
import random

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

METHOD_NAME = "4GRAMS"
NEW_STATUS = "NEW"
MIN_JAQ = 0.015

docs = session.execute('SELECT doc_id from documents')

docIDs =[]

def jaccard_distance(a, b):
    """Calculate the jaccard distance between sets A and B"""
    a = set(a)
    b = set(b)
    return 1.0 * len(a&b)/len(a|b)

def checkIfVirExist(viralID):
    rows = session.execute("SELECT * FROM virals WHERE viral_id = '{}'".format(viralID))
    if not rows:
        return False
    else:
        return True

def insertOrUpdateViral(pag1_id, pag2_id):
    if checkIfVirExist(p.doc_page_id):
        session.execute("UPDATE virals SET similar_pages = similar_pages + ['{}'] WHERE viral_id = '{}'".format(pag2_id, pag1_id))
    else:
        session.execute("INSERT INTO virals (viral_id,page_id, similar_pages, status, method_name)VALUES ('{}','{}',['{}'],'{}','{}')".format(p.doc_page_id, p.doc_page_id, p2.doc_page_id,NEW_STATUS,METHOD_NAME))

for doc in docs:
    docIDs.append(doc.doc_id)
    #print(doc.doc_id)

docIDs = list(set(docIDs))
#docIDs =  random.sample(docIDs, 50)

lenDocIDs = len(docIDs)
print(lenDocIDs)
for i in range(0,lenDocIDs - 1):
    for j in range( i + 1, lenDocIDs):
        page1 = session.execute('SELECT doc_id , doc_page_id , page_text from documents WHERE doc_id = {} ALLOW FILTERING'.format(docIDs[i]))
        page2 = session.execute('SELECT doc_id , doc_page_id , page_text from documents WHERE doc_id = {} ALLOW FILTERING'.format(docIDs[j]))
        for p in page1:
            page1_4grams = list(ngrams(p.page_text.split(), 4))
            for p2 in page2:
                page2_4grams = list(ngrams(p2.page_text.split(),4))
                jq = jaccard_distance(page1_4grams,page2_4grams)
                if jq > MIN_JAQ:
                    print('insert')
                    insertOrUpdateViral(p.doc_page_id, p2.doc_page_id)