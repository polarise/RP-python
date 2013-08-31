#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import *
import pysam

def bedrow2coords(row):
	"""
	given a BED row returns a list of tuples of junction coordinates
	"""
	l = row.strip().split('\t')
	begin = int(l[1])
	lengths = map(int,l[10].split(',')[:-1])
	starts = map(int,l[11].split(',')[:-1])
	jxns = list()
	for i in xrange(int(l[9])-1):
		jxns += [(begin + starts[i] + lengths[i],begin + starts[i+1])]
	return jxns

def has_exon_skipped(jxn,jxns):
	"""
	the simplest way to determine whether skipping has occurred is to disregard the locus and treat starts and
	ends as separate; also, assume that we have checked and found that jxn[0] and jxn[1] do not occur together
	"""
	starts = [j[0] for j in jxns]
	ends = [j[1] for j in jxns]
	if jxn[0] in starts and jxn[1] in ends:
		return True
	else:
		return False

tf = pysam.Tabixfile(argv[2])

f = open(argv[1])
c = 0

exon_not_skipped = 0
exon_skipped = 0
total = 0
SR = dict()

# iterate over all junction-spanning reads
for row in f:
	if row[0] == '#': continue
	if c >= 10000: break
	l = row.strip().split('\t')
	total += 1
	start = int(l[3])
	
	# get the junction boundaries from the CIGAR string
	end,exon1_sp,exon2_st = cigar2end(l[5],start)
	
	# construct this junction
	jxn = (exon1_sp,exon2_st)
#	print "start: %s; end: %s" % jxn
	
	# construct the region string
	region = l[2]+":"+l[3]+"-"+str(end)
	
	# get all transcripts that overlap this region
	result = tf.fetch(region=region)
	
	# for each row in the bed result...
	for r in result:
		# construct the junctions
		jxns = bedrow2coords(r)
		
		# find out if this read corresponds at least one of the junctions
		if jxn in jxns:
			exon_not_skipped += 1
			break
		# otherwise find out if an exon has been skipped
		if has_exon_skipped(jxn,jxns):
			exon_skipped += 1
			SR[l[0]] = [jxn,r]
			break
	c += 1
f.close()

print "not skipped = %s" % exon_not_skipped
print "skipped     = %s" % exon_skipped
print "total       = %s" % total

for s in SR:
	
	print s+"\t"+
