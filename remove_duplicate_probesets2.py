#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from random import choice

try:
	f = open(argv[1])
	g = open(argv[2],'w')
except IndexError:
	print >> stderr,"Usage: %s <report_in> <ps_list_out>" % argv[0]
	exit(1)

exon2ps = dict()
for row in f:
	ps_exon = row.strip().split('\t')
	if len(ps_exon) == 1: print >> g,ps_exon[0]; continue
	ps,exon = ps_exon
	if exon not in exon2ps:
		exon2ps[exon] = [ps]
	else:
		exon2ps[exon] += [ps]
f.close()

# now choose a probeset at random
for e in exon2ps:
	print >> g,choice(exon2ps[e])
g.close()
