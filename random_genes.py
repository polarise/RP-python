#!/home/paulk/software/bin/python
from random import choice
from sys import argv,stderr,exit

try:
	fn = argv[1]
	no = int(argv[2])
except IndexError:
	print >> stderr,"Script to get <no> random IDs from a <list_file>. Results printed to <stdout>."
	print >> stderr,"Usage: ./%s <list_file> <no>" % argv[0]
	exit(1)

assert 0 < no < 10000

f = open(fn)
genes = list()
for row in f:
	genes.append(row.strip())
f.close()

random_genes = [choice(genes) for i in xrange(no)]

for r in random_genes:
	print r
