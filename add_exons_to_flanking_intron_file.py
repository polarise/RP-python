#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from key_functions import parse_lines
import pysam 

f = open(argv[1])
t = pysam.Tabixfile("resources/Homo_sapiens.GRCh37.66.gtf.gz")
for row in f:
	if row[0] == 'u': continue
	l = row.strip().split('\t')
	regions = [l[0],l[1],l[5],l[6]]
	the_exons = ""
	for region in regions:
		result = t.fetch(region[3:-2])
		strand = region[-1]
		exons,no_lines = parse_lines(result,strand,get_transcripts=True)
		the_exons += ",".join(exons) + "\t"
	print row.strip()+"\t"+the_exons
f.close()
	
