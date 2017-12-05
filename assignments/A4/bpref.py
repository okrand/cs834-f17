from galago import *

def getsub(rel, retr):
    sub = []
    count = 0
    for document in retr:
        if document not in rel:
            count += 1
        if count > len(rel):
            break
        sub.append(document)
    return sub

values = []
for qnum in args.qnum:
    results = process(qnum)
    retr, rel = results[2], results[3]
    if not retr:
        print 'no results for query {}'.format(qnum)
        continue
    sub = getsub(rel, retr)
    b1 = bpref1(rel, sub)
    b2 = bpref2(rel, sub)
    print 'Query: {}'.format(qnum)
    print 'R: {}'.format(len(rel))
    print 'BPREF1: {}'.format(b1)
    print 'BPREF2: {}'.format(b2)
    values.append((qnum, len(rel), b1, b2))