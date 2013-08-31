#!/usr/bin/env python
from __future__ import division
import sys

"""
Given n tab-delimitted files having the first column as a unique ID
returns the intersection of IDs in all files
"""
no_files = len( sys.argv )

try:
	assert no_files > 1
except:
	raise IOError( "Missing files! Exciting..." )
	sys.exit( 1 )

my_files = [ open( f ) for f in sys.argv[1:no_files] ]
ID_lists = [ [ row.strip().split( '\t' )[0] for row in f ] for f in my_files ]

minimal_ID_list = set( ID_lists[0] )
for i in xrange( 1, no_files - 1 ):
	minimal_ID_list = minimal_ID_list.intersection( set( ID_lists[i] ) )

minimal_ID_list = list( minimal_ID_list )
minimal_ID_list.sort()
for m in minimal_ID_list:
	print m
