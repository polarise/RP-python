#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import *
import pysam
from cPickle import load

f = open("resources/exons.hg19.Ens66.0-based.pic")
exons = load(f)
f.close()

print "exon\tincl\texcl\ttotal\tupintrlen\texonlen\tdownintrlen"
f = open("test.out")
c = 0
for row in f:
	if c > 20: break
	l = row.strip().split('\t')
	tx,ex = l[0].split(':')
	exon = int(ex)
	bexon_reg = exons[tx+":"+str(exon-1)]
	exon_reg = exons[l[0]]
	aexon_reg = exons[tx+":"+str(exon+1)]
	bintron_length = simple_intron_length(bexon_reg,exon_reg)
	chrom,st_sp,sd = exon_reg.split(':')
	e = map(int,st_sp.split('-'))
	exon_length = abs(e[1] - e[0]) + 1
	aintron_length = simple_intron_length(exon_reg,aexon_reg)
	print row.strip()+"\t"+bintron_length+"\t"+str(exon_length)+"\t"+aintron_length
	c += 0
f.close()
