#!/usr/bin/env python
from __future__ import division
import sys

# All based on Ens v.66

# ps to gene
f = open( "/data2/paulk/MARS/9B_custom_mps/gene_to_exonic_probesets.core.unique.txt" )
ps2gene = dict()
for row in f:
  ps, gene = row.strip().split( '\t' )
  if ps not in ps2gene:
    ps2gene[ps] = [gene]
  else:
    ps2gene[ps] += [gene]
f.close()

# mps to ps
f = open( "/home/paulk/RP/resources/HuEx-1_0-st-v2.2/HuEx-1_0-st-v2.r2.dt1.hg18.core.mps" )
m2p = dict()
for row in f:
  if row[0] == 'p' or row[0] == '#': continue
  L = row.strip().split( '\t' )
  mps = L[0]
  ps = L[2]
  if ps == '': continue
  pss = ps.split( ' ' )
  if mps not in m2p:
    m2p[mps] = pss
  else:
    m2p[mps] += pss
f.close()

f = open( sys.argv[1] ) # file with a list of metaprobesets
mpss = [ row.strip() for row in f ]
f.close()

for mps in mpss:
  # get  a ps
  ps = m2p[mps]
    
  # get the gene
  gotten = False
  i = 0
  for i in xrange( len( ps )):
    try:
      gene = ps2gene[ps[i]]
      break
    except KeyError:
      i += 1  
  
  print gene[0]

#print m2p
