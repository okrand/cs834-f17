#!/usr/bin/env python

import re
import sys
import cPickle
from collections import Counter

try:
    words = cPickle.load(open('big.p', 'rb'))
except IOError:
    wordmap = Counter(re.findall(r'\w+', open('big.txt').read().lower()))
    cPickle.dump(wordmap, open('big.p', 'wb'))
    words = cPickle.load(open('big.p', 'rb'))

N = sum(words.values())


def known(wordset):
    return set([word for word in wordset if word in words])


def prob(word): #all errors with the same edit distance have the same probability
    return float(words[word]) / float(N)


def edit1(w):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    deletes    = [w[:i]+w[i+1:]             for i in range(len(w))]
    transposes = [w[:i]+w[i+1]+w[i]+w[i+2:] for i in range(len(w)-1)]
    replaces   = [w[:i]+l+w[i+1:]           for i in range(len(w)) for l in letters]
    inserts    = [w[:i]+l+w[i:]             for i in range(len(w)+1) for l in letters]
    return set(deletes + transposes + replaces + inserts)


def edit2(word):
    e2 = [edit1(w) for w in edit1(word)]
    return [item for sublist in e2 for item in sublist]


def parse(word):
    return known([word]) or known(edit1(word)) or known(edit2(word)) or [word]


def correct(word):
    return max(parse(word), key=prob)


if __name__ == '__main__':
    print correct(sys.argv[1])