#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from scipy import *
import argparse

parser = argparse.ArgumentParser(description="Script to combine t-stats from two different platforms")
parser.add_argument('type',choices='ep',help="'e' - exonic; 'p' - probeset")
parser.add_argument('-r','--rnaseq',help="file of rna-seq data as feature|t-stat|...")
parser.add_argument('-e','--exonarray',help="file of exon array data as feature|t-stat|...")
parser.add_argument('-o','--outfile',help="output filename")

args = parser.parse_args()

t = args.type
gene_exon_file = args.rnaseq
ps_to_exon_file = args.exonarray
outfile = args.outfile

t_stats_gex = dict()
f = open(gene_exon_file)
for row in f:
	l = row.strip().split('\t')
	if t == 'e':
		t_stats_gex[l[0]] = l[1] # for gene exons
	elif t == 'p':
		t_stats_gex[l[1]] = l[2]	# for probeset regions
f.close()

t_stats_psx = dict()
if t == 'p':
	# for probeset regions
	f = open(ps_to_exon_file)
	for row in f:
		l = row.strip().split('\t')
		t_stats_psx[l[1]] = l[2]	# for probeset regions
	f.close()
elif t == 'e':
	# for ps_to_exon - there may be be overlapping exons
	f = open(ps_to_exon_file)
	for row in f:
		l = row.strip().split('\t')
		for l0 in l[0].split(','):
			if l0 not in t_stats_psx:
				t_stats_psx[l0] = [float(l[1])]
			else:
				t_stats_psx[l0] += [float(l[1])]
	f.close()

f = open(outfile,'w')
keys = set(t_stats_gex.keys()+t_stats_psx.keys())
for key in keys:
	try:
		gex_tstat = t_stats_gex[key]
	except KeyError:
		gex_tstat = 'NA'
	try:
		psx_tstat = t_stats_psx[key]
	except KeyError:
		psx_tstat = 'NA'
	if gex_tstat != 'NA' and psx_tstat != 'NA':
		if t == 'p': print >> f,key+"\t"+gex_tstat+"\t"+psx_tstat
		elif t == 'e': print >> f,key+"\t"+gex_tstat+"\t"+str(mean(psx_tstat))
f.close()
