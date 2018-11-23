from flask import Flask, render_template, request ,redirect, url_for
from cassandra.cluster import Cluster
import json

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')

app = Flask(__name__)

def str2bool(v):
  return v.lower() == "true"

@app.route('/')
def mainPage():
    virals = session.execute('SELECT * from simpages')
    return render_template('mainPage.html', virals = virals)

@app.route('/text/<id>')
def text(id):
    rows = session.execute('SELECT * from oldvirals WHERE ov_id = {}'.format(id))
    ovText = ""
    for query_row in rows:
        ovText = query_row.ov_text
    return render_template('OneText.html', text = ovText)

@app.route('/viral/<vir_id>',methods=['GET', 'POST'])
def viralPage(vir_id):
    if request.method == 'POST':
        simVirals = request.get_data().decode("utf-8")
        pairs = simVirals.split('&')
        simVirals = {}
        for pair in pairs:
            keyval = pair.split('=')
            simVirals[keyval[0]] = str2bool(keyval[1])
        print(simVirals)
        '''
        simVirals = request.json()
        for k, v in simVirals:
            print("{} {}".format(k,v))
        '''
        return "OK"
    else:
        viral = session.execute("SELECT * FROM simpages WHERE id = '{}'".format(vir_id))
        #query = "SELECT * FROM documents WHERE doc_page_id IN ('"
        idsInString = ""
        for v in viral:
            idsInString = str(v.sim)[1:-1]
        rows = session.execute("SELECT * FROM documents WHERE doc_page_id IN ({})".format(idsInString))
        return render_template('viralPage.html', articles = rows)




if __name__ == '__main__':
   app.run(debug = True)