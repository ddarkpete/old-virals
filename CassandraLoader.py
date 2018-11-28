import sys
from cassandra.cluster import Cluster

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

print(" doc_page_id\tdoc_id\tdoc_title\tpage_no\tpage_text")

for line in sys.stdin:
    pageNo = 1
    data = line.split('\t')
    splitedLine = data[4][:-1].split('//  //  \\\\')
    for spl in splitedLine:
        docIDPageNo = "{}_{}".format(data[0], pageNo)
        print("{}\t{}\t{}\t{}\t{}".format(docIDPageNo,data[0],data[1],pageNo,spl))
        pageNo+=1
        '''
        session.execute(
        """
        INSERT INTO documents (doc_page_id)
        VALUES (?)
        """,
        (docIDPageNo)
        )
        '''
        

# TODO
# Tabela documet taka jak oldviral ale dodatkowo nr strony (id + nr strony w kluczu glownym)
# insertowanie z tego skryptu do tej tabeli
