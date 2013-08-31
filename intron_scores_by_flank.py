#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from random import choice
from re import search

def PrintStatic(line):
	stderr.write("\r%s" %line.ljust(50)+" "*20)
	stderr.flush()

def intron_length(region1,region2,pos1,pos2):
	c1,st1_sp1,sd1 = region1.split(':')
	c2,st2_sp2,sd2 = region2.split(':')
	st1,sp1 = map(int,st1_sp1.split('-'))
	st2,sp2 = map(int,st2_sp2.split('-'))
	if c1 != c2: raise ValueError("Conflict in chromosome names")
	if sd1 != sd2: raise ValueError("Conflict in strands")
	if sd1 == '+': return abs((st1+pos1) - (sp2-pos2))
	elif sd1 == '-': return abs((st2+pos2) - (sp1-pos1))

f = open("resources/Homo_sapiens.GRCh37.66.gtf.upstream_introns")
data = dict()
i = 0
for row in f:
	data['row_%s' % i] = row.strip().split('\t')
	i += 1
f.close()

f = open("resources/Homo_sapiens.GRCh37.66.gtf.downstream_introns")
i = 0
for row in f:
	data['row_%s' % i] += row.strip().split('\t')
	i += 1
f.close()

up_scores = dict()
f = open("upstream_intron.full")
for row in f:
	l = row.strip().split('\t')
#	PrintStatic(str(l))
	if len(l) != 5: continue
	up_scores[l[0],l[1]] = l[4]
f.close()

down_scores = dict()
f = open("downstream_intron.full")
for row in f:
	l = row.strip().split('\t')
#	PrintStatic(str(l))
	if len(l) != 5: continue
	down_scores[l[0],l[1]] = l[4]
f.close()

print "up5SS\tup3SS\tup_len\tup3_score\tdown5SS\tdown3SS\tdown_len\tdown3_score"
c = 0
for d in data:
	l = data[d]
	if c > 5: break
	if len(l) != 8: continue
	try:
		up_score = up_scores[l[0],l[1]]
	except KeyError:
		try:
			up_score = up_scores[l[1],l[0]]
		except KeyError:
			up_score = 'NA'
	try:
		down_score = down_scores[l[4],l[5]]
	except KeyError:
		try:
			down_score = down_scores[l[5],l[4]]
		except KeyError:
			down_score = 'NA'
	print "\t".join(map(str,[l[0],l[1],intron_length(l[0],l[1],3,3),up_score,l[4],l[5],intron_length(l[4],l[5],3,3),down_score]))
	c += 0
