#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

try:
	fn = argv[1]
	sub_len = int(argv[2])
except IndexError:
	print >> stderr,"""\
Script to subsample reads i.e. reduced n bp reads to r bp where r < n.
Usage:./subsample_reads.py <fastq_file> <r> [<outfile>]"""
	exit(1)

try:
	ofn = argv[3]
except IndexError:
	ofn = "subsample."+fn

TEST_LENGTH = 0
	
f = open(fn)
of = open(ofn,'w')
row_no = 0
for row in f:
	if row_no%4 == 0 or row_no%4 == 2:
		print >>of,row.strip()
	elif row_no%4 == 1 or row_no%4 == 3:
		if not TEST_LENGTH:
			try:
				assert sub_len < len(row.strip())
				TEST_LENGTH = 1
			except:
				print >> stderr,"Error: read length error. Exiting..."
				of.close()
				f.close()
				exit(1)
		print >>of,row.strip()[:sub_len]
	row_no += 1
f.close()
