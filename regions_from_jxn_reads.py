#!/home/paulk/software/bin/python
from __future__ import division
import sys

def mod_cigar(cigar):
	cigar_list = list()
	for v in cigar.split('N'):
		for u in v.split('M'):
			cigar_list.append(u)
	
	new_cigar_list = list()
	for i in xrange(len(cigar_list[:-1])):
		if cigar_list[i].find('I') >= 0:
			new_cigar_list.append(int(cigar_list[i-1])+sum(map(int,cigar_list[i].split('I'))))
		elif cigar_list[i].find('D') >= 0:
			new_cigar_list.append(int(cigar_list[i-1])+sum(map(int,cigar_list[i].split('D'))))
		else:
			new_cigar_list.append(int(cigar_list[i]))
	
	return new_cigar_list

def make_exonic_regions(chrom,termini):
	regions = list()
	for t in termini:
		regions.append(chrom+":"+str(t[0])+"-"+str(t[1]))
	return regions

def make_intronic_regions(chrom,termini):
	regions = list()
	for i in xrange(len(termini)-1):
		regions.append(chrom+":"+str(termini[i][1]+1)+"-"+str(termini[i+1][0]-1))
	return regions

f = open(sys.argv[1])
for row in f:
	l = row.strip().split('\t')
	st = int(l[3])
	components = map(int,mod_cigar(l[5]))
	cumsum = [0]
	for i in xrange(len(components)):
		cumsum.append(cumsum[i]+components[i])
	
	sts = map(lambda x:st + x,[cumsum[i] for i in xrange(0,len(cumsum),2)])
	sps = map(lambda x:st + x -1,[cumsum[i] for i in xrange(1,len(cumsum),2)])
	
	termini = zip(sts,sps)
	
	print "\t".join([l[0]]+[",".join(make_exonic_regions(l[2],termini))]+[",".join(make_intronic_regions(l[2],termini))])#,l[5],cumsum

f.close()
