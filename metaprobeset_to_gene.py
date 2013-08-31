#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import load,dump,HIGHEST_PROTOCOL

"""
# create the pickle from tx to gene
tx2g = dict()
f = open("../resources/gene_to_txs.hg19.Ens63")
for row in f:
	g,txs,no = row.strip().split('\t')
	for tx in txs.split(','):
		tx2g[tx] = g
f.close()

f = open("../resources/tx_to_gene.hg19.Ens63.pic",'w')
dump(tx2g,f,HIGHEST_PROTOCOL)
f.close()
"""

f = open("../resources/tx_to_gene.hg19.Ens63.pic")
tx2g = load(f)
f.close()

f = open("../microarray/HuEx-1_0-st-v2.na31.hg19.transcript.csv")
mps2tx = dict()
c = 0
for row in f:
	if c >= 1000: break
	if row[0] == '#': continue
	l = row.strip().split('","')
	if l[0].strip('"')[0] == 'p': continue
	txs1 = [t.strip(' ').split("//")[0].strip(' ') for t in l[7].strip('"').split("///")]
	txs2 = [t.strip(' ').split("//")[0].strip(' ') for t in l[8].strip('"').split("///")]
	txs = set(txs1 + txs2)
	enstxs = [tx for tx in txs if tx[:4] == 'ENST']
	if enstxs != []:
		mps2tx[l[0].strip('"')] = enstxs
	c += 0
f.close()

print >> stderr,"No. of mps to genes: %s"%len(mps2tx.keys())

# probeset to gene
mps2g = dict()
for p in mps2tx:
	g = None
	i = 0
	while g is None and i < len(mps2tx[p]):
		try:
			g = tx2g[mps2tx[p][i]]
		except KeyError:
			g = None
		i += 1
	mps2g[int(p)] = g

f = open("../resources/mps_to_gene.hg19.Ens63.pic",'w')
dump(mps2g,f,HIGHEST_PROTOCOL)
f.close()

