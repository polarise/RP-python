#!/home/paulk/software/bin/python
from __future__ import division
import sys,os,time,gzip
import cPickle,pysam,random,math
import pylab
from multiprocessing import Process,Queue
import numpy

"""
Synopsis
Given a GTF file of genes, txs and exons prints to stdout the union of genes'
exons over all txs.
"""

def usage():
	print >> sys.stderr,"""Script to determine the union of exons over txs
Usage: ./gene2exons.py <GTF> <exon_file>
Results are printed to std out.
Output (tab-delimited): gene_id,chrom,exon_no,start,end"""
	
class Interval:
	def __init__(self,st,sp):
		self.l = st
		self.r = sp
	
	def union(self,I):
		if self.l <= I.r: L = self.l
		else: L = I.l
		if self.r >= I.r: R = self.r
		else: R = I.r
		return Interval(L,R)

try:
	gtf_file = sys.argv[1]
except IndexError:
	print >> sys.stderr,"Error: Enter GTF file"
	usage()
	sys.exit(1)
try:
	exonsfile = sys.argv[2]
except IndexError:
	print >> sys.stderr,"Error: Enter exons file"
	usage()
	sys.exit(1)

# tx2gene
gene2tx = dict()
f = open(gtf_file,'r')
for l in f:
	line = l.strip().split('\t')
	_data = line[8].split(';')
	data = [each.strip() for each in _data]
	tx = data[1][15:-1]
	gene = data[0][9:-1]
	if gene not in gene2tx:
		gene2tx[gene] = [tx]
	else:
		gene2tx[gene] += [tx]
f.close()
print >> sys.stderr,"[%s] Read GTF." % (time.ctime(time.time()))

# tx2exons
tx2exons = dict()
f = open(exonsfile,'r')
for line in f:
	l = line.strip().split('\t')
	tx_id = l[0]
	st = int(l[3])
	sp = int(l[4])
	no = int(l[1])
	chrom = l[2]
	if tx_id not in tx2exons:
		tx2exons[tx_id] = dict()
	else:
		pass
	tx2exons[tx_id][no] = Interval(st,sp)
	tx2exons[tx_id]['chrom'] = chrom
f.close()

print >> sys.stderr,"[%s] Read exons." % (time.ctime(time.time()))

# genes2exons
gene2exons = dict()
for gene in gene2tx:
	for tx in gene2tx[gene]:
		if not tx2exons.has_key(tx): continue
		for no in tx2exons[tx]:
			if gene not in gene2exons:
				gene2exons[gene] = dict()
				gene2exons[gene]['chrom'] = tx2exons[tx]['chrom']
			else:
				pass
			if no not in gene2exons[gene] and no != 'chrom':
				gene2exons[gene][no] = tx2exons[tx][no]
			elif no in gene2exons[gene] and no != 'chrom':
				gene2exons[gene][no] = gene2exons[gene][no].union(tx2exons[tx][no])

print >> sys.stderr,"[%s] Built gene->exons." % (time.ctime(time.time()))

for gene in gene2exons:
	for no in gene2exons[gene]:
		if no == 'chrom': continue
		print "%s\t%s\t%s\t%s\t%s" % (gene,gene2exons[gene]['chrom'],no,gene2exons[gene][no].l,gene2exons[gene][no].r)
		
