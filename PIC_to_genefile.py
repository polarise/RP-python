#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import load

try:
	picfn = argv[1]
	genefile = argv[2]
except IndexError:
	print >> stderr,"""\
Script to convert a PIC file to a gene file."""
