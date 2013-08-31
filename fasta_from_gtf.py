#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr,stdout
import pysam
import argparse
from cPickle import load
from key_functions import GTFrow_to_5p3pcoords,complementDNA,parse_lines,terminal_exon,region_to_GTF

parser = argparse.ArgumentParser(description="Script to get unique splice site region sequences given a GTF file. Note: 5' and 3' are relative to the splice junction.")
parser.add_argument('gtffile',help="GTF of input features about whose exon boundary sequences are required")
parser.add_argument('-f','--fasta-file',default="/data2/paulk/RP/resources/refs/hg19/hg19.fa",help="path to the FASTA file containing the genome [default: /data2/paulk/RP/resources/refs/hg19/hg19.fa]")
parser.add_argument('-n','--offset',default=[3,6,20,3],nargs=4,type=int,help="integer of number of bases of either side of the splice junction starting with the 5'SS then 3'SS (default: 3 6 20 3 meaning 3 exonic and 6 intronic at the 5'SS and 20 intronic and 3 exonic at the 3'SS)")
parser.add_argument('-F','--feature-coords',help="usually a PIC file with feature (gene-exons,transcript-exon) coordinates to enable identification whether this is a terminal feature")
parser.add_argument('-x','--transcripts',default=False,action='store_true',help="use transcript identifiers [default: false]")
parser.add_argument('-c','--chrom-names',default=True,action='store_false',help="determines whether chromosome names should begin with 'chr' when being passed to the search object [default: true]")
parser.add_argument('-i','--introns',default=False,action='store_true',help="instead of concentrating on the bounding splice sites get the flanking splices sites; this returns the upstream 5'SS and 3'SS as well as the down stream ones [default: false]")

args = parser.parse_args()

gtffn = args.gtffile
offset = args.offset
fastafn = args.fasta_file
feature_coords_fn = args.feature_coords
get_transcripts = args.transcripts
use_chromnames = args.chrom_names
get_introns = args.introns

if feature_coords_fn:
	feature_coords = load(open(feature_coords_fn))

print >> stderr,"Note: using FASTA file at %s" % fastafn

f = open(gtffn)
junctions = set()
for row in f: # for each row in the input GTF
	# we need to get rid of first and last exons
	if row.strip().split('\t')[2] in ['start_codon','stop_codon','CDS']: continue
	if feature_coords_fn: # if we have the resource to check whether this is a terminal exon or not
#		print >> stderr,row.strip()
		strand = row.strip().split('\t')[6]
		feature,blank = parse_lines([row.strip()],strand,get_transcripts)
#		print >> stderr,feature
		is_terminal_feature,up_exon,down_exon = terminal_exon(list(feature)[0],feature_coords)
		if is_terminal_feature:	# if this is terminal ignore it
			continue
		# now we know that this is not a terminal exon so there must be neighbouring exons
		up_exon_gtf = region_to_GTF(up_exon,feature_coords[up_exon],get_transcripts)
		down_exon_gtf = region_to_GTF(down_exon,feature_coords[down_exon],get_transcripts)

 		if get_introns:
 			up_exon_five,up_exon_three = GTFrow_to_5p3pcoords(up_exon_gtf,offset,use_chromnames)
 			five,three = GTFrow_to_5p3pcoords(row,offset,use_chromnames)
 			down_exon_five,down_exon_three = GTFrow_to_5p3pcoords(down_exon_gtf,offset,use_chromnames)
 			junctions.add((up_exon_five,three,five,down_exon_three))
 		else:
			five,three = GTFrow_to_5p3pcoords(row,offset,use_chromnames)
			junctions.add((five,three))
f.close()

fastafile = pysam.Fastafile(fastafn)

# arrange to receive data
if get_introns:
	tog1 = open(gtffn+".upstream_introns",'w')
	tog2 = open(gtffn+".downstream_introns",'w')
else:
	fivesfn = gtffn+".fives.%s_%s.fasta"%(offset[0],offset[1])
	threesfn = gtffn+".threes.%s_%s.fasta"%(offset[2],offset[3])
	f5 = open(fivesfn,'w')
	f3 = open(threesfn,'w')

for pieces in junctions:
	if get_introns:
		seqs = list()
		for p in pieces:
			if p[:3] == "chr": q = p[3:-2]
			else: q = p[:-2]
			seq = fastafile.fetch(region=q)
			if p[-1] == '-':
				seq = complementDNA(seq[::-1])
			seqs += [seq]
	else:
		five,three = pieces
		A = fastafile.fetch(region=five)
		B = fastafile.fetch(region=three)
		if five[-1] == '-':
			A = complementDNA(A[::-1])	# reverse the string
		if three[-1] == '-':
			B = complementDNA(B[::-1])
	
	if get_introns:
		u5,u3,d5,d3 = pieces
		print >> tog1,"\t".join([u5,u3]+[seqs[0][:offset[0]]+seqs[0][offset[0]:].lower()]+[seqs[1][:offset[2]].lower()+seqs[1][offset[2]:]])
		print >> tog2,"\t".join([d5,d3]+[seqs[2][:offset[0]]+seqs[2][offset[0]:].lower()]+[seqs[3][:offset[2]].lower()+seqs[3][offset[2]:]])
	else:
		print >> f5,"> %s"%five
		print >> f5,A[:offset[0]]+A[offset[0]:].lower()
		print >> f3,"> %s"%three
		print >> f3,B[:offset[2]].lower()+B[offset[2]:]

fastafile.close()
if get_introns:
	tog1.close()
	tog2.close()
else:
	f5.close()
	f3.close()

print >> stderr,"Found %s unique features."%len(junctions)
print >> stderr,"Path to indexed FASTA file: %s"%fastafn
print >> stderr,"Offsets: 5'-> (%s,%s); 3'-> (%s,%s))"%tuple(offset)
if not get_introns:
	print >> stderr,"5' results written to %s."%fivesfn
	print >> stderr,"3' results written to %s."%threesfn
