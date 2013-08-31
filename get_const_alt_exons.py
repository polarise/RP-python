#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import process_feature
import pysam

tabixfile = pysam.Tabixfile("resources/Homo_sapiens.GRCh37.66.gtf.gz")
c = 0
f = open("alternative_exons.hg19.bed")
meps = dict()
for row in f:
	if c > 5: break
	l = row.strip().split('\t')
	st = int(l[1])
	sp = int(l[2])
	sd = l[4]
	region = ":".join([l[0][3:],"-".join([l[1],l[2]])])
	try:
		results = tabixfile.fetch(region=region)
	except ValueError:
		results = None
	if results == None: continue
	for result in results:
		l2 = result.strip().split('\t')
		st2 = int(l2[3])
		sp2 = int(l2[4])
		sd2 = l2[6]
		if st - 1 <= st2 <= st + 1 and sp - 1 <= sp2 <= sp + 1 and sd == sd2 and l2[2] == 'exon':
			features = process_feature(result.strip())
			exon = features['transcript_id'] + ':' + features['exon_number']
			if exon not in meps:
				meps[region] = [exon]
			else:
				meps[region] += [exon]			
	c += 0
f.close()

for m in meps:
	print m+"\t"+",".join(meps[m])
