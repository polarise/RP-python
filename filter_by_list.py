#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import argparse

parser = argparse.ArgumentParser(description="Script to data by a list")
parser.add_argument('-d','--data',help="data file whose rows will be filtered")
parser.add_argument('-l','--list',help="file containing the list to filter by")
parser.add_argument('-o','--outfile',help="output file")

args = parser.parse_args()

datafn = args.data
listfn = args.list
outfile = args.outfile

data = dict()
for row in open(datafn):
	l = row.strip().split('\t')
	for r in l[0].split(','):
		try:	# exons
			A,B = r.split(':')
			if A not in data:
				data[A] = {B:l[1:]}
			else:
				data[A][B] = l[1:]
		except ValueError: # not exons
			data[l[0]] = l[1:]

if outfile: f = open(outfile,'w')
else: f = stderr
missing = 0
for row in open(listfn):
	A = row.strip()
	if data.has_key(A) and isinstance(data[A],dict):
		try:
			for B in data[A]:
				print >> f,"\t".join([A+":"+B]+data[A][B])
		except KeyError:
			missing += 1
	elif data.has_key(A) and isinstance(data[A],list):
		try:
			print >> f,"\t".join([A]+data[A])
		except KeyError:
			missing += 1
if outfile: f.close()
print >> stderr,"Missing %s transcripts."%missing
