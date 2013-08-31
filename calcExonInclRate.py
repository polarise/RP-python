#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import *
import pysam
from cPickle import load

def count_incl2excl(jreads,exon,sd,exon_st,exon_sp,pexon_st,pexon_sp,nexon_st,nexon_sp,tally,read_reads):
	for read in jreads:
		if read.qname not in read_reads: read_reads[read.qname] = 0	# if we've seen this read before...
		else: continue	# get the next read
		
		if exon not in tally: tally[exon] = [0,0,0,0,0]		# left_incl.,right_incl.,excl./skip,first/last_exon_only,all
		
		start = read.pos+1	# start pos of the read
		cigar = read.cigar
		
		if len(cigar) > 3: continue	# not interested in multi-junction reads
		lengths = [c[1] for c in cigar] 
		
		# handle first and second junction reads differently
		end = start+sum(lengths)-1 # end position of the read
		exon1_sp = start+lengths[0]-1	# the end of the first exon that the read terminates
		exon2_st = end-lengths[2]+1		# the beginning of the next exon that the read continues along

		if (exon1_sp <= exon_st and (exon_st <= exon2_st <= exon_sp)):
			tally[exon][0] += 1 				# left incl.
		elif ((exon_st <= exon1_sp <= exon_sp) and exon2_st >= exon_sp):
			tally[exon][1] += 1					# right incl.
		elif (exon1_sp <= exon_st) and (exon2_st >= exon_sp):
			tally[exon][2] += 1					# excl./skip
		elif start > exon_sp or end < exon_st:
			tally[exon][3] += 1

		tally[exon][-1] += 1
	
	return

try:
	bf = argv[1]
	of = argv[2]
except IndexError:
	print >> stderr,"Usage: %s <bamfile_jxns> <outfile> [<exons_to_use>]" % argv[0]
	exit(0)

# reference list of all exons
f = open("/data2/paulk/RP/resources/exons.hg19.Ens66.0-based.pic")
exons = load(f)
f.close()

try:
  ref = argv[3]
  g = open(ref)
  non_redundant_exons = map(lambda x:x.strip(),g.readlines())
  g.close()
except IndexError:
  print >> stderr,"Warning: using all exons!"
  g = open("/data2/paulk/RP/resources/exons.hg19.Ens66.0-based.non_redundant.pic")
  non_redundant_exons = load(f)
  g.close()

no_exons = len(non_redundant_exons) #361400 #561192 #1234927

b = pysam.Samfile(bf,'rb')

c = 0
tally = dict()			# where the tallies are kept
read_reads = dict()	# a dictionary to keep track of read reads so as not to count them twice
for e in non_redundant_exons:
	pct = c*100/no_exons
	PrintStatic("Progress: %.2f%% [analysed %d exons]" % (pct,c))
#	if c >= 1000: break
	tx,ex = e.split(':')
	exon = int(ex)
	
	# if this is a first or last exon dump it and try again...
	if exon == 1: c += 1; continue
	if terminal_exon(e,exons)[0]: c += 1; continue
	
	# define search boundaries
	cexcoords = exons[tx+":"+str(exon)]
	chrom,st_sp,sd = cexcoords.split(':')
	cst,csp = map(int,st_sp.split('-'))	# 0-based
	
	mod_len = 47	# value by which to modify position coordinates

	if sd == '+':
		pexcoords = exons[tx+":"+str(exon-1)]
	elif sd == '-':
		pexcoords = exons[tx+":"+str(exon+1)]	# read coordinates are fixed as leftmost regardless of strand; reads on reverse strand with then overlap on the cassette exon beginning at the downstream exon
	chrom,st_sp,sd = pexcoords.split(':')
	pst,psp = map(int,st_sp.split('-'))	# 0-based
	
	if sd == '+':
		nexcoords = exons[tx+":"+str(exon+1)]
	elif sd == '-':
		nexcoords = exons[tx+":"+str(exon-1)]
	chrom,st_sp,sd = nexcoords.split(':')
	nst,nsp = map(int,st_sp.split('-')) # 0-based
	
	srch_rgn = chrom+":"+str(pst)+"-"+str(nst+1+50)	# 1-based
	
	try:
		jreads = b.fetch(region=srch_rgn)
	except ValueError:
		c += 1
		continue
	
	# count inclusion/exclusion
	count_incl2excl(jreads,e,sd,cst+1,csp+1,pst,psp,nst,nsp,tally,read_reads)
								 #jxn_rds,exon,strand,current_start+1,current_stop+1,reads_that_have_been_read
	c += 1
print >> stderr

f = open(of,'w')	
for t in tally:
	print >> f,"\t".join([t] + map(str,tally[t]))
f.close()
