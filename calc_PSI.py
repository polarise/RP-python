#!/home/paulk/software/bin/python
from __future__ import division
import sys
import scipy

def psi(left,right,over):
	return .5*(left+right)/(over + 0.5*(left+right))
	
def se(p,n):
	return scipy.sqrt(p*(1-p)/n)

try:
  counts_fn = sys.argv[1]
  tover = int(sys.argv[2])
  tleft = int(sys.argv[3])
  tright = int(sys.argv[4])
except IndexError:
  print >> sys.stderr,"Usage:./script.py <counts_fn> <over> <left> <right>"
  sys.exit(0)

f = open(counts_fn)
for row in f:
	l = row.strip().split('\t')
	left = int(l[1])
	right = int(l[2])
	over = int(l[3])
	if over >= tover or (left >= tleft and right >= tright) or (left >= tleft and right >= tright):
		p = psi(left,right,over)
		n = 0.5*(left+right)+over
		SE =  se(p,n)
		p_low = p - 2*SE
		try:
			assert 0 <= p_low
		except:
			p_low = 0	
		p_high = p + 2*SE
		try:
			assert p_high <= 1
		except:
			p_high = 1
		P = [p_low,p,p_high,n*p]
		print l[0]+"\t"+"\t".join(map(str,P))
f.close()
	
