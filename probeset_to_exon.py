#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from cPickle import load
import pysam
import argparse
from key_functions import parse_lines
import random

parser = argparse.ArgumentParser(description="Script to replace a single column of probeset values with the respective gene-exon number.")
parser.add_argument('infile',help="input file to be processed")
parser.add_argument('-i','--index',type=int,default=0,help="index of column to be substituted [default: 0 (the first column)]")
parser.add_argument('-d','--detail-pic',help="the PIC file containing the coordinates of the index column")
parser.add_argument('-t','--tabix-file',help="an indexed tabix file that contains the features with which to carry out the substitution")
#parser.add_argument('-s','--skip',type=int,default=0,help="number of lines to skip from the top of the file [default: 0 (start from the immediate top)]")
parser.add_argument('-c','--chrom-names',action='store_false',default=True,help="determines whether chromosome names should begin with 'chr' when being passed to the search object [default: true]")
parser.add_argument('-x','--transcripts',default=False,action='store_true',help="determines whether to get transcripts instead of genes by default [default: false]")
parser.add_argument('-o','--outfile',help="file to write the output")
parser.add_argument('-r','--report',default=False,action="store_true",help="build a .report file") # a report file is a compilation of probeset to exon mappings to be used by 'remove_duplicate_probesets.py' to create 'up_sanitised' and friends

args = parser.parse_args()

infile = args.infile
#print >> stderr, infile
colno = args.index
ps_detail_file = args.detail_pic
tabix_file = args.tabix_file
chrom_names = args.chrom_names
get_transcripts = args.transcripts
report = args.report

# obtain the ps details
f = open(ps_detail_file)
ps_detail = load(f)
f.close()

# open the tabix file using pysam
tabix_file_ptr = pysam.Tabixfile(tabix_file)

# exon lengths
f = open("/data2/paulk/RP/resources/exon_lengths.pic")
exon_lengths = load(f)
f.close()

f = open(infile)
if args.outfile: g = open(args.outfile,'w')
else: g = stderr
if report: h = open(infile+".report",'w')
ps_missing = list()
for row in f:
	if row[0] in ['p','I']: continue
	l = row.strip().split('\t')
	try:
		chrom,st_sp,sd = ps_detail[int(l[colno])].split(':')
	except KeyError:	# funny enough there are some probesets that are missing!!! e.g. 2593464 and 2381177
		continue
#	print chrom,st_sp,sd
	if chrom == '---': continue
	st,sp = st_sp.split('-')
	if not chrom_names:	# if tabix needs 'chr' removed
		chrom = chrom[3:]
	else:	# if tabix can work with 'chr'
		pass
	if chrom == "chrM": chrom = "chrMT"
	if chrom == "M": chrom = "MT"
	try:
		lines = tabix_file_ptr.fetch(region="%s:%s-%s" % (chrom,st,sp))
	except ValueError:
		ps_missing.append((int(l[0]),ps_detail[int(l[colno])]))
#		print l[0]
		continue
	
	gene_exons,no_lines = parse_lines(lines,sd,get_transcripts)
	if gene_exons == []:
		ps_missing.append((int(l[0]),ps_detail[int(l[colno])]))
		#print l[0]
		continue
		
	if report:
		print >> h,l[colno]+"\t"+",".join(gene_exons)
#		for ge in gene_exons:
#			print >> h,l[colno]+"\t"+ge
#	"""
#	"""

	#if len(gene_exons) > 0: print >> g,"\t".join([",".join(gene_exons)]+l[colno+1:])
	if len(gene_exons) > 0:
		ge = random.choice(list(gene_exons))
		el = str(exon_lengths[ge])
		print >> g,l[colno]+"\t"+ge+"\t"+el
		#print >> g,l[colno]+"\t"+random.choice(list(gene_exons))+"\t"+str(exon_lengths[random.choice(list(gene_exons))])
	
	#print >> h,l[colno]+"\t"+",".join(gene_exons)+"\t"+l[colno]

f.close()
if args.outfile: g.close()
if report: h.close()

#print >> stderr,ps_missing
#print >> stderr,len(ps_missing)
