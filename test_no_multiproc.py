#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from multiprocessing import Process

f = open("test.out")
data = [r.strip() for r in f]
f.close()

for d in data:
	print d
