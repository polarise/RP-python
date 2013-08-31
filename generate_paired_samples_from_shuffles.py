#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

f = open(argv[1])
A_set = set()
B_set = set()
main = set(map(str,range(3,11)))
for row in f:
	A = set(row.strip().split(','))
	B = main.difference(A)
	print " ".join(list(A)+list(B))
f.close()
