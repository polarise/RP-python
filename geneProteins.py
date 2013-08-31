#!/home/paulk/software/bin/python
from sys import argv,exit,stderr
from re import search

try:
	fn = argv[1]
except IndexError:
	print >> stderr,"""Script to get the association between genes and proteins
Usage: ./geneProteins.py <GTF>"""
	exit(1)

g2p = dict()

if search(r".gz$",fn):
	from gzip import open
	f = open(fn)
else:
	f = open(fn)
c = 0
for line in f:
	if c > 1000: break
	l = line.strip().split('\t')
	L = [i.strip().strip().strip(";").strip("\"") for i in l[8].strip().split(" ")]
	if 'protein_id' in L:
		g = L[1]
		w = L.index('protein_id')	# get the index of 'protein_id'
		p = L[w+1]	# the protein id is the next index
		if g not in g2p:
			g2p[g] = [p]
		else:
			if p not in g2p[g]: g2p[g] += [p]
	c += 0
f.close()

print "gene_id\tprotein_id"
for g in g2p:
	print "%s\t%s" % (g,",".join(g2p[g]))

