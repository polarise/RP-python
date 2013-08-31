#!/home/paulk/software/bin/python
from sys import argv,stderr
from subprocess import Popen,PIPE

def reduce_genes(exon_list):
	return list(set([exon.split(':')[0] for exon in exon_list.split(',')]))

f = open(argv[1])
for row in f:
	l = row.strip().split('\t')
	gene_list = reduce_genes(l[0])
	for gene in gene_list:
		print "\t".join([gene] + l[1:])
#	cmd = "grep -P '%s' resources/genes.hg19.Ens63.gene" % "|".join(gene_list)
#	p = Popen(cmd,shell=True,stdout=PIPE)
#	print cmd
#	print p.communicate()[0]
#	print
f.close()
	
