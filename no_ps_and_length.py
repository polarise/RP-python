#!/home/paulk/software/bin/python
from cPickle import load
from sys import argv

f = open(argv[1])
data = dict()
for row in f:
	l = row.strip().split('\t')
	if l[0] not in data:
		data[l[0]] = [l[1]]
	else:
		data[l[0]] += [l[1]]
f.close()

gene_lengths = load(open("resources/gene_lengths.hg19.pic"))

for d in data:
	print d,len(data[d]),gene_lengths[d]
