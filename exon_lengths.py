#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import load

exon_lengths = load(open(argv[1]))

f = open(argv[2])
for row in f:
	for e in row.strip().split(','):
		print e+"\t"+str(exon_lengths[e])
f.close()

