#!/usr/bin/python
from __future__ import division
import sys
try:
	dec = int(sys.argv[1])
	if dec < -1 or dec > 255: raise IndexError()
except IndexError, ValueError:
	print "Convert decimal to binary to a maximum of 255."
	print "Usage: ./dec2bin.py <dec>"
	sys.exit(1)

pwr = 8
bits = ''
while pwr > -1:
	bits += str(dec // 2**pwr)
	dec  %= 2**pwr
	pwr -= 1
print bits
