from cassandra.cluster import Cluster
from nltk import ngrams
import random
import mmh3

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

METHOD_NAME = "4GRAMS"
NEW_STATUS = "NEW"
MIN_JAQ = 0.05

#docs = session.execute('SELECT doc_page_id  from documents')

docIDs =[]

def fingerprints(txt, n):
    output = []
    for i in range(len(txt)-n+1):
        minutiae = txt[i:i+n]
        for j in range(len(minutiae)):
            minutiae[j] = mmh3.hash(minutiae[j])
        output.append(tuple(minutiae))
    return output

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

def insertOrUpdateViral(p, p2):
    if checkIfVirExist(p.doc_page_id):
        session.execute("UPDATE virals SET similar_pages = similar_pages + ['{}'] WHERE viral_id = '{}'".format(p.doc_page_id, p2.doc_page_id))
    else:
        session.execute("INSERT INTO virals (viral_id,page_id, similar_pages, status, method_name, page_title)VALUES ('{}','{}',['{}'],'{}','{}','{}')".format(p.doc_page_id, p.doc_page_id, p2.doc_page_id,NEW_STATUS,METHOD_NAME, p.doc_title))
'''
for doc in docs:
    docIDs.append(doc.doc_page_id)
    #print(doc.doc_id)
'''

tag = session.execute("SELECT documents FROM tags WHERE tagname = '{}'".format("CIEKHISTZDARZ"))
for t in tag:
    for pagid in t.documents:
        docIDs.append(pagid)

docIDs = list(set(docIDs))
#docIDs =  random.sample(docIDs, 50)

lenDocIDs = len(docIDs)
print(lenDocIDs)
for i in range(0,lenDocIDs - 1):
    page1query = "SELECT doc_id , doc_page_id , page_text , doc_title from documents WHERE doc_page_id = '{}'".format(docIDs[i])
    page1 = session.execute(page1query)
    for p in page1:
        p1_text = p.page_text.replace('/','')
        p1_text = [word for word in p1_text.split(' ') if len(word) > 1]
        page1_4grams = fingerprints(p1_text, 6)#list(ngrams(p1_text, 4))
        #print(page1_4grams)
        #quit()
        page1_title = p.doc_title   
    for j in range( i + 1, lenDocIDs):
        page2query = "SELECT doc_id , doc_page_id , page_text, doc_title from documents WHERE doc_page_id = '{}'".format(docIDs[j])
        page2 = session.execute(page2query)
        for p2 in page2:
            page2_title = p2.doc_title
            if page1_title == page2_title:
                break
            try:
                p2_text = p2.page_text.replace('/','')
                p2_text = [word for word in p2_text.split(' ') if len(word) > 1]
                page2_4grams = fingerprints(p2_text,6)
            except AttributeError:
                print(p2.doc_page_id)
                continue
            jq = jaccard_distance(page1_4grams,page2_4grams)
            if jq > MIN_JAQ:
                print('insert {} {} {}'.format(jq,p.doc_page_id,p2.doc_page_id))
                insertOrUpdateViral(p, p2)