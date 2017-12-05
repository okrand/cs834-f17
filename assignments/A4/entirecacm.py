from galago import *

netavg = []
iprl = []
ndcg5lst = []
ndcg10lst = []
prunlst = []
for i in range(1, 64):
    qnum, qstr, retr, rel, prun, rrun, prec, rec, ndcg5, ndcg10, avgprec, recip = process(i)
    if avgprec:
        netavg.append(avgprec)
        prunlst.append(prun[9])
        irrun, iprun = ipr(rrun, prun)
        iprl.append((iprun, qnum))
        ndcg5lst.append(ndcg5)
        ndcg10lst.append(ndcg10)

# MAP
cacmmap = float(sum(netavg)) / len(netavg)
print 'MAP: {0}'.format(cacmmap)

# Recall-Precision
netavgrpg = [float(sum(col))/len(col) for col in zip(*[col[0] for col in iprl])]
writetodat(np.arange(0, 1.1, .1), netavgrpg, 'avgall.dat')

# NDCG @ 5 and 10
avgndcg5 = float(sum(ndcg5lst))/len(ndcg5lst)
avgndcg10 = float(sum(ndcg10lst))/len(ndcg10lst)
print 'NDCG @5 : {0}'.format(avgndcg5)
print 'NDCG @10: {0}'.format(avgndcg10)

# precision at 10
avgprec10 = float(sum(prunlst))/len(prunlst)
print 'Precision @10: {0}'.format(avgprec10)