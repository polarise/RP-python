#!/home/paulk/software/bin/python
import sys
import random
import cPickle

try:
	rfn = sys.argv[1]
	pic = sys.argv[2]
except IndexError:
	print >> sys.stderr,"Usage: %s <rfn> <pic>\n<rfn> - report file\n<pic> - pickle of exon lengths" % sys.argv[0]
	sys.exit(0)

f = open(rfn)
ps2exons = dict()
for row in f:
	ps,exon = row.strip().split('\t')
	if ps not in ps2exons:
		ps2exons[ps] = [exon]
	else:
		ps2exons[ps] += [exon]
f.close()

f = open(pic)
exon_lengths = cPickle.load(f)
f.close()

for ps in ps2exons:
	random_exon = random.choice(ps2exons[ps])	# pick an exon at random
	length = exon_lengths[random_exon]
	print "\t".join([ps,random_exon,str(length)])
