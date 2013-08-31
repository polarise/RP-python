#!/home/paulk/software/bin/python
import sys
import random

try:
	fn = sys.argv[1]
	col = int(sys.argv[2])
	no = int(sys.argv[3])
except IndexError:
	print >> sys.stderr,"Script to print a random number of items from a column."
	print >> sys.stderr,"Usage: %s <file> <column> <number>" % sys.argv[0]
	sys.exit(0)

f = open(fn)
data = [row.strip().split('\t')[col-1] for row in f]
f.close()

chosen = [random.choice(data) for i in xrange(no)]

for c in chosen:
	print c	
