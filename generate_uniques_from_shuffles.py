#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr

# takes output from generate_shuffles.py e.g. shuffles.txt having been sorted using
# cut -d "," -f1-4 shuffles.txt | sort -t "," -k1,1n -k2,2n -k3,3n -k4,4n | uniq > cases.txt
# cut -d "," -f1-4 shuffles.txt | sort -t "," -k5,5n -k6,6n -k7,7n -k8,8n | uniq > controls.txt
# and gives uniq cases i.e. uniq_cases.txt or uniq_controls.txt, respectively

f = open(argv[1])
the_ones = set()
for row in f:
	l = row.strip().split(',')
	l.sort()
	the_ones.add(tuple(l))
f.close()

for s in the_ones:
	print ",".join(list(s))
