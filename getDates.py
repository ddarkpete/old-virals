from cassandra.cluster import Cluster
import sys


cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

for line in sys.stdin:
    line = line.split('\t')
    line[4] = line[4].replace('\\','').replace('//','').replace('---0---','').replace('---','').replace('  0  ', '').replace(' . ', '')
    tempLine = line[4].lower()
    if not (len(line[2]) > 4 or len(line[3]) > 4): 
        #print(line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3])# + '\t' + line[4][:-1])
        docs = session.execute("SELECT doc_page_id from documents where doc_id = {} ALLOW FILTERING".format(line[0]))
        for d in docs:
            #print(d.doc_page_id)
            session.execute("UPDATE documents SET doc_date_start = '{}-01-01' WHERE doc_page_id = '{}'".format(line[2] ,d.doc_page_id))
            session.execute("UPDATE documents SET doc_date_stop = '{}-12-31' WHERE doc_page_id = '{}'".format(line[3] ,d.doc_page_id))

