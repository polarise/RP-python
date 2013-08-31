#!/usr/bin/env python
from __future__ import division
import sys
import os.path
import cPickle
import scipy
import random

try:
	sanitised_fn = sys.argv[1]
	ps2mps_fn = sys.argv[2]
	mps_expr_fn = sys.argv[3]
	data_fn = sys.argv[4]
except IndexError:
	print >> sys.stderr, "Usage: %s <sanitised_fn> <ps2mps_fn> <mps_expr_fn> <data_fn>" % os.path.basename( sys.argv[0] )
	print >> sys.stderr, """\
<sanitised_fn> - e.g. ~/RP/eBayesVII/up_exons.sanitised
<ps2mps_fn>    - e.g. ~/RP/resources/probesets_grouped.pic
<mps_expr_fn>  - e.g. ~/RP/rma_proper/1C_results_due_to_filtering/rma.filtered.txt.core.mps
<data_fn>      - e.g. ~/RP/eBayesVII/up_exons.sanitised.data"""
	sys.exit( 1 )

"""
NOTES:
- Objective: to augment the 'data' file with information on gene expression and the ID of the gene
- It is better to use mps IDs for the gene because it is the direct repre. of the expression; using Ens IDs
admits noise because the map from ps to exons requires ps to multiple txs to one exon and moving backwards
does not guarantee the right ps
"""

# exons to probesets
f = open( sanitised_fn )
exon2ps = dict()
for row in f:
	L = row.strip().split( '\t' )
	if L[1] not in exon2ps:
		exon2ps[L[1]] = [int( L[0] )]
	else:
		exon2ps[L[1]] += [int( L[0] )]
f.close()

# ps to mps
f = open( ps2mps_fn )
ps2mps = cPickle.load( f )
f.close

# mps expr
mps_expr = dict()
f = open( mps_expr_fn )
idx = [1, 4, 5, 8]
for row in f:
	if row[0] == 'S': continue
	L = row.strip().split( '\t' )
	mps_expr[int( L[0] )] = scipy.mean( map( float, [L[i] for i in idx] ))
f.close()

# include analysis of nucleotide content

# process each row in data file
f = open( data_fn )
c = 0
for row in f:
	if c > 5: break
	L = row.strip().split( '\t' )
	
	# get the ps
	ps = random.choice( exon2ps[ L[0] ] )
	
	# get the mps
	mps = ps2mps[ps]
	
	# get the mps_expr
	expr = mps_expr[mps]
	
	# new print
	print "\t".join( [L[0], str( mps ), str( expr )] + L[1:] )
	
	c += 0

