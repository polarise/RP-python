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

f = open("../microarray/HuEx-1_0-st-v2.na31.hg19.probeset.csv")
ps2tx = dict()
c = 0
count = 0
for row in f:
	if c >= 100: break
	if row[0] == '#': continue
	l = row.strip().split(',')
	if l[0].strip('"')[0] == 'p': continue
	txs = [t.strip(' ').split("//")[0].strip(' ') for t in l[10].strip('"').split("///")]
	enstxs = [tx for tx in txs if tx[:4] == 'ENST']
	if enstxs != []:
		ps2tx[l[0].strip('"')] = enstxs
		count += 1
	c += 0
f.close()

# probeset to gene
ps2g = dict()
for p in ps2tx:
	g = None
	i = 0
	while g is None and i < len(ps2tx[p]):
		try:
			g = tx2g[ps2tx[p][i]]
		except KeyError:
			g = None
		i += 1
	ps2g[int(p)] = g

f = open("../resources/ps_to_gene.hg19.Ens63.pic",'w')
dump(ps2g,f,HIGHEST_PROTOCOL)
f.close()

