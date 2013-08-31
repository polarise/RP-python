#!/home/paulk/software/bin/python
from __future__ import division
import sys,time,os

def get_flag(flag):
	"""
	convert decimal to binary string of the binary representation
	"""
	bin_final = "00000000"
	bin = ""
	while flag > 0:
		if flag % 2 == 0:
			bin = "0" + bin
			flag /= 2
		else:
			bin = "1" + bin
			flag //= 2
	l = len(bin)
	return bin_final[:8-l] + bin

try:
	dec = sys.argv[1]
except IndexError:
	print "Simple script to convert decimal to binary"
	print "Usage: ./conv2bin.py <dec>"
	print """Example:
$./conv2bin.py 99
Dec: 99
Bin: 01100011
-| Mate #1| Other aligned to (-)| (+)| -| -| One of aligned pair| One of pair"""
	sys.exit(1)

# i am quite annoyed at this flag thing; it conveys no real information!
if __name__ == '__main__':
	val = get_flag(int(dec))
	print 'Dec: %s' % dec
	print 'Bin: %s' % val
	if val[0] == '1': print 'Mate #2|',
	else: print '-|',
	if val[1] == '1': print 'Mate #1|',
	else: print '-|',
	if val[2] == '1': print 'Other aligned to (-)|',	# meaningless
	else: print '-|',
	if val[3] == '1': print '(-)|',
	else: print '(+)|',
	if val[4] == '1': print 'One of pair without alignment(s)|',	# meaningless
	else: print '-|',
	if val[5] == '1': print 'No alignment(s)|',	# meaningless - doesn't turn up on Tophat SAM output but turns up in Bowtie SAM output
	else: print '-|',	
	if val[6] == '1': print 'One of aligned pair|',		# meaningless
	else: print '-|',
	if val[7] == '1': print 'One of pair'	 # uninformative - you should already know this a priori
	else: print '-'

