#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from scipy import *
from scipy import stats
from key_functions import statistical_test,dict_to_file

try:
	fn = argv[1]
	ofn = argv[2]
except IndexError:
	print >> stderr,"""\
Script to perform a statistical test on columns of data one row at a time.
Performs an unpaired t-test by default. Modify to add tests.
Usage:./script.py <infile> <outfile>"""
	exit(1)

cascon = [4,5,8,9,3,6,7,10]
f = open(fn)
normalised_data = dict()
for row in f:
	l = row.strip().split('\t')
	normalised_data[l[0],l[1]] = map(float,l[2:])
f.close()

test_results = statistical_test(normalised_data,cascon)
dict_to_file(test_results,ofn)
