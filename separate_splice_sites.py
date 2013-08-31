#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

try:
	f = open(argv[1])
	g = open(argv[2],'w')
	h = open(argv[3],'w')
	len_5 = int(argv[4])
	len_3 = int(argv[5])
except IndexError:
	print >> stderr,"Usage: ./script.py <combined_file> <five.fasta> <three.fasta> <len_5> <len_3>"
	exit(1)

for row in f:
	l = row.strip().split('\t')
	try:
		if len(l[2]) != len_5:
			l[2] = l[2]+"n"*(len_5-len(l[2]))
	except IndexError:
		pass
	try:
		if len(l[3]) != len_3:
			l[3] = l[3]+"n"*(len_3-len(l[3]))
	except IndexError:
		pass
	try:
		print >> g,">%s\n%s" % (l[0],l[2])
	except IndexError:
		print >> g,">%s" % l[0]
		print >> g,"n"*len_5
	try:
		print >> h,">%s\n%s" % (l[1],l[3])
	except IndexError:
		print >> h,">%s" % l[1]
		print >> h,"n"*len_3
f.close()
	
