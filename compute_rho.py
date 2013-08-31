#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import rpy2.robjects as R
from rpy2.robjects.packages import importr

qvalue = importr('qvalue')

cor = R.r['cor']
qunif = R.r['qunif']
runif = R.r['runif']
sort = R.r['sort']

try:
	prefix = argv[1]
except IndexError:
	print >> stderr,"Usage: %s [core|all]" % argv[0]
	exit(1)

#assert prefix == 'core' or prefix == 'all'

if prefix == 'core': quniform = sort(qunif(runif(123266)))
elif prefix == 'full': quniform = sort(qunif(runif(131997)))

import fnmatch
import os

for file in os.listdir('permutation_tests'):
	#if fnmatch.fnmatch(file,'%s_norm_ps.[0-9]*' % prefix):
	if fnmatch.fnmatch(file,'%s_sanitised.paired.[0-9]*.out.tests' % prefix):
		f = open('permutation_tests/'+file)
		data = list()
		data = [row.strip().split('\t')[3] for row in f]
		data.sort()
		data = R.FloatVector(map(float,data))
		q = qvalue.qvalue(data)
		f.close()
		print file+"\t"+str(q[1][0])
#		print file+"\t"+str(cor(data,quniform,method="pearson")[0])
