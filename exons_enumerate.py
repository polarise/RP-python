#!/home/paulk/software/bin/python
import sys

"""
Synopsis
Simple script to enumerate exons by gene.
Exon numbers are counted from 5' of + strand. Sorry.
"""
try:
	fn = sys.argv[1]
except IndexError:
	print >> sys.stderr,"Script to enumerate exons by gene"
	print >> sys.stderr,"Usage: ./exons_enumerate.py <gene_file>"
	sys.exit(1)

f = open(fn,'r')
c = 0
for line in f:
	l = line.strip().split('\t')
	g_id = l[0]
	sd = l[5]
	if c == 0:
		current = g_id
		exno = 1
	else:
		if g_id != current:
			exno = 1
			current = g_id
		else:
			exno += 1
	print g_id+'\t'+str(exno)+'\t'+'\t'.join(l[2:])
	c += 1
