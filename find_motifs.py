#!/home/paulk/software/bin/python
from __future__ import division
import sys
import rpy2.robjects as R

binom_test = R.r['binom.test']

try:
	fn = sys.argv[1]
	motif_length = int(sys.argv[2])
except IndexError:
	print >> sys.stderr,"Usage: script.py <fasta_file> <motif_length>"
	sys.exit(1)

null_motifs = {'N':0}
null_motif_length = 1
null_total_motifs = 0
null_seq = ''
motifs = dict()
f = open(fn)
c = 0
seq = ''
for row in f:
	if c > 100: break
	if row[0] == '>':
		if seq != '':
			for i in xrange(len(seq)-motif_length+1):
				motif = seq[i:i+motif_length]
				if motif not in motifs:
					motifs[motif] = 1
				else:
					motifs[motif] += 1
			for i in xrange(len(seq)-null_motif_length+1):
				null_motif = seq[i:i+null_motif_length]
				if null_motif not in null_motifs:
					null_motifs[null_motif] = 1
				else:
					null_motifs[null_motif] += 1
				null_total_motifs += 1
		seq = ''
		continue
	else:
		seq += row.strip()
	c += 0
f.close()

import cPickle
f = open("/data2/paulk/RP/motifs/core_exons.%s.motifs" % motif_length)
#f = open("/data2/paulk/RP/motifs/core_exons.%s.motifs" % motif_length,'w')
core_motifs = cPickle.load(f)
#cPickle.dump(motifs,f,cPickle.HIGHEST_PROTOCOL)
f.close()
#sys.exit(0)

total_motifs = sum(motifs.values())
core_total_motifs = sum(core_motifs.values())

#print "%s-mer\tobs.\tE[x]\tobs.(core)\tp" % motif_length
for m in motifs:
	no_motifs = motifs[m]
	ratio = no_motifs/total_motifs
	core_ratio = core_motifs[m]/core_total_motifs
	p = binom_test(no_motifs,total_motifs,core_ratio)[2][0]
	print "%s\t%.5f\t%.5f\t%.5f\t%.5f\t%.5e" % (m,ratio,reduce(lambda x,y:x*y,[null_motifs[l]/null_total_motifs for l in m]),core_ratio,ratio-core_ratio,p)
	
#print motifs[m],total_motifs,core_motifs[m]/core_total_motifs
#result = binom_test(motifs[m],total_motifs,core_motifs[m]/core_total_motifs)[2][0]
#print result[0][0],result[2][0]
print motifs
