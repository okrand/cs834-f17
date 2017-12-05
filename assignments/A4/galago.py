import sys, argparse, requests, re, xmltodict
import numpy as np
from math import log
from bs4 import BeautifulSoup

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=52108, help='galago server port')
    parser.add_argument('-q', '--qnum', nargs='+', type=int, default=[9, 10], help='query number')
    parser.add_argument('-n', type=int, default=10, help='number of retrieval pages')
    return parser.parse_args()

args = parseargs()

def buildrel():
    #read CACM relevance judgments for each query
    rel = {}
    for line in open('cacm.rel').readlines():
        q, _, doc, _ = line.split()
        if q not in rel:
            rel[q] = []
        rel[q].append(int(doc.split('-')[1]))
    return rel

def buildqueries():
    #read CACM queries into a map
    with open('cacm.query.xml') as fd:
        return xmltodict.parse(fd.read())

REL = buildrel()
QUERIES = buildqueries()
RE = re.compile('/Users/Krando67/Desktop/CS734 - Info Retrieval/galago-3.12/../cs834-f17/assignments/A4/cacm/CACM-(\d+).html')
URL = 'http://0.0.0.0:{0}/search'
Q1 = 'what articles exist which deal with tss time sharing system an operating system for ibm computers'
PDICT = {'q': Q1, 'start': 0, 'n': args.n}

def query(qstr, port=args.port):
    PDICT['q'] = qstr
    PDICT['n'] = args.n
    res = requests.get(URL.format(port), params=PDICT)
    if not res.ok:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    #print [soup.select("#result a")[0].text]
    return [int(RE.match(href.text).groups()[0]) for href in soup.select("#result a")]

def precision(rel, retr):
    relset = set(rel)
    retrset = set(retr)
    return float(len(relset.intersection(retrset))) / len(retrset)

def recall(rel, retr): 
    relset = set(rel)
    retrset = set(retr)
    return float(len(relset.intersection(retrset))) / len(relset)

def getrel(rel, retr, i):
    #relevancy score
    return 1 if retr[i] in rel else 0

def DCG(rel, retr, p):
    #DCG at p 
    sum = 0
    for i in range(2, p+1):
        sum += float(getrel(rel, retr, i-1)) / log(i, 2)
    return getrel(rel, retr, 0) + sum

def IDCG(p):
    #IDCG at p
    sum = 0
    for i in range(2, p+1):
        sum += 1 / log(i, 2)
    return 1 + sum

def NDCG(rel, retr, p):
    #NDCG at p 
    dcg = DCG(rel, retr, p)
    idcg = IDCG(p)
    return dcg / idcg

def reciprank(rel, retr):
    #reciprocal rank
    for i in range(1, len(retr)+1):
        if retr[i-1] in rel:
            return 1.0 / i
    return 0.0

def run(rel, retr, func):
    #recall or precision at all ranks
    rr = []
    for i in range(1, len(retr)+1):
        rr.append(func(rel, retr[:i]))
    return rr

def avg(rel, retr, func):
    #average recall or precision
    prun = run(rel, retr, func)
    res = []
    for i in range(len(retr)):
        if retr[i] in rel:
            res.append(prun[i])
    if len(res) == 0:
        return 0.0
    return float(sum(res))/len(res)

def ipr(rrun, prun):
    #interpolated precision at std recall given recall and precision runs
    res = []
    for i in np.arange(0, 1.1, .1):
        for j in range(len(rrun)):
            if rrun[j] > i:
                idx = j
                break
        res.append(max(prun[idx:]))
    return np.arange(0, 1.1, 0.1), res

def rprecision(rel, prun):
    return prun[len(rel)]

def getquery(qnum):
    return QUERIES['parameters']['query'][qnum-1]['text']

def process(qnum):
    qstr = getquery(qnum)
    retr = query(qstr)
    if str(qnum) not in REL:
        return [None]*12
    rel = REL[str(qnum)]
    prun = run(rel, retr, precision)
    rrun = run(rel, retr, recall)
    prec = precision(rel, retr)
    rec = recall(rel, retr)
    avgprec = avg(rel, retr, precision)
    ndcg5 = NDCG(rel, retr, 5)
    ndcg10 = NDCG(rel, retr, 10)
    recip = reciprank(rel, retr)
    return qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip

def printresults(qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip):
    if not qnum:
        return
    print 'query {0}'.format(qnum)
    print 'query: {0}'.format(qstr)
    if args.n == 10:
        print 'relevant: {0}'.format(rel)
        print 'retrieved: {0}'.format(retr)
        print 'p-run: {0}'.format(prun)
        print 'r-run: {0}'.format(rrun)
    else:
        print 'relevant: {}'.format(len(rel))
        print 'retrieved: {}'.format(len(retr))
    print 'Precision: {0}'.format(prec)
    print 'Recall: {0}'.format(rec)
    print 'Precision @10: {0}'.format(prun[9])
    print 'NDCG @5: {0}'.format(ndcg5)
    print 'NDCG @10: {0}'.format(ndcg10)
    print 'Average Precision: {0}'.format(avgprec)
    print 'Reciprocal Rank: {0}'.format(recip)

def writetodat(rrun, prun, fname):
    #print a data table for Rscript consumption
    with open(fname, 'w') as fd:
        zipped = zip(rrun, prun)
        for z in zipped:
            fd.write('{0}\t{1}\n'.format(z[0], z[1]))

def bpref1(rel, retr):
    #BPREF first equation
    relset = set(rel)
    retrset = set(retr)
    R = float(len(rel))
    res = 0
    for dr in rel:
        if dr not in retr:
            Ndr =  R
        else:
            Ndr = float(len([doc for doc in retr[:retr.index(dr)] if doc not in rel]))
        res += (1.0 - Ndr/R)
    return 1.0/R * res 

def bpref2(rel, retr):
    #BPREF second equation
    p = 0.0
    q = 0.0
    for dr in rel:
        if dr not in retr:
            p += 0
            q += len(retr)
        else:
            p += float(len([doc for doc in retr[retr.index(dr):] if doc not in rel]))
            q += float(len([doc for doc in retr[:retr.index(dr)] if doc not in rel]))
    return p / (p + q)

if __name__ == '__main__':
    for qnum in args.qnum:
        printresults(*process(qnum))