#!/home/paulk/software/bin/python
from __future__ import division
import os, time
from sys import argv,exit,stderr
from key_functions import *

def PrintStatic(line):
	stderr.write("\r%s\n"%line.ljust(100))
	stderr.flush()

"""
Bugs
20110805 - Basic; cast line[3] and line[4] to ints! Imagine!
"""

"""
For each line in the annotation file we populate the following dictionary
	genes = {gene_id:{'gene_name': , 'chr': , 'start': , 'end': , 'strand': }}
However, if we come across a line that conflicts we need to deal with it
How might another line conflict with what is currently in the dictionary?
Each line contains one of either a start_codon, stop_codon, exon, CDS etc and each gene is described by one or several or all of these classifiers. For each, positional information is provided. The goal is to use this data to come up with the gene coordinates hence a conflict will be a set of values under one of the classifiers that differs from what is presently in the dictionary. The resolution of this conflict is by stretching what is currently known so that the 'start' and 'end' keys will be the interval that is the UNION of all classifiers for that gene.
"""

try:
	infile = argv[1]
except IndexError:
	print >> stderr, "Script to collate genes by Ensembl gene ID."
	print >> stderr, "Usage: ./genes.py <GTF-file>"
	exit(1)

f = open(infile,'r')
genes = {}
d = 0
for l in f:
	if d > 20: break
	line = l.strip().split('\t')
	chrm = line[0]
	start = int(line[3])
	end = int(line[4])
	strand = line[6]
	#annot = [j.strip().strip(';').lstrip('"').rstrip('"') for j in line[8].split(' ')]
	feature_dict = process_feature(l)
	gene_id = feature_dict['gene_id']
	#print >> stderr,chrm,start,end,strand,feature_dict,gene_id
	try:
		gene_name = feature_dict['gene_name']
	except IndexError:
		gene_name = "*"
	if gene_id not in genes:
		genes[gene_id] = {'gene_name':gene_name, 'chr':chrm, 'start':start, 'end':end, 'strand':strand}
	elif gene_id in genes:
		if start < genes[gene_id]['start']: # if 'start' is less than what is recorded in the dictionary replace what is in the dictionary (extend); the same applies for end (though we use 'if greater')
			genes[gene_id]['start'] = start
		else: pass
		if end > genes[gene_id]['end']:
			genes[gene_id]['end'] = end
		else: pass
		# unlikely results
		if strand != genes[gene_id]['strand']:
			PrintStatic("%s %s"%(strand,genes[gene_id]['strand']))
			PrintStatic("Strand value conflict at %s"%(gene_id))
			genes[gene_id]['flagged'] = True
		if chrm != genes[gene_id]['chr']:
			PrintStatic("Chromosome value conflict at %s"%(gene_id))
			genes[gene_id]['flagged'] = True			
	d += 0

print >> stderr
c = 0
for gene in genes:
	if c > 20: break
	if 'flagged' not in genes[gene]:
		print gene+'\t'+genes[gene]['gene_name']+'\t'+genes[gene]['chr']+'\t'+str(genes[gene]['start'])+'\t'+str(genes[gene]['end'])+'\t'+genes[gene]['strand']
	c += 0
f.close()
