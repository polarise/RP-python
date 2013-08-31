#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr,stdout
from cPickle import load
import pysam
import argparse
from key_functions import augment_region,terminal_exon

parser = argparse.ArgumentParser(description="Script to get interesting exonic region sequences.")
parser.add_argument('exonfile',help="a file whose first column is exonic regions e.g. ENSGXXXXXXX:<exno>")
parser.add_argument('-p','--gexons-pic',default="/data2/paulk/RP/resources/gene_exons.hg19.Ens63.pic",help="a PIC with 0-based coordinates of exonic regions (default: resources/gene_exons.hg19.Ens63.pic)")
parser.add_argument('-t','--tabixfile',default="/data2/paulk/RP/resources/hg19.Ens63.plain.gtf.gz",help="the tabix indexed GTF for genomic features (default: resources/hg19.Ens63.plain.gtf.gz)")
parser.add_argument('-o','--outfile',help="output filename (default: stdout)")
parser.add_argument('-e','--extend-by',default=100,type=int,help="extend by this number of bases on either side of the exon boundary (default: 100)")
parser.add_argument('-c','--chrom-names',default=True,action='store_false',help="determines whether chromosome names should begin with 'chr' when being passed to the search object [default: true]")

args = parser.parse_args()

exonfn = args.exonfile
gexons_pic = args.gexons_pic
tabixfn = args.tabixfile
extend = args.extend_by
ofn = args.outfile+".%s"%extend
use_chrom_names = args.chrom_names

o = open(ofn,'w')
o_before = open(ofn+".before",'w')
o_after = open(ofn+".after",'w')

print >> stderr,"Extending exonic regions by %s bases. Specify your own with option '-e' (see help for details)"%extend

exons = list()
for row in open(exonfn):
	h1 = row.strip().split('\t')[1]
	for h in h1.split(','):
		exons.append(h)

gex_coords = load(open(gexons_pic))
tabixfile = pysam.Tabixfile(tabixfn)
for exon in exons:
	is_terminal_exon,prev_exon,next_exon = terminal_exon(exon,gex_coords)
	if is_terminal_exon: continue
	
	# get the coordinates
	coords = augment_region(gex_coords[exon],extend)
	coords_before = augment_region(gex_coords[prev_exon],extend)
	coords_after = augment_region(gex_coords[next_exon],extend)
	
	# whether to use 'chr' or not
	if not use_chrom_names:
		coords = coords[3:]
		coords_before = coords_before[3:]
		coords_after = coords_after[3:]
	
	# get the GTF rows that satisfy this
	rows = [row for row in tabixfile.fetch(region=coords) if row.strip().split('\t')[2] == "exon"]
	rows_before = [row for row in tabixfile.fetch(region=coords_before) if row.strip().split('\t')[2] == "exon"]
	rows_after = [row for row in tabixfile.fetch(region=coords_after) if row.strip().split('\t')[2] == "exon"]
	
	# print to the files :: separate exons before and after
	for row in rows:
		print >> o,row
		
	for row_b in rows_before:
		print >> o_before,row_b
		
	for row_a in rows_after:
		print >> o_after,row_a

o.close()
o_before.close()
o_after.close()
