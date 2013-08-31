#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import *

f = open(argv[1])
for row in f:
	l = row.strip().split('\t')
	if len(l) != 4: continue
	if l[2] == '': continue
	print row.strip()+"\t"+intron_length(l[0],l[1],3,3)
f.close()

