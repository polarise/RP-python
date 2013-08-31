#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from os import system

f = open(argv[1])
coords = list()
for row in f:
	a,b,c,d,e,g = row.strip().split('\t')
	coords.append((a,b,c))
f.close()

for c in coords:
	cmd = "samtools mpileup -C50 -f ~/bowtie-0.12.7/scripts/hg19.fa -r %s:%s-%s /data2/paulk/RP/output2/4C/accepted_hits.bam"%(c[0],c[1],c[2])
	print >> stderr,cmd
	system(cmd)
