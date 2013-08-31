#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr,stdout
from scipy import *
from scipy.stats.mstats import rankdata

ranks = dict()
data = dict()
f = open(argv[1])
unwanted = ['I','S','\t']
for row in f:
	if row[0] in unwanted: continue
	l = row.strip().split('\t')
	ranks[l[1]] = rankdata(map(float,l[2:]))
f.close()


c = 0
for r in ranks:
	if c > 20: break
	print "\t".join([r] + map(str,list(ranks[r])))
	c += 0

	


	
