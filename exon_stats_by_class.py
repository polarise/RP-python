#!/home/paulk/software/bin/python
from __future__ import division
import sys
import cPickle

try:
	tx2gene_fn = sys.argv[1]
	gl_fn = sys.argv[2]
	g_coords_fn = sys.argv[3]
	ps_coords_fn = sys.argv[4]
	exon_fn = sys.argv[5]
except IndexError:
	print >> sys.stderr,"Usage: script.py <tx2gene_fn> <g1_fn> <g_coords_fn> <ps_coords_fn> <exon_fn>"
	sys.exit(0)

# i need a map of transcripts to genes
tx2gene = dict()
f = open(tx2gene_fn)
for row in f:
	g,t = row.strip().split('\t')
	tx2gene[t] = g
f.close()
	
# i need a map of gene lengths
f = open(gl_fn)
gene_lengths = cPickle.load(f)
f.close()

# gene coordinates
f = open(g_coords_fn)
g_coords = cPickle.load(f)
f.close()

# probeset coordinates
f = open(ps_coords_fn)
ps_coords = cPickle.load(f)
f.close()

print "probeset_id\texon\texon_len\tgene\tgene_length\tdistfrom3p"
f = open(exon_fn)
c = 0
for row in f:
	if c > 5: break
	l = row.strip().split('\t')
	ps = int(l[0])
	ps_coord = ps_coords[ps]
	ps_st = int(ps_coord.split(':')[1].split('-')[0])
	t = l[1].split(':')[0]
	g = tx2gene[t]
	g_len = gene_lengths[g]
	g_coord = g_coords[g]
	gs_sp = int(g_coord.split(':')[1].split('-')[1])
	dist_from_3_prime = gs_sp - ps_st + 1
	print "\t".join(map(str,l+[g,g_len,dist_from_3_prime]))
	c += 0
f.close()
	
	
