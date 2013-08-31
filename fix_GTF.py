#!/home/paulk/software/bin/python
from sys import argv,exit,stderr

f = open(argv[1])
for row in f:
	l = row.strip().split('\t')
	if l[0] not in map(str,range(1,23))+['X','Y','M','MT']: pass
	else: print "chr"+row.strip()
f.close()
