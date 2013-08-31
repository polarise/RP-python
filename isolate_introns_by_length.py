#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from os.path import basename

try:
	fn = argv[1]
	kind = argv[2]
except IndexError:
	print >> stderr,"./%s <gene_file> [first|internal|last]" % basename(argv[0])
	exit(1)

try:
	assert kind in ['first','internal','last']
except:
	raise ValueError("Use one of either 'first','internal', or 'last' only.")
	exit(1)

f = open(fn)
introns = dict()
for row in f:
	l = row.strip().split('\t')
	if l[0] not in introns:
		introns[l[0]] = dict()
	introns[l[0]][int(l[1])] = int(l[-1])
f.close()

for i in introns:
	last_intron = len(introns[i].keys())
	if kind == 'first':
		print i,introns[i][1]
	elif kind == 'internal':
		for j in xrange(2,last_intron):
			print i,introns[i][j]
	elif kind == 'last':
		print i,introns[i][last_intron]
