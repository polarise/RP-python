#!/usr/bin/env python
from __future__ import division
import sys
import os.path
import scipy

try:
	ps_fn = sys.argv[1]
	expr_fn = sys.argv[2]
except IndexError:
	print >> sys.stderr, "Usage: %s <ps_fn> <expr_fn>" % os.path.basename( sys.argv[0] )
	print >> sys.stderr, "ps_fn: probeset_id"
	print >> sys.stderr, "expr_fn: probeset_id | metaprobeset_id | S1 | ... | SN"
	sys.exit( 1 )

# read in the probesets
f = open( ps_fn )
pss = { row.strip():0 for row in f }
f.close()

# read in the expression by computing the mean of controls only
# controls are the last four columns
controls = [2, 5, 6, 9]
f = open( expr_fn )
mean_expr = dict()
pss_expr = dict()
affected_means = list()
unaffected_means = list()
for row in f:
	L = row.strip().split( '\t' )
	mn = scipy.mean( map( float, [L[i] for i in controls] ))
	if L[0] not in mean_expr:
		mean_expr[L[0]] = mn
		if L[0] in pss:
			pss_expr[L[0]] = mn
			print mn
		else:
			print >> sys.stderr, mn
	else:
		raise ValueError( "You have a duplicate probeset. How did that happen?" )
f.close()

# calculate the overall mean and sd
ov_mean = scipy.mean( pss_expr.values() )
ov_sd = scipy.std( pss_expr.values() )

sys.exit( 0 )

#print ov_mean, ov_sd
#print scipy.mean( mean_expr.values() ), scipy.std( mean_expr.values() )

# get all ps that are within 2*sd of this mean :: these are low inclusion probesets
for p in mean_expr:
	if ov_mean-2*ov_sd > mean_expr[p]:
		print p # low inclusion
	elif mean_expr[p] > ov_mean+2*ov_sd:
		print >> sys.stderr, p # high inclusion
