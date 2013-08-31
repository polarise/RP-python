#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

"""
Simple script to obtain gene-introns from gene-exons.
Paul K. Korir
NUIG
2012-02-16
"""

class Gene:
	def __init__(self,name,chrom,sd):
		self.name = name
		self.chrom = chrom
		self.sd = sd
		self.exons = dict()
		self.introns = dict()

	def add_exon(self,exno,st,sp):
		self.exons[int(exno)] = (int(st),int(sp))

	def create_introns(self):
		if len(self.exons.keys()) > 1:
			for e in xrange(1,len(self.exons.keys())):
				self.introns[e] = (self.exons[e][1]+1,self.exons[e+1][0]-1)

	def print_introns(self):
		if len(self.introns.keys()) > 0:
			for i in self.introns:
				print "\t".join([self.name,str(i),self.chrom,str(self.introns[i][0]),str(self.introns[i][1]),self.sd])

	def count_introns(self):
		return len(self.introns.keys())
			
try:
	fn = argv[1]
except IndexError:
	print >> stderr,"""Script to obtain gene-intron co-ordinates from gene-exons.
Usage:./<s.py> <gene_exon.gene>"""
	exit(1)

genes = dict()
f = open(fn)
for line in f:
	l = line.strip().split('\t')
	if l[0] not in genes:
		genes[l[0]] = Gene(l[0],l[2],l[5])
		genes[l[0]].add_exon(l[1],l[3],l[4])
	else:
		genes[l[0]].add_exon(l[1],l[3],l[4])
f.close()

without_introns = 0
for g in genes:
	genes[g].create_introns()
	if genes[g].count_introns() == 0: without_introns += 1
	genes[g].print_introns()

print >> stderr,"Genes without introns are %s."%without_introns
	
