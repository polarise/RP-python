#!/home/paulk/software/bin/python
from __future__ import division
import sys
import pysam
from key_functions import *

try:
	regionfile = sys.argv[1]
	tabixfn = sys.argv[2]
	outfile = sys.argv[3]
except IndexError:
	print >> sys.stderr,"Usage: %s <regionfile> <tabixfn> <outfile>" % sys.argv[0]
	sys.exit(1)

tabixfile = pysam.Tabixfile(tabixfn)
exon_counts = dict()

f = open(regionfile)
for row in f:
	rname,exonic_regions,intronic_regions = row.strip().split('\t')
	for exonic_region in exonic_regions.split(','):
		included_lines = tabixfile.fetch(region=exonic_region[3:])
		included_exons = list(parse_lines(included_lines,'*',True)[0])
	
	for x in included_exons:
		if x not in exon_counts:
			exon_counts[x] = [1,0]		# inclusion, skipping
		else:
			exon_counts[x][0] += 1
	
	for intronic_region in intronic_regions.split(','):
		skipped_lines = tabixfile.fetch(region=intronic_region[3:])
		skipped_exons = list(parse_lines(skipped_lines,'*',True)[0])
	
	for y in skipped_exons:
		if y not in exon_counts:
			exon_counts[y] = [0,1]
		else:
			exon_counts[y][1] += 1
f.close()

f = open(outfile,'w')
for e in exon_counts:
	print >> f,e+"\t"+"\t".join(map(str,exon_counts[e]))
f.close()
