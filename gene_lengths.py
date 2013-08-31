#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import dump,HIGHEST_PROTOCOL
import argparse

print >> stderr,"Warning: this script can either provide exonic or exonic+intronic bases. You have to be CAREFUL!!!"

parser = argparse.ArgumentParser(description="Script to get the length of exonic bases in a gene.")
parser.add_argument('genefile',help="the input gene file")
parser.add_argument('-p','--pic-file',help="PIC file to write to")
parser.add_argument('-o','--out-file',help="tab-delim'd file")
parser.add_argument('-f','--features',default=False,action='store_true',help="takes a gene file with features (exons or introns) instead of a gene or transcript file")

args = parser.parse_args()

gf = args.genefile
pf = args.pic_file
of = args.out_file
feats = args.features

gene_lengths = dict()
f = open(gf)
for row in f:
	l = row.strip().split('\t')
	if feats:
		length = int(l[-1])
	else:
		length = int(l[4])-int(l[3])+1
	if feats:
		s = l[0]+":"+l[1]
		if s not in gene_lengths:
			gene_lengths[s] = length
		else:
			gene_lengths[s] += length			
	else:
		if l[0] not in gene_lengths:
			gene_lengths[l[0]] = length
		else:
			gene_lengths[l[0]] += length
f.close()

if pf:
	dump(gene_lengths,open(pf,'w'),HIGHEST_PROTOCOL)
	exit(0)

if of: f = open(of,'w')
c = 0
for g in gene_lengths:
	if c > 20: break
	if of: print >> f,g+"\t"+str(gene_lengths[g])
	else: print >> stderr,g+"\t"+str(gene_lengths[g])
	c += 0
if of: f.close()
