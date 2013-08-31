#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr,stdout
from cPickle import load

#full_dinucls = {(d[:2],d[2:]):0 for d in load(open("/data2/paulk/RP/resources/quartermers.pic"))}
#print >> stderr,len(full_dinucls)

total = 0
dinucls = dict()
f = open(argv[1]) # e.g. 
for row in f:
	l = row.strip().split('\t')
#	try:
#		s1 = l[2][:3].upper()
#		s2 = l[3][-3:].upper()
#	except IndexError:
#		continue
#	if s1 in ['TAG','TGA','TAA'] or s2 in ['ATG']:
#		continue
	try:
		d1 = l[2][3:5].upper()
		d2 = l[3][-5:-3].upper()
	except IndexError:
		total += 1
		continue
		
	if d1 == 'AT' and d2 == 'CC':
		print >> stderr,row.strip()
#	"""
	if (d1,d2) not in dinucls:
		dinucls[d1,d2] = 1
	else:
		dinucls[d1,d2] += 1
	"""
	try:
		full_dinucls[d1,d2] += 1
	except KeyError:
		continue
	"""
	total += 1
f.close()

"""
# add pseudocounts
for_total = 0
for (d1,d2) in full_dinucls:
	full_dinucls[d1,d2] += 1
	for_total += 1

total += for_total
print "x_TOTAL_x\t%s\t" % total
for d1,d2 in full_dinucls:
	print "\t".join(map(str,[d1,d2,full_dinucls[d1,d2],round(full_dinucls[d1,d2]/total*100,5)]))
"""
print "x_TOTAL_x\t%s\t" % total
for d1,d2 in dinucls:
	print "\t".join(map(str,[d1,d2,dinucls[d1,d2],round(dinucls[d1,d2]/total*100,5)]))
