from cassandra.cluster import Cluster
from nltk import ngrams
import random

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')

docs = session.execute('SELECT doc_id from documents')

docIDs =[]

def jaccard_distance(a, b):
    """Calculate the jaccard distance between sets A and B"""
    a = set(a)
    b = set(b)
    return 1.0 * len(a&b)/len(a|b)

def checkIfVirExist(viralID):
    rows = session.execute("SELECT * FROM simpages WHERE id = {}".format(viralID))
    if not rows:
        return False
    else:
        return True

def insertOrUpdateViral(pag1_id, pag2_id, jaq_sim):
    if checkIfVirExist(p.doc_page_id):
        session.execute("UPDATE simpages SET sim = sim + ['{}'] WHERE id = {}").format(pag2_id, pag1_id)
    else:
        session.execute("INSERT INTO simpages (id,page_id, jaq_sim, sim)VALUES ('{}','{}','{}',{})".format(p.doc_page_id, p.doc_page_id,round(jq,4), p2.doc_page_id))

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
                if jq > 0.01:
                    insertOrUpdateViral(p.doc_page_id, p2.doc_page_id, jq)