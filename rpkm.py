#!/home/paulk/software/bin/python
from __future__ import division
import pysam
from sys import exit,argv,stderr

no_reads = {3:27765315,4:29049542,5:34720217,6:33450737,7:31397618,8:7970677,9:27649575,10:30556757}
root = "/data2/paulk/RP/"

try:
	sample = int(argv[1])
except IndexError:
	print >> stderr,"Usage: ./rpkm.py <sample>"
	print >> stderr,"Example: ./rpkm.py 3"
	exit(1)

genes = dict()
f = open(root+"nonov_genes.hg18.gene",'r')
for line in f:
	id,name,chrom,st,sp,sd = line.strip().split('\t')
	genes[int(id[4:])] = [chrom,int(st),int(sp),sd]
f.close()


bf = "output4/%sC/accepted_hits.bam"
bamfile = pysam.Samfile(root+bf%sample,'rb')
for g in genes:
	gene = genes[g]
	glength = gene[2]-gene[1]+1
	total_reads = no_reads[sample]
	try:
		count = bamfile.count(gene[0],gene[1],gene[2])
	except ValueError:
		count = 0
	gene += [count/(glength*10**-3)/(total_reads*10**-6)]
bamfile.close()

base = "ENSG00000000000"
len_base = len(base)
print "gene_id\tchr\tstart\tend\tstrand\tRPKM"
for g in genes:
	g_len = len(str(g))
	G = genes[g]
	print "%s\t%s\t%s\t%s\t%s\t%s" % (base[:len_base-g_len]+str(g),G[0],G[1],G[2],G[3],G[4])
