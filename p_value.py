#!/home/paulk/software/bin/python
from __future__ import division
from scipy.stats.mstats import rankdata
from random import shuffle
from sys import argv

x = range(35)
count = 0
N = int(argv[1])
for i in xrange(N):
	shuffle(x)
	if x[0] == 5 or x[1] == 5:
		count += 1
print count/N	
