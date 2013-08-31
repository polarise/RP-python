#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import pysam
from key_functions import complementDNA

fastafile = pysam.Fastafile("resources/refs/hg19/Homo_sapiens.GRCh37.66.dna.fa")

f = open("u12_introns_all_norm_ps_details.txt")
for row in f:
	if row[0] == 'i': continue
	l = row.strip().split('\t')
	c1 = map(str,[l[8][3:],int(l[11]),int(l[11])+1])
	c2 = map(str,[l[8][3:],int(l[12])-1,int(l[12])])
	reg1 = c1[0]+":"+c1[1]+"-"+c1[2]
	reg2 = c2[0]+":"+c2[1]+"-"+c2[2]
	if l[-6] == "U12-U2":
		print l[4],
		if l[14] == '-':
			print complementDNA(fastafile.fetch(region=reg2))[::-1]+"-"+complementDNA(fastafile.fetch(region=reg1))[::-1]
		else:
			print fastafile.fetch(region=reg1)+"-"+fastafile.fetch(region=reg2)
f.close()
