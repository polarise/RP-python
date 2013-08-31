#!/home/paulk/software/bin/python
from sys import argv,exit,stderr
from cPickle import dump,HIGHEST_PROTOCOL
import argparse

plain_chroms = map(str,range(1,23))+['X','Y','MT']

parser = argparse.ArgumentParser(description="Script to parse a gene-formatted file to give a PIC of 0-based regions by default")
parser.add_argument('infile',help="gene-formatted input file; chromosomes can be either <id> or chr<id> e.g. '3' or 'chr3'")
parser.add_argument('outfile',help="output PIC file")
parser.add_argument('-o','--one-based',default=False,action='store_true',help="use 1-based indexing basis [default: 0-based]")
parser.add_argument('-a','--all-chroms',default=False,action='store_true',help="use all chromosome names (even '*MHC*') [default: false]")
parser.add_argument('-s','--suppress-col-two',default=False,action='store_true',help="to be used when dealing with genes; suppress the second column of the gene file [default: false]")

args = parser.parse_args()

fn = args.infile
ofn = args.outfile
one_based_indexing = args.one_based
use_all_chroms = args.all_chroms
suppress = args.suppress_col_two

f = open(fn)
data = dict()
for row in f:
	l = row.strip().split('\t')
	if l[2] not in plain_chroms and not use_all_chroms: continue
	if not one_based_indexing:
		st = int(l[3])-1
		sp = int(l[4])-1
	else:
		st = int(l[3])
		sp = int(l[4])
	if suppress:
		if l[2][0] == 'c': data[l[0]+":"+l[1]] = l[2]+":"+str(st)+"-"+str(sp)+":"+l[5]
		else: data[l[0]+":"+l[1]] = "chr"+l[2]+":"+str(st)+"-"+str(sp)+":"+l[5]		
	else:
		if l[2][0] == 'c': data[l[0]] = l[2]+":"+str(st)+"-"+str(sp)+":"+l[5]
		else: data[l[0]] = "chr"+l[2]+":"+str(st)+"-"+str(sp)+":"+l[5]
f.close()

f = open(ofn,'w')
dump(data,f,HIGHEST_PROTOCOL)
f.close()
