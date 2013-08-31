#!/usr/bin/python
'''
Paul K. Korir
2011-03-10
NUI, Galway
Script that excludes a gene from a SAM file
'''
from __future__ import division
import os,sys
import time

def cigar2end(cigar,start):
	'''
	given simple CIGAR string (with the M and N only) returns the position of the last nucleotide
	'''
	excl_M = cigar.split('M')		# split by 'M' first
	excl_N = [c.split('N') for c in excl_M]	# for each in excl_M now split by 'N'; may result in a list with some lists
	vals = []
	for l in excl_N:
		if isinstance(l,list):
			vals += l		# if l is a list stick it at the end
		else:
			vals.append(l)		# if l is an atom append it at the end
	length = 0
	for i in vals:
		if i != '':
			length += int(i)
		else:
			pass
	return start+length-1

chromosome_symbols = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','x','X','y','Y','m','M','mt','MT','mT','Mt']

try:
	infile = sys.argv[1]
#	chromosome = sys.argv[2]
#	assert chromosome in chromosome_symbols
#	start_position = int(sys.argv[3])
#	end_position = int(sys.argv[4])
#	assert start_position <= end_position
	genes_excl = sys.argv[2]

except IndexError,ValueError:
	print "Inadequate number of input variables."
	print "Usage: /excl_genes.py <sam_file> <gene_file> [<outfile_sam>]"
	print
	print "<sam_file>       - a valid SAM file"
	print "<gene_file>      - file containing genes to exclude"
	print "<outfile_sam>    - SAM output file"
	sys.exit(1)

OF_FLAG = True
try:
	outfile = sys.argv[3]
	if outfile[-4:] == '.sam':
		pass
	else:
		outfile += '.sam'
except IndexError:
	print "Warning: Optional parameter <outfile_sam> not specified. Only excluded genes will be output in SAM files."
	print
	OF_FLAG = False


f = open(infile,'r')
if OF_FLAG:
	g = open(outfile,'w')
k = open(genes_excl,'r')
for m in k:
	start = time.time()
	mine = m.strip().split('\t')
	gene = mine[0]
	chromosome = mine[1]
	start_position = int(mine[2])
	end_position = int(mine[3])
	print "%s|%s|%s|%s"%(gene,chromosome,start_position,end_position)
	h = open(gene+".sam",'w')
	count_for = 0
	count_against = 0
	for l in f:
		line = l.strip().split('\t')
		if line[2] == 'chr'+chromosome and (start_position <= cigar2end(line[5],50)+int(line[3]) and int(line[3]) <= end_position):	# check whether the chromosome is correct, the end of the read coincides with the beginning or after of the gene or the beginning of the read coincides with the end or before of the gene
			h.write(l)
			count_for += 1
		else:
			if OF_FLAG:
				g.write(l)
				count_against += 1
			else:
				count_against += 1
	h.close()
	f.seek(0,0)	# go back to the beginning of the SAM input file
	stop = time.time()	
	print "No. of reads that mapped to gene located at:"
	print "Chromosome %s, start: %s, end: %s"%(chromosome,start_position,end_position)
	print "Count: %s reads."%(count_for)
	print
	print "No. of reads that do not map:"
	print "Count : %s reads."%(count_against)
	print
	print "Time taken: % seconds."%(stop - start)
	print
f.close()
if OF_FLAG:
	g.close()
