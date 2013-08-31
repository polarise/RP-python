#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

f = open(argv[1])
for row in f:
	l = row.strip().split('\t')
	if len(l) != 4: continue
	print ">"+l[1]
	print l[3]
f.close()
	
	
