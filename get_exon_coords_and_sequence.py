#!/home/paulk/software/bin/python
import sys
import pysam
from key_functions import complementDNA

try:
	exon_fn = sys.argv[1]
	gene_fn = sys.argv[2]
	fasta_fn = sys.argv[3]
except IndexError:
	print >> sys.stderr,"Usage: script.py <exon_fn> <gene_fn> <tabix_fn>"
	sys.exit(0)

fastafile = pysam.Fastafile(fasta_fn)

keys = dict()
f = open(exon_fn)
for row in f:
	keys[tuple(row.strip().split(':'))] = []
f.close()

f = open(gene_fn)
c = 0
for row in f:
	if c > 5: break
	l = row.strip().split('\t')
	sd = l[5]
	if (l[0],l[1]) in keys:
		coord =  l[2]+":"+l[3]+"-"+l[4]
		results = fastafile.fetch(region=coord)
		print ">%s" % coord+":"+sd
		if sd == '+':
			print results
		elif sd == '-':
			print complementDNA(results)[::-1]
		c += 0
f.close()

fastafile.close()
