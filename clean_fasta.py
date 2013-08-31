#!/home/paulk/software/bin/python
from sys import argv,exit,stderr,stdout

"""
Simple script to get rid of bad values from FASTA file.
"""

try:
	fastafn = argv[1]
	outfn = argv[2]
	typ = int(argv[3])
	len_35 = int(argv[4])
except IndexError:
	print >> stderr,"Usage: %s <fasta> <outfn> <3|5> <len_3|5>" % argv[0]
	exit(1)

f = open(fastafn)
g = open(outfn,'w')
for row in f:
	if row[0] == '>':
		label = row.strip()
		continue
	if row.strip().find('n') >= 0 or row.strip().find('N') >= 0:
		continue
	elif (typ == 5 and len(row.strip()) <> len_35) or (typ == 3 and len(row.strip()) <> len_35):
		continue
	print >> g,label
	print >> g,row.strip()
g.close()
f.close()
