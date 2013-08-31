#!/home/paulk/software/bin/python
import sys
from key_functions import *

try:
	gtf_file = sys.argv[1]
	filt = sys.argv[2]
except IndexError:
	print >> sys.stderr,"Usage: %s <gtf_file> <filter>" % sys.argv[0]
	sys.exit(0)

f = open(filt)
canonical_txs = {row.strip():0 for row in f}
f.close()

f = open(gtf_file)
tx2line = dict()
for row in f:
	if process_feature(row.strip())['transcript_id'] in canonical_txs: print row.strip()
f.close()


