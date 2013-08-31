#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from re import search
from cPickle import load

types = ['up','down','bottom','core','all']
dinucls = [r"GT-AG",r"GC-AG",r"AT-AC",r"AT-A.*"]

totals = ["Totals"]
Results = dict()
for a in types:
	for b in ['5','3']:
		D = dict() # the dictionary of the dinucls in this category
		try:
#			f = open("%s%s.dinucl.pseudo"%(a,b))
			f = open("%s%s.dinucl"%(a,b))
		except IOError:
#			f = open("%s.dinucl.pseudo"%a)
			f = open("%s.dinucl"%a)
		for row in f:
			if row[0] == 'x': totals.append(row.strip().split('\t')[1]); continue
			l = row.strip().split('\t')
			if len(l) != 4: continue
#			D["%s-%s" % (l[0],l[1])] = round(float(l[3]),4)
			D["%s-%s" % (l[0],l[1])] = float(l[3])
		f.close()
		
		results = dict()
		for d in D: # for each dinucl category...
			for k in dinucls: # for each of the dinucls of interest...
				if search(k,d): # examine for a match
					if k not in results:
						results[k] = D[d]
					else:
						results[k] += D[d]

		for k in dinucls:
			try:
				N = results[k]
			except KeyError:
				N = 0
#			print k+"\t%s"%N
			if k not in Results:
				Results[k] = [N]
			else:
				Results[k] += [N]

for R in Results:
	print "\t".join([R]+map(str,Results[R]))
print "\t".join(totals)
