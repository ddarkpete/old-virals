from flask import Flask, render_template, request ,redirect, url_for
from cassandra.cluster import Cluster
import json

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')

app = Flask(__name__)

def str2bool(v):
  return v.lower() == "true"

@app.route('/')
def redirToAll():
    return redirect('/all')

@app.route('/<method>')
def mainPage(method):
    if method == 'all' or method == '':
        virals = session.execute("SELECT viral_id , status , snippet from virals")
        met = 1
    elif method == 'ngrams':
        virals = session.execute("SELECT viral_id , status , snippet from virals where method_name = '4GRAMS' ALLOW FILTERING")
        met = 2   
    elif method == 'shingling':
        virals = session.execute("SELECT viral_id , status , snippet from virals where method_name = 'SHINGLING' ALLOW FILTERING")
        met = 3
    elif method == 'tfidf':
        virals = session.execute("SELECT viral_id , status , snippet from virals where method_name = 'TFIDF' ALLOW FILTERING")
        met = 4
    else:
        return redirect('/all')
    return render_template('mainPage.html', virals = virals, met = met)

@app.route('/text/<id>')
def text(id):
    rows = session.execute("SELECT page_text , doc_title , doc_date_start , doc_date_stop from documents WHERE doc_page_id = '{}'".format(id))
    page_text = ""
    doc_title = ""
    doc_date_start = ""
    doc_date_stop = ""
    for query_row in rows:
        page_text = query_row.page_text
        doc_title = query_row.doc_title
        doc_date_start = query_row.doc_date_start
        doc_date_stop = query_row.doc_date_stop
    return render_template('OneText.html', text = page_text, title = doc_title , doc_date_start = doc_date_start , doc_date_stop = doc_date_stop)

@app.route('/viral/<vir_id>',methods=['GET', 'POST'])
def viralPage(vir_id):
    if request.method == 'POST':
        simVirals = request.get_data().decode("utf-8")
        pairs = simVirals.split('&')
        simVirals = {}
        for pair in pairs:
            keyval = pair.split('=')
            simVirals[keyval[0]] = keyval[1]
        for s in simVirals:
            if s[-4:] == 'INT':
                cql = "UPDATE documents SET isinterestingsimilar = isinterestingsimilar + {{'{}' : {}}} WHERE doc_page_id = '{}'".format(vir_id, str(simVirals[s]).lower(), s[:-4])
            else:
                cql = "UPDATE documents SET issimilar = issimilar + {{'{}' : {}}} WHERE doc_page_id = '{}'".format(vir_id, str(simVirals[s]).lower(), s)
            session.execute(cql)

        session.execute("UPDATE virals SET status = 'REVIEWED' WHERE viral_id = '{}'".format(vir_id))
        return "200"
    else:
        viral = session.execute("SELECT similar_pages , snippet , page_title , status FROM virals WHERE viral_id = '{}'".format(vir_id))
        #query = "SELECT * FROM documents WHERE doc_page_id IN ('"
        viralSnippet=""
        idsInString = ""
        virTitle = ""
        for v in viral:
            idsInString = str(v.similar_pages)[1:-1]
            viralSnippet = v.snippet
            virTitle =  v.page_title
            #viral
            if v.status == 'NEW':
                session.execute("UPDATE virals SET status = 'VIEWED' WHERE viral_id = '{}'".format(vir_id))
        rows = session.execute("SELECT doc_page_id , doc_title , snippets , issimilar , doc_date_start, doc_date_stop FROM documents WHERE doc_page_id IN ({})".format(idsInString))
        print(vir_id)
        return render_template('viralPage.html', articles = rows, vir_id = vir_id, viralSnippet=viralSnippet, virTitle=virTitle)




if __name__ == '__main__':
   app.run(debug = True)