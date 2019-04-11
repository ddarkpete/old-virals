import os
import re
import time
import binascii
import hashlib
import numpy as np

from random import randint
from bisect import bisect_right
from heapq import heappop, heappush
from cassandra.cluster import Cluster
from nltk import ngrams
import random

cluster = Cluster() 
session = cluster.connect('oldviralskeyspace')
session.default_timeout = 6000

METHOD_NAME = "SHINGLING"
NEW_STATUS = "NEW"
MIN_JAQ = 0.06

docIDs =[]
docs = session.execute("SELECT doc_page_id from documents where doc_id = 287988 ALLOW FILTERING")# , page_text from documents')
docs2 = session.execute("SELECT doc_page_id from documents where doc_id = 64428 ALLOW FILTERING")

for doc in docs:
    docIDs.append(doc.doc_page_id)
for doc2 in docs2:
    docIDs.append(doc2.doc_page_id)


#random.shuffle(docIDs)

def strToIntHash(text):
    return np.int32(int(hashlib.md5(text.encode('utf-8')).hexdigest()[:8], 16))

def getTriangleIndex(i, j):
    if i == j:
        print("No triangle matrix where indexes i == j")
    
    if j < i:
        temp = i
        i = j
        j = temp
    
    k = int( i * (numDocs - (i + 1)) / 2.0 + j - i) - 1
    return k
    

def pickRandomCoefs(k):
    randList = []
    while k > 0:
        randIndex = randint(0, maxShingleId)
        while randIndex in randList:
            randIndex = randint(0, maxShingleId)
        randList.append(randIndex)
        k -= 1
    return randList

def checkIfVirExist(viralID):
    rows = session.execute("SELECT * FROM virals WHERE viral_id = '{}'".format(viralID))
    if not rows:
        return False
    else:
        return True

def insertOrUpdateViral(p, p2):
    if checkIfVirExist(p):
        session.execute("UPDATE virals SET similar_pages = similar_pages + ['{}'] WHERE viral_id = '{}'".format(p2 ,p))
    else:
        session.execute("INSERT INTO virals (viral_id,page_id, similar_pages, status, method_name)VALUES ('{}','{}',['{}'],'{}','{}')".format(p, p, p2,NEW_STATUS,METHOD_NAME))



hashNum = 10
fileName = "1934_preprocesed.tsv"

print("Shingling in progress...")

currShID = 0
docsShingles = {}
docsIDs = []
allShingles = 0
numDocs = 0

lenDocIDs = len(docIDs)
print(lenDocIDs)
for i in range(0,lenDocIDs - 1):
    page1query = "SELECT doc_id , doc_page_id , page_text , doc_title from documents WHERE doc_page_id = '{}'".format(docIDs[i])
    page1 = session.execute(page1query)
    text_page1 = ""
    id_page1 = ""
    title_page1 = ""
    for p  in page1:
        text_page1 = p.page_text
        id_page1 = p.doc_page_id
        title_page1 = p.doc_title
    words_page1 = text_page1.split(' ')
    shinglesInPage1 = set()
    for ind in range(0, len(words_page1) - 2):
        shingle = "{} {} {}".format(words_page1[ind], words_page1[ind + 1], words_page1[ind + 2])
        shingle = strToIntHash(shingle)
        shinglesInPage1.add(shingle)
    for j in range( i + 1, lenDocIDs):
        page2query = "SELECT doc_id , doc_page_id , page_text , doc_title from documents WHERE doc_page_id = '{}'".format(docIDs[j])
        page2 = session.execute(page2query)
        #numDocs += 1
        #currDocID = doc.doc_page_id
        #docsIDs.append(currDocID)
        text_page2 = ""
        id_page2 = ""
        title_page2 = ""
        for p2 in page2:
            text_page2 = p2.page_text
            id_page2 = p2.doc_page_id
            title_page2 = p2.doc_title

        if title_page1 == title_page2:
            continue

        words_page2 = text_page2.split(' ')
        shinglesInPage2 = set()
        for ind in range(0, len(words_page2) - 2):
            shingle = "{} {} {}".format(words_page2[ind], words_page2[ind + 1], words_page2[ind + 2])
            shingle = strToIntHash(shingle)
            shinglesInPage2.add(shingle)
    
        #docsShingles[currDocID] = shinglesInDoc
        #allShingles = allShingles + (len(words) - 2)
        '''
        with open(fileName, 'r') as file:
            for line in file:
                numDocs += 1
                line  = line.split('\t')
                currDocID = line[0]
                docsIDs.append(currDocID)
                words = line[4].split(' ')
                shinglesInDoc = set()

                for ind in range(0, len(words) - 2):
                    shingle = "{} {} {}".format(words[ind], words[ind + 1], words[ind + 2])
                    shingle = strToIntHash(shingle)
                    shinglesInDoc.add(shingle)
                
                docsShingles[currDocID] = shinglesInDoc
                allShingles = allShingles + (len(words) - 2)
        '''
        #print("Average shingle per doc: {}".format(allShingles/numDocs))

        #TRIANGLE MATRICE

        #elemCount = int(numDocs * (numDocs - 1) / 2 )

        #estJSim = [ 0 for x in range(elemCount)]
        #estJSim = JSim

        maxShingleId = 2 * 32 - 1
        nextPrime = 4294967311

        coeffA = pickRandomCoefs(hashNum)
        coeffB = pickRandomCoefs(hashNum)

        signature_pag1 = []
        signature_pag2 = []

        for i in range(0, hashNum):
            minHashCode = nextPrime + 1
            for shingleID in shinglesInPage1:
                hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
                if hashCode < minHashCode:
                    minHashCode = hashCode
            signature_pag1.append(minHashCode)
            
            minHashCode = nextPrime + 1
            for shingleID in shinglesInPage2:
                hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
                if hashCode < minHashCode:
                    minHashCode = hashCode
            signature_pag2.append(minHashCode)
   
        count = 0
        for k in range(0, hashNum):
            count += (signature_pag1[k] == signature_pag2[k])
        
        estJ = (count / hashNum)

        threshold = 0.5
        underThrsh = 0
        #if(estJ > 0.0):
        #    print(estJ)
        if estJ > threshold:

            J = (len(shinglesInPage1.intersection(shinglesInPage2)) / len(shinglesInPage1.union(shinglesInPage2)))
            if J > MIN_JAQ:
                print('insert')
                insertOrUpdateViral(id_page1, id_page2)
        else:
            underThrsh += 1

 

        















        
        

