#!/home/paulk/software/bin/python
import sys
import cPickle

try:
  t2g_fn = sys.argv[1]
  rp_fn = sys.argv[2]
except IndexError:
  print >> sys.stderr,"Usage:./script.py <tx_to_gene_fn> <data>"
  sys.exit(0)

f = open(t2g_fn)
tx_to_gene = cPickle.load(f)
f.close()

f =  open(rp_fn)
for row in f:
  l = row.strip().split('\t')
  tx,exon = l[1].split(':')
  print tx_to_gene[tx]
f.close()
