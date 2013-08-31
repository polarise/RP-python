#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr,stdout
from scipy import mean
import argparse

parser = argparse.ArgumentParser(description="Script to filter data in columns. Assumes that the columns to be filtered follow one another adjacently.")
parser.add_argument('tabfile',help="tab-delimited file of data (required)")
parser.add_argument('-o','--outfile',help="output file (required)")
parser.add_argument('-s','--start-col',default=1,type=int,help="first column")
parser.add_argument('-n','--no-cols',default=8,type=int,help="number of columns to filter")
parser.add_argument('-m','--mean',type=float,help="filter by mean value defined")
parser.add_argument('-v','--value',type=float,help="filter by value define present in at least one column")
parser.add_argument('-a','--at-least-one',type=float,nargs=2,help="filter by at least n above the given threshold t e.g. 4 0.018 is at four are above 0.018")

args = parser.parse_args()

fn = args.tabfile
ofn = args.outfile
colfrom = args.start_col
nocols = args.no_cols
value = args.value
at_least = args.at_least_one[0]
thresh = args.at_least_one[1]
m = args.mean

f = open(fn)
if ofn: g = open(ofn,'w')
else: g = open(fn+".over%s"%m,'w')
total_cols = 0
final = -1
for row in f:
	l = row.strip().split('\t')
	if not total_cols: total_cols = len(l)
	final = colfrom + nocols
	if final == total_cols:
		all_cols = l[colfrom:]
	else:
		all_cols = l[colfrom:final]
	lv = list()
	for v in all_cols:
		try:
			lv += [float(v)]
		except ValueError:
			lv += ['NA']	
	#lv = map(float,all_cols)
	if isinstance(value,float):
		if value not in lv:
			print >> g,"\t".join(l[0:colfrom]+map(str,lv))
	elif isinstance(m,float):
		if mean(lv) >= m:
			print >> g,"\t".join(l[0:colfrom]+map(str,lv))
	elif isinstance(at_least,float):
		if sum([1 for i in xrange(nocols) if lv[i] >= thresh]) >= at_least and lv.count('NA') <= 0:
			print >> g,"\t".join(l[0:colfrom]+map(str,lv))
f.close()
if ofn: g.close()
	
