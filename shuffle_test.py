#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from multiprocessing import Process

f = open("permutation_tests/paired_shuffles.txt")

c = 0
for row in f:
	if c > 5: break
	r = row.strip()
	print >> stderr,r
#	cmd = "platform_comparison.py -n quotient.out.normalised p -s %s -o quotient.%s.out" % (r,"_".join(r.split(' ')))
#	cmd2 = "platform_comparison.py -n eBayesIV/all_difference.out.normalised p -s %s -o difference.paired.%s.out" % (r,"_".join(r.split(' ')))
	cmd2 = "platform_comparison.py -n eBayesVII/full_sanitised.normalised p -s %s -o full_difference_sanitised.paired.%s.out" % (r,"_".join(r.split(' ')))
#	p = Popen(cmd,stdout=PIPE,shell=True)
	p2 = Popen(cmd2,stdout=PIPE,shell=True)
#	print >> stderr,p.communicate()[0]
	print >> stderr,p2.communicate()[0]
	c += 0
f.close()
