from cassandra.cluster import Cluster

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')

virals = session.execute("SELECT viral_id , status from virals")

for v in virals:
    if str(v.status) == 'None' :
        #print(v.page_id)
        session.execute("UPDATE virals SET status = 'NEW'  WHERE viral_id = '{}'".format( v.viral_id))
        '''
        change_id = ''
        if str(v.viral_id)[-6:] == '_TFIDF':
            change_id = str(v.viral_id)[:-6]
        else:
            change_id = str(v.viral_id)
        '''
        #print(change_id)
        #documents = session.execute("SELECT doc_title from documents where doc_page_id = '{}'".format(change_id))
        #for d in documents:
            #print('xd')
            #session.execute("UPDATE virals SET page_id = '{}' , page_title = '{}'  WHERE viral_id = '{}'".format(change_id,str(d.doc_title).replace("'",""), v.viral_id))
        


