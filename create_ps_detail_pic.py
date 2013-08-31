#!/home/paulk/software/bin/python
from __future__ import division
from cPickle import load,dump,HIGHEST_PROTOCOL
from sys import argv,exit,stderr
import csv

try:
	inf = argv[1]
	outf = argv[2]
except IndexError:
	print >> stderr,"""\
Script to construct a PIC with probeset to its coordinates.
Usage:./create_ps_detail_pic.py <inf> <outf>
<inf> - Affymetrix annotation file e.g. HuEx-1_0-st-v2.na31.hg19.probeset.csv
<outf> - name of output file e.g. ps_detail.na31.hg19.pic"""
	exit(1)

# create a probeset-detail map
c = 0
f = open(inf)
handle = csv.reader(f,delimiter=',',quotechar='"')
ps_detail = dict()
for row in handle:
	if c > 20: break
	if row[0][0] == 'p' or row[0][0] == '#' or row[0][0] == 't': continue
	#ps_detail[int(row[0])] = row[1]+":"+"-".join(row[3:5])+":"+row[2]		# uncomment for probeset file
	ps_detail[int(row[0])] = row[2]+":"+"-".join(row[4:6])+":"+row[3]			# use for transcript file
	c += 0
f.close()

g = open(outf,'w')
dump(ps_detail,g,HIGHEST_PROTOCOL)
g.close()
