#!/usr/bin/env python

import cPickle
import math

wordlist = {}
try:
    wordlist = cPickle.load(open('wordlist.p', 'rb'))
except IOError:
    wordlist = {line.split()[0].lower(): line.split()[1:] for line in open('invertindex.dat').readlines()}
    cPickle.dump(wordlist, open('wordlist.p', 'wb'))
    wordlist = cPickle.load(open('wordlist.p', 'rb'))
N = float(sum(len(x) for x in wordlist.values()))

class Result(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        sett1 = set(wordlist[t1])
        Nt1 = float(len(sett1))
        sett2 = set(wordlist[t2])
        Nt2 = float(len(sett2))
        sett = sett1.intersection(sett2)
        Nt = float(len(sett))
        self.mim = Nt / (Nt1 * Nt2)
        try:
            self.emim = Nt * math.log(N * Nt / (Nt1 * Nt2))
        except Exception as e:
            self.emim = 0.0
        self.dice = Nt / (Nt1 + Nt2)
        self.x2 = (Nt - (1/N) * Nt1 * Nt2)**2 / (Nt1 * Nt2)
    def getmim(self):
        return self.mim

    def getemim(self):
        return self.emim

    def getx2(self):
        return self.x2

    def getdice(self):
        return self.dice

    def __repr__(self):
        return '({},{})\n  MIM  {}\n  EMIM {}\n  X2   {}\n  Dice {}'.format(
            self.a, self.b, self.mim, self.emim, self.x2, self.dice)

def gethighest(results, w, keyfunc):
    return sorted(results[w], key=keyfunc, reverse=True)[:10]

def printresults(results, mywords):
    for w in mywords:
        mim  = [res.t2 for res in gethighest(results, w, Result.getmim)]
        emim = [res.t2 for res in gethighest(results, w, Result.getemim)]
        x2   = [res.t2 for res in gethighest(results, w, Result.getx2)]
        dice = [res.t2 for res in gethighest(results, w, Result.getdice)]
        print('{}\n  MIM  {}\n  EMIM {}\n  X2   {}\n  Dice {}'.format(
            w, mim, emim, x2, dice))
        #print(w + ": MIM=" + mim + " EMIM =" + emim + " X2=" + x2 + " Dice=" + dice)

mywords = ['umbrella','messenger','cramps','equestrian','sea','everlasting','association','vehicle','python','motorcycle']
results = {w: [Result(w, word) for word in wordlist.keys() if w != word] for w in mywords}
printresults(results, mywords)
