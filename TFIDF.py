from cassandra.cluster import Cluster
from nltk import ngrams
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import math

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

tokenize = lambda doc: doc.lower().split(' ')
sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

METHOD_NAME = "TFIDF"
NEW_STATUS = "NEW"

docs = session.execute('SELECT doc_id from documents')

docIDs =[]

for doc in docs:
    docIDs.append(doc.doc_id)
    #print(doc.doc_id)

docIDs = list(set(docIDs))

lenDocIDs = len(docIDs)
print(lenDocIDs)
for i in range(0,lenDocIDs - 1):
    for j in range( i + 1, lenDocIDs):
        page1 = session.execute('SELECT doc_id , doc_page_id , page_text from documents WHERE doc_id = {} ALLOW FILTERING'.format(docIDs[i]))
        page2 = session.execute('SELECT doc_id , doc_page_id , page_text from documents WHERE doc_id = {} ALLOW FILTERING'.format(docIDs[j]))
        for p in page1:
            document_0 = p.page_text
            for p2 in page2:
                document_1 = p2.page_text
                all_documents = [document_0 ,document_1]
                tfidf = sklearn_tfidf.fit_transform(all_documents)
                tfidf_comparisons = []
                for count_0, doc_0 in enumerate(tfidf.toarray()):
                    for count_1, doc_1 in enumerate(tfidf.toarray()):
                        tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))

                for x in sorted(tfidf_comparisons, reverse = True):
                    print(x)




