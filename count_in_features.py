#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,stderr,exit
from math import log
import pysam
import argparse
from cPickle import load

print >> stderr,"Note: the alignment being used is unique-reads against hg19. Please change it if needed (and change this notice)."

"""
Synopsis
Given a BAM file and a GTF file returns a tab delimitted file of counts to features
"""

def PrintStatic(line):
	stderr.write("\r%s"%line.ljust(50))
	stderr.flush()

parser = argparse.ArgumentParser(description="Script to count reads in features.")
parser.add_argument('bamfile',help="a SAM/BAM file")
#parser.add_argument('type',choices='FM',help="feature or metafeature: 'F' - feature (e.g. exon, probeset); 'M' - metafeature (e.g. gene/tx,metaprobeset)")
parser.add_argument('-g','--gene-file',help="a file formatted as follows: gene_id|exon_no/gene_name|chr|start|stop|strand")
parser.add_argument('-p','--pic-file',help="a PIC file formatted as follows: {key:<chr>:<start>-<stop>:<strand>}")
parser.add_argument('-o','--out-file',help="output file")

parser.add_argument('-u','--unnormalised',choices='gnut',default='n',help=" 'n' = normalise by exonic region length (default); 'u' = do not normalise by feature length; 'g' = normalise by gene-exon region dimensions (special);")

args = parser.parse_args()

bf = args.bamfile
gf = args.gene_file
pf = args.pic_file
of = args.out_file
u = args.unnormalised

# hg19
no_reads = {3:27765315,4:29049542,5:34720217,6:33450737,7:31397618,8:7970677,9:27649575,10:30556757}

# hg18
#no_reads = {3:40728726,4:42406011,5:48229121,6:46376465,7:46053435,8:15437411,9:47822316,10:44246330}
norm = True
by_gene = False
by_tx = False

if u == 'u':
	norm = False
elif u == 'g':
	norm = True
	by_gene = True
	gene_lengths = load(open("/home/paulk/RP/resources/gene_lengths.hg19.pic"))
elif u == 't':
	norm == True
	by_tx = True
	tx_lengths = load(open("/home/paulk/RP/resources/tx_lengths.hg19.pic"))
elif u == 'n':
	norm = True
else:
	print >> stderr,"Warning: normalisation flag not set. Using default: by feature length..."
	norm = True

exon_counts = dict()
for s in xrange(3,11):
	#bamfile = pysam.Samfile("/home/paulk/RP/output_hg18/%sC/accepted_hits.bam"%s,'rb')
#	bamfile = pysam.Samfile("/home/paulk/RP/output2/%sC/accepted_hits.bam"%s,'rb')
	bamfile = pysam.Samfile( bf, 'rb' )
	if gf:
		f = open(gf)	# f is a file object
	elif pf:
		f = load(open(pf))	# f is a dictionary
	odd = 0
	c = 0
	for line in f:	# line can be a line in a file or a dictionary key
		if c > 20: break
		if gf:
			l = line.strip().split('\t')
			gid = l[0]
			exno = l[1]
			if l[2][:3] != "chr": chrom = "chr"+l[2]
			else: chrom = l[2]
			st = int(l[3])-1
			sp = int(l[4])-1
		elif pf:
			chrom,st_sp,sd = f[line].strip().split(':')
			a,b = st_sp.split('-')
			st = int(a)
			sp = int(b)
		length = sp-st+1
		try:
			if norm and not by_gene and not by_tx:
				count = bamfile.count(chrom,st,sp)/length/no_reads[s]*10**9
			elif norm and by_gene:
				count = bamfile.count(chrom,st,sp)/gene_lengths[l[0]]/no_reads[s]*10**9
			elif norm and by_tx:
				count = bamfile.count(chrom,st,sp)/tx_lengths[l[0]]/no_reads[s]*10**9
			else:
				count = bamfile.count(chrom,st,sp)/no_reads[s]*10**6
		except ValueError:
			#odd += 1
			#PrintStatic("Odd chromosome: %s (%s)"%(odd,chrom))
			continue
		if gf:
			if (gid,exno) not in exon_counts:
				exon_counts[(gid,exno)] = ["%.5f"%(count)]
			else:
				exon_counts[(gid,exno)] += ["%.5f"%(count)]
		elif pf:
			if line not in exon_counts:
				exon_counts[line] = ["%.5f"%(count)]
			else:
				exon_counts[line] += ["%.5f"%(count)]
		c += 0
	if gf: f.close()
	bamfile.close()

if of: f = open(of,'w')
else: f = stderr
c = 0
for t in exon_counts:
	if c > 20: break
	if gf: 
		print >> f,"%s\t%s"%(t[0],"\t".join(exon_counts[t]))
#		if t[1] != '' or not t[1].isalnum() or t[1].find('_') < 0: print >> f,"%s:%s\t%s"%(t[0],t[1],"\t".join(exon_counts[t]))
#		else: print >> f,"%s\t%s"%(t[0],"\t".join(exon_counts[t]))
	elif pf: print >> f,"%s\t%s"%(t,"\t".join(exon_counts[t]))
	c += 0
if of: f.close()
