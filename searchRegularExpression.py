from cassandra.cluster import Cluster
import re
import sys


cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

 
TAGNAME = 'DONOSI'#sys.argv[1]

pattern = 'don[oi]{0,1}[se]{0,1}[iząaśs][aącć]{0,1}'#sys.argv[2]
#search_expression = re.compile(pattern)

tag = session.execute("SELECT tagname from tags WHERE tagname = '{}'".format(TAGNAME))

if not tag:
    session.execute("INSERT into tags (tagname) VALUES ('{}')".format(TAGNAME))

docs = session.execute('SELECT doc_page_id from documents')



for doc in docs:
    texts = session.execute("SELECT page_text FROM documents WHERE  doc_page_id = '{}'".format(doc.doc_page_id))
    for text in texts:
        if re.search(pattern,text.page_text,re.IGNORECASE):
            session.execute("UPDATE tags SET documents = documents + ['{}'] WHERE tagname = '{}'".format(doc.doc_page_id, TAGNAME))




