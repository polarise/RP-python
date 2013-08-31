#!/home/paulk/software/bin/python
import sys
import cPickle
import scipy

root = "/data2/paulk/RP/"

f = open(root + "resources/exon_lengths.pic")
exon_lengths = cPickle.load(f)
f.close()

f = open(root + "eBayesVII/exons_FC")
for row in f:
	l = row.strip().split('\t')
	if len(l) != 2:
		print >> sys.stderr,row.strip()
		continue
	else:
		exons = l[0]
		logFC = l[1]
	print "%.2f\t%s" % (scipy.mean([int(exon_lengths[exon]) for exon in exons.split(',')]),logFC)
f.close()
