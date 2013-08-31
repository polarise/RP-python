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

ps2exon = dict()
exon2ps = dict()
for row in f:
	ps,exon = row.strip().split('\t')
	if exon not in exon2ps:
		exon2ps[exon] = [ps]
	else:
		exon2ps[exon] += [ps]
	if ps not in ps2exon:
		ps2exon[ps] = [exon]
	else:
		ps2exon[ps] += [exon]
f.close()

# generate a representative set of exons
exons = list()
for p in ps2exon:
	exons.append(choice(ps2exon[p]))
	
# now this set will be our representative source of exons
for e in exons:
	print >> g,choice(exon2ps[e])
g.close()
