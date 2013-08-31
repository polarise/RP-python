#!/home/paulk/software/bin/python
import sys
from cPickle import load

f = open("resources/quartermers.pic")
quarts = load(f)
f.close()

for q in quarts:
	print "\t".join([q[:2],q[2:]])
