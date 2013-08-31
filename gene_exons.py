#!/home/paulk/software/bin/python
from __future__ import division
from random import randint
from sys import exit,argv,stderr

def sort_tuple(tup_list,by=0):
	"""
	# convert tuple to dictionary
	# where the sorting key is repeated make a list at that key
	
	# some sanity checks
	# 1-check that all elements have the same sizes of tuples
	# 2-check that all elements in 'by' are same type
	"""	
	dic = dict()
	for t in tup_list:
		T = t[by]
		if T not in dic:
			dic[t[by]] = [t]
		else:
			dic[t[by]] += [t]
	
	# now sort the keys of dic
	keys_dic = dic.keys()
	keys_dic.sort()		# in-place sort
	
	# now rebuild the list of tups
	new_tup_list = list()
	for k in keys_dic:
		for t in dic[k]:
			new_tup_list += [t]
	
	return new_tup_list
	
def validate_sort_tuple(old,new,by):
	"""
	objective: 	validate that sort_tuple() works correctly
	result:			OK
	"""
	l = len(old)		# assume len(new) is the same -- it should be!
	test_old = [old[i][by] for i in xrange(l)]
	test_new = [new[i][by] for i in xrange(l)]
	test_old.sort()
	for i in xrange(l):
		if test_old[i] != test_new[i]:
			return False
	return True
	
def gene_exons(L):
	"""
	Gene-exon extractor
	"""
	exons = dict()
	i = 0	# state index
	l = 0	# position index
	while l < len(L):
		term0 = L[l][1]
		i += 1
		l += 1
		tx = set([L[l][2]])
		while i != 0:		# in between ends
			if L[l][0] == 0:
				term1 = L[l][1]
				tx.add(L[l][2])
				i += 1	#	0->0 state transition
			elif L[l][0] == 1:
				term1 = L[l][1]
				tx.add(L[l][2])
				i -= 1	# 1->0 state transition
			l += 1	# step through list
		exons[(term0,term1)] = tx	# create a new gene exon
		
	return exons		

#--

try:
	fn = argv[1]
except IndexError:
	print >> stderr,"""\
Script to extract gene-exons from a GTF file
Usage: ./gene_exons.py <GTF>
"""
	exit(1)

f = open(fn)
genes = dict()
other_data = dict()
for line in f:
	l = line.strip().split('\t')
	st = int(l[3])
	sp = int(l[4])
	annot = [j.strip().strip(';').lstrip('"').rstrip('"') for j in l[8].strip().split(' ')]
	g_id = annot[1]
	tx_id = annot[3]
	if g_id not in genes:
		genes[g_id] = [(0,st,tx_id),(1,sp,tx_id)]
	else:
		genes[g_id] += [(0,st,tx_id),(1,sp,tx_id)]
	if g_id not in other_data:
		other_data[g_id] = (l[0],annot[7],l[6])	# chrom,gene-name and strand
f.close()

for g in genes:	
	gexons = gene_exons(sort_tuple(genes[g],1))
	for ss in sort_tuple(gexons.keys(),0):
		print "%s\t%s\t%s\t%s\t%s\t%s\t%s"%(g,other_data[g][1],other_data[g][0],ss[0],ss[1],other_data[g][2],",".join(gexons[ss]))	# gene_id | gene_name | start | end | strand | txs overlapping
