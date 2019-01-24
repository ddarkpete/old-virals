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
MIN_JAQ = 0.089

docs = session.execute('SELECT doc_page_id , page_text from documents')

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

def insertOrUpdateViral(pag1_id, pag2_id):
    if checkIfVirExist(p.doc_page_id):
        session.execute("UPDATE virals SET similar_pages = similar_pages + ['{}'] WHERE viral_id = '{}'".format(pag2_id, pag1_id))
    else:
        session.execute("INSERT INTO virals (viral_id,page_id, similar_pages, status, method_name)VALUES ('{}','{}',['{}'],'{}','{}')".format(p.doc_page_id, p.doc_page_id, p2.doc_page_id,NEW_STATUS,METHOD_NAME))



hashNum = 10
fileName = "1934_preprocesed.tsv"

print("Shingling in progress...")

currShID = 0
docsShingles = {}
docsIDs = []
allShingles = 0
numDocs = 0

for doc in docs:
    numDocs += 1
    currDocID = doc.doc_page_id
    docsIDs.append(currDocID)
    words = doc.page_text.split(' ')
    shinglesInDoc = set()
    for ind in range(0, len(words) - 2):
        shingle = "{} {} {}".format(words[ind], words[ind + 1], words[ind + 2])
        shingle = strToIntHash(shingle)
        shinglesInDoc.add(shingle)
    
    docsShingles[currDocID] = shinglesInDoc
    allShingles = allShingles + (len(words) - 2)
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
print("Average shingle per doc: {}".format(allShingles/numDocs))

#TRIANGLE MATRICE

elemCount = int(numDocs * (numDocs - 1) / 2 )

estJSim = [ 0 for x in range(elemCount)]
#estJSim = JSim

maxShingleId = 2 * 32 - 1
nextPrime = 4294967311

coeffA = pickRandomCoefs(hashNum)
coeffB = pickRandomCoefs(hashNum)

signatures = []

for docID in docsIDs:
    shingleSet = docsShingles[docID]
    signature = []
    for i in range(0, hashNum):
        minHashCode = nextPrime + 1
        for shingleID in shingleSet:
            hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
            if hashCode < minHashCode:
                minHashCode = hashCode
        signature.append(minHashCode)
    signatures.append(signature)

for i in range(0, numDocs):
    signature1 = signatures[i]
    for j in range( i + 1, numDocs ):
        signature2 = signatures[j]
        
        count = 0
        for k in range(0, hashNum):
            count += (signature1[k] == signature2[k])
        
        estJSim[getTriangleIndex(i, j)] = (count / hashNum)

threshold = 0.5
underThrsh = 0

for i in range(0, numDocs):
    for j in range( i + 1, numDocs):
        
        estJ =  estJSim[getTriangleIndex(i, j)]

        if estJ > threshold:

            s1 = docsShingles[docsIDs[i]]
            s2 = docsShingles[docsIDs[j]]
            J = (len(s1.intersection(s2)) / len(s1.union(s2)))
            if J > MIN_JAQ:
                print('insert')
                insertOrUpdateViral(docsIDs[i], docsIDs[j])
        else:
            underThrsh += 1

 

        















        
        

