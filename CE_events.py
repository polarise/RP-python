#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import load

exon_lengths = load(open(argv[1]))

f = open(argv[2])
for row in f:
	a,b = row.strip().split('\t')
	coords = exon_lengths[a]
	c,d_e,g = coords.split(':')
	d,e = d_e.split('-')
	print "_".join([a.split(':')[0],d,e])
f.close()

