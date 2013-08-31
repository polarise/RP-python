#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from random import choice
from re import search

def intron_length(region1,region2,pos1,pos2):
	c1,st1_sp1,sd1 = region1.split(':')
	c2,st2_sp2,sd2 = region2.split(':')
	st1,sp1 = map(int,st1_sp1.split('-'))
	st2,sp2 = map(int,st2_sp2.split('-'))
	if c1 != c2: raise ValueError("Conflict in chromosome names")
	if sd1 != sd2: raise ValueError("Conflict in strands")
	if sd1 == '+': return str(abs((st1+pos1) - (sp2-pos2))+1)
	elif sd1 == '-': return str(abs((st2+pos2) - (sp1-pos1))+1)

files = ["up5.score","up3.score","down5.score","down3.score"]
data = dict()
for fn in files:
	i = 0
	f = open(fn)
	for row in f:
		l = row.strip().split('\t')
		if 'row_%s' % i not in data: data['row_%s' % i] = [l[0],l[2]]
		else: data['row_%s' % i] += [l[0],l[2]]
		i += 1
	f.close()

print "up5SS\tup3SS\tup_len\tup5_score\tup3_score\tdown5SS\tdown3SS\tdown_len\tdown5_score\tdown3_score"
c = 0
for d in data:
	if c > 20: break
	v = data[d]
#	print v
	print "\t".join([v[0],v[2],intron_length(v[0],v[2],3,3),v[1],v[3],v[4],v[6],intron_length(v[4],v[6],3,3),v[5],v[7]])
	c += 0
