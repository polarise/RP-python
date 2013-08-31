#!/home/paulk/software/bin/python
import sys
import argparse
import subprocess
import cPickle
from key_functions import *
import pysam
import tempfile

try:
#	gtf_file = sys.argv[1]
	exons_file = sys.argv[1]
except IndexError:
	print >> sys.stderr,"Usage: %s <gtf_file|exons_file>" % sys.argv[0]
	sys.exit(0)

# datasets to use
# exon lengths
f = open("/data2/paulk/RP/resources/exon_lengths.pic")
cel = cPickle.load(f)
f.close()

# exons
f = open("/data2/paulk/RP/resources/exons.hg19.Ens66.0-based.pic")
exons = load(f)
f.close()

# intron lengths
f = open("/data2/paulk/RP/resources/intron_lengths.pic")
cil = cPickle.load(f)
f.close()

# fasta
#fastafile = pysam.Fastafile("/data2/paulk/RP/resources/refs/hg19/Homo_sapiens.GRCh37.66.dna.chr.fa")
fastafile = pysam.Fastafile("/data2/paulk/RP/resources/refs/hg19/Homo_sapiens.GRCh37.66.dna.fa")

fo1 = open("%s_intron_length" % exons_file,'w')
fo2 = open("%s_fiveSS" % exons_file,'w')
fo3 = open("%s_threeSS" % exons_file,'w')

#f = open(gtf_file)
f = open(exons_file)
for row in f:
#	if row.strip().split('\t')[2] in ['start_codon','stop_codon','CDS']: continue
	# make sure the exon is a terminal ones
	l = row.strip().split('\t')
#	strand = row.strip().split('\t')[6]
#	feature,blank = parse_lines([row.strip()],strand,True)
#	exon = list(feature)[0]
	exon = l[1]
#	is_terminal_feature,up_exon,down_exon = terminal_exon(exon,cel)
	is_terminal_feature,up_exon,down_exon = terminal_exon(exon,exons)
	if is_terminal_feature:	# if this is terminal ignore it
		continue
	tx,exno = exon.split(':')
	upstream_intron = tx+':'+str(int(exno)-1)
	
	# get the exon lengths
	try:
		exon_length = cel[exon]
	except KeyError:
		continue
	
	# get the upstream intron lengths
	upstream_intron_length = cil[upstream_intron]
	
	# get the downstream intron length
	try:
		downstream_intron_length = cil[exon]
	except KeyError:
		downstream_intron_length = "NA"
	
	# create GTF-like rows
	exon_region = exons[exon]
	gtf_row = region_to_GTF(exon,exon_region,True)
	
	# get the data for the 5SS score
	
	five,three = GTFrow_to_5p3pcoords(gtf_row,[3,6,20,3],False)
	
	A = fastafile.fetch(region=five)
	if five[-1] == '-':
		A = complementDNA(A[::-1])	# reverse the string
	print >> fo2,">",exon
	print >> fo2,A

	# get the data for the 3SS score
	B = fastafile.fetch(region=three)
	if three[-1] == '-':
		B = complementDNA(B[::-1])
	print >> fo3,">",exon
	print >> fo3,B
	
	# spew everything outfile
	print >> fo1,"\t".join(map(str,[exon,exon_length,upstream_intron_length,downstream_intron_length]))
#	print >> fo1,"\t".join(map(str,[exon,upstream_intron_length,downstream_intron_length]))
f.close()
