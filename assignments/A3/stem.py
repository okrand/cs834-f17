#!/usr/bin/env python

from nltk.stem.snowball import SnowballStemmer
import collections
from itertools import combinations
import cPickle

class Result(object):
    def __init__(self,t1,t2):
        self.t1 = t1
        self.t2 = t2

    def getdice(self):
        sett1 = set(stems2[self.t1])
        Nt1 = float(len(sett1))
        sett2 = set(stems2[self.t2])
        Nt2 = float(len(sett2))
        sett = sett1.intersection(sett2)
        Nt = float(len(sett))
        return Nt / (Nt1 + Nt2)

def convert(filtered):
    converted = {}
    for stem, fres in filtered.items():
        if len(fres) > 0:
            res = set()
            for result in fres:
                res.add(result.t1)
                res.add(result.t2)
            converted[stem] = res
    return converted

print("Started")
wordlist = {}
try:
    wordlist = cPickle.load(open('wordlist.p', 'rb'))
except IOError:
    wordlist = {line.split()[0].lower(): line.split()[1:] for line in open('invertindex.dat').readlines()}
    cPickle.dump(wordlist, open('wordlist.p', 'wb'))
    wordlist = cPickle.load(open('wordlist.p', 'rb'))

wordlist = sorted(wordlist.keys())[15000:16000]

snowball = SnowballStemmer('english')
stems = {w: snowball.stem(unicode(w.lower(), 'utf-8')) for w in wordlist}
dupcount = collections.Counter(stems.values()) #duplicate counter
stems2 = {} 
for key, val in stems.items():
	if dupcount[val] > 1:
		stems2[key] = val
classes = {}
print("Before for loop")
for pair in combinations(stems2.items(), 2):
    k1 = pair[0][0]
    k2 = pair[1][0]
    v1 = pair[0][1]
    v2 = pair[1][1]
    if v1 == v2:
        if not classes.has_key(v1):
            classes[v1] = set()
        classes[v1].add(k1)
        classes[v1].add(k2)
print("Classes ready")

results = {}
for stem, term in classes.items():
    for pair in combinations(term, 2):
        t1 = pair[0]
        t2 = pair[1]
        if not results.has_key(stem):
            results[stem] = set()
        results[stem].add(Result(t1, t2))
print("Results ready")

filtered1 = {stem: [r for r in resultset if r.getdice() > 0.1] for stem, resultset in results.items()}
c1 = convert(filtered1)
print ("C1 Results")
for stemclass in c1.items():
    try:
        print(stemclass[0] + ": " + ', '.join(stemclass[1]) + "\\\\")
    except UnicodeDecodeError:
        pass