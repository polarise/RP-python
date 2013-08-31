#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from key_functions import statistical_test,dict_to_file

try:
	fn = argv[1]
	cascon = map(int,argv[2].split(','))
	ofn = argv[3]
except IndexError:
	print >> stderr,"""\
Script to perform statistical test on data.
Usage:./script.py <infile> <comma-sep'd sample names (cases then controls)> <outfile>
Example: ./script.py <infile> 4,5,8,9,3,6,7,10 <outfile>"""
	exit(1)

normalised_data = dict()
f = open(fn)
for row in f:
	l = row.strip().split('\t')
	if l[0] not in normalised_data:
		normalised_data[l[0]] = [map(float,l[1:])]
	else:
		normalised_data[l[0]] += [map(float,l[1:])]
f.close()

# averaging
normalised_data2 = dict()
for e in normalised_data:
	if len(normalised_data[e]) > 1:
		no = len(normalised_data[e]) # the number of probesets
		normalised_data2[e] = [sum([normalised_data[e][i][j] for i in xrange(no)])/no for j in xrange(8)]
	else:
		normalised_data2[e] = normalised_data[e][0]

#g = open(ofn,'w')
#for e in normalised_data2:
#	print >> g,"\t".join([e]+map(str,normalised_data2[e]))
#g.close()

test_results = statistical_test(normalised_data2,cascon,test_type="unpaired t-test")
dict_to_file(test_results,ofn)

