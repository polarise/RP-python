#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from random import randint

def PrintStatic(line):
      stderr.write("\r%s"%line.ljust(50))
      stderr.flush()

def shuffle_list(a_list):
	shuffled_list = list()
	while len(a_list) > 0:
		i = randint(0,len(a_list)-1)
		shuffled_list.append(a_list.pop(i))	
	return tuple(shuffled_list)
	
shuffles = set()
c = 0
while len(shuffles) < 40320:
	PrintStatic("Iteration number %s; length of shuffles set is %s" % (c,len(shuffles)))
	l = range(3,11)
	shuffles.add(shuffle_list(l))
	c += 1
print >> stderr
print >> stderr,"Done!"

for s in shuffles:
	print ",".join(map(str,list(s)))
