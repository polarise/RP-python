#!/home/paulk/software/bin/python
from __future__ import division
import sys,os,time
from re import search

"""
'tx_class' values for Exon or CDS
IG_C_gene
IG_C_pseudogene
IG_D_gene
IG_J_gene
IG_J_pseudogene
IG_V_gene
IG_V_pseudogene
lincRNA
miRNA
miRNA_pseudogene
misc_RNA
misc_RNA_pseudogene
Mt_rRNA
Mt_tRNA
Mt_tRNA_pseudogene
polymorphic_pseudogene
processed_transcript
protein_coding
pseudogene
rRNA
rRNA_pseudogene
scRNA_pseudogene
snoRNA
snoRNA_pseudogene
snRNA
snRNA_pseudogene
TR_C_gene
TR_J_gene
tRNA_pseudogene
TR_V_gene
TR_V_pseudogene
"""

class Exon:
	def __init__(self,chrom,start,end,strand,exon_no,element_type):
		self.chrom = chrom
		self.start = int(start)
		self.end = int(end)
		self.strand = strand
		self.exon_no = int(exon_no)
		self.element_type = element_type
		self.length = self.end - self.start + 1

class Transcript:
	def __init__(self,name,strand,hgnc_name=None):
		self.name = name
		self.strand = strand
		self.hgnc_name = hgnc_name
		self.exons = dict()			# a dictionary of lists (each of at least length one)
		self.cdss = dict()			# a dictionary of lists (each of at least length one)
		self.introns = dict()		# a dictionary of exon objects
		
	def addExon(self,exon_obj):
		"""
		add an exon to a transcript
		"""
		exon_no = exon_obj.exon_no
		if exon_obj.element_type == "exon":
			if exon_no not in self.exons:
				self.exons[exon_no] = [exon_obj]
			else:
				self.exons[exon_no].append(exon_obj)
		elif exon_obj.element_type == "CDS":
			if exon_no not in self.cdss:
				self.cdss[exon_no] = [exon_obj]
			else:
				self.cdss[exon_no].append(exon_obj)
		return
	
	def addIntron(self,intron_obj):
		"""
		add (by inference) an intron to a transcript
		"""
		intron_no = intron_obj.exon_no
		if intron_no not in self.introns:
			self.introns[intron_no] = intron_obj
		return	
	
	def firstExon(self):
		"""
		get the exon_no for the first exon of this transcript
		"""
		exon_nos = self.exons.keys()
		exon_nos.sort()
		self.first = exon_nos[0]
		return self.first	
	
	def lastExon(self):
		"""
		get the exon_no for the last exon of this transcript
		"""
		exon_nos = self.exons.keys()
		exon_nos.sort()
		self.last = exon_nos[-1]
		return self.last
	
	def defStart(self):
		"""
		infer the start from the exons/cdss
		"""
		last_exon = self.lastExon()
		first_exon = self.firstExon()
		if self.strand == '-':	# reverse strand
			self.start = self.exons[last_exon][0].start
		else:					# forward strand and other cases
			self.start = self.exons[first_exon][0].start
		return self.start
		
	def defEnd(self):
		"""
		infer the end from the exons/cdss
		"""
		last_exon = self.lastExon()
		first_exon = self.firstExon()
		if self.strand == '-':	# reverse strand
			self.end = self.exons[first_exon][0].end
		else:
			self.end = self.exons[last_exon][0].end
		return self.end
	
	def defChrom(self):
		"""
		infer chrom from exons/cds
		"""
		first_exon = self.firstExon()
		self.chrom = self.exons[first_exon][0].chrom
		return self.chrom
	
	def exonCount(self):
		return len(self.exons.keys())
		
	def cdsCount(self):
		return len(self.cdss.keys())
		
	def defIntrons(self,of="exons"):
		"""
		introns are constructed using the same class as exons
		by default computes introns for exons
		of = "exon" | "cds"
		"""
		if of == "exon":
			exon_keys = self.exons.keys()
			exon_keys.sort()
			last_exon = exon_keys[-1]
			first_exon = exon_keys[0]
			strand = self.exons[first_exon][0].strand
			chrom = self.exons[first_exon][0].chrom
			for e in xrange(len(exon_keys)-1):
				k = exon_keys[e]
				k_n = exon_keys[e + 1]
				if strand == '-':
					end = self.exons[k][0].start - 1
					start = self.exons[k_n][0].end + 1
				else:
					start = self.exons[k][0].end + 1
					end = self.exons[k_n][0].start - 1
				intron = Exon(chrom,start,end,strand,exon_keys[e],"intron")	# an intron is of the same class as an exon
				self.addIntron(intron)
		elif of == "cds":
			cds_keys = self.cdss.keys()
			cds_keys.sort()
			if len(cds_keys) == 0: return
			last_cds = cds_keys[-1]
			first_cds = cds_keys[0]
			strand = self.cdss[first_cds][0].strand
			chrom = self.cdss[first_cds][0].chrom
			for c in xrange(len(cds_keys)-1):
				l = cds_keys[c]
				l_m = cds_keys[c + 1]
				if strand == '-':
					end = self.cdss[l][0].start - 1
					start = self.cdss[l_m][0].end + 1
				else:
					start = self.cdss[l][0].end + 1
					end = self.cdss[l_m][0].start - 1
				intron = Exon(chrom,start,end,strand,cds_keys[c],"intron")
				self.addIntron(intron)
			
		return
	
	def intronCount(self):
		return len(self.introns.keys())
	
	def printTranscript(self,colour=False):
		"""
		print method for transcripts
		"""
		if colour == True:
			COLOUR = "\033[1;33m"
		else:
			COLOUR = ""
		PLAIN = "\033[0;0m"		
		self.start = self.defStart()
		self.end = self.defEnd()
		self.chrom = self.defChrom()
		self.defIntrons()
		#print "%s%s (%s): %s exons, %s introns"%(COLOUR,self.name, self.hgnc_name, self.exonCount(),self.intronCount())
		#print "%s[%s-%s](%s) [%4skb]%s"%(self.chrom,self.start,self.end,self.strand,(self.end - self.start + 1)/1000,PLAIN)
		print "\t".join([self.name,self.hgnc_name,self.chrom,str(self.start),str(self.end),self.strand,str(self.end - self.start + 1)])
		
		return
			
	def printExons(self,colour=False):
		"""
		print method for exons
		"""
		if colour == True:
			COLOUR = "\033[1;32m"
			PLAIN = "\033[0;0m"
		else:
			COLOUR = ""
			PLAIN = ""

		exon_keys = self.exons.keys()
		exon_keys.sort()
		for e in exon_keys:
			exon = txs[t].exons[e][0]	# alias for the first element in the list of exon object instances
			print "%s%s\t%s\t%s\t%s\t%s\t%s\t%s%s"%(COLOUR,self.name,exon.exon_no,exon.chrom,exon.start,exon.end,exon.strand,exon.length,PLAIN)		
		
		return
	
	def printCDSs(self,colour=False):
		"""
		print method for CDS
		"""
		if colour == True:
			COLOUR = "\033[1;31m"
			PLAIN = "\033[0;0m"
		else:
			COLOUR = ""
			PLAIN = ""
		cds_keys = self.cdss.keys()
		cds_keys.sort()
		for c in cds_keys:
			cds = txs[t].cdss[c][0]	# alias for the first element in the list of exon object instances
			print "%s%s\t%s\t%s\t%s\t%s\t%s\t%s%s"%(COLOUR,self.name,cds.exon_no,cds.chrom,cds.start,cds.end,cds.strand,cds.length,PLAIN)		
		
		return		

	def printIntrons(self,colour=False):
		"""
		print method for introns
		"""
		if colour == True:
			COLOUR = "\033[1;31m"
			PLAIN = "\033[0;0m"
		else:
			COLOUR = ""
			PLAIN = ""
		intron_keys = self.introns.keys()
		intron_keys.sort()
		for i in intron_keys:
			intron = txs[t].introns[i]	# alias for the first element in the list of exon object instances
			print "%s%s\t%s\t%s\t%s\t%s\t%s\t%s%s"%(COLOUR,self.name,intron.exon_no,intron.chrom,intron.start,intron.end,intron.strand,intron.length,PLAIN)		
		
		return

import argparse
parser = argparse.ArgumentParser(description="Script to glean specific features from a GTF file.")
parser.add_argument('infile',help="input GTF file")
parser.add_argument('-c','--type',action='store_true',help="use CDS features instead of the default use of exons")
parser.add_argument('-C','--chrom-names',action='store_true',help="make sure the chromosome names begin with 'chr' (not implemented)")
parser.add_argument('-e','--exons',action='store_true',help="exons")
parser.add_argument('-i','--introns',action='store_true',help="introns")
parser.add_argument('-t','--txs',action='store_true',help="transcripts")

args = parser.parse_args()

infile = args.infile

if args.type:
	of_value = "cds"
else:
	sys.stderr.write("Warning: Assuming that you are interested in non-cds introns.\n")
	of_value = "exon"

if search(r".gz$",infile):
	import gzip
	f = gzip.open(infile)
else:
	f = open(infile)
	
txs = dict()
for l in f:
	line = l.strip().split('\t')
	# chrom(0) | tx_class(1) | element_type(2) | start(3) | end(4) | ?(5) | strand(6) | ?(7) | annotation(8)
	"""
	annot = line[8].split(';')
	gene_id = annot[0].rstrip("\"")[10:]	# neat trimming
	tx_id = annot[1].rstrip("\"")[16:]
	exon_no = annot[2].rstrip("\"")[14:]
	gene_name = annot[3].rstrip("\"")[12:]
	try: tx_name = annot[4].rstrip("\"")[18:]
	except IndexError: tx_name = ''
	"""
	Annot = [k.strip().strip(';').strip('"') for k in line[8].strip().split(' ')]
	if 'gene_id' in Annot: gene_id = Annot[Annot.index('gene_id')+1]
	if 'transcript_id' in Annot: tx_id = Annot[Annot.index('transcript_id')+1]
	if 'exon_number' in Annot: exon_no = Annot[Annot.index('exon_number')+1]
	if 'gene_name' in Annot: gene_name = Annot[Annot.index('gene_name')+1]
	if 'tx_name' in Annot: tx_name = Annot[Annot.index('tx_name')+1]
	else: tx_name = ''
	
	chrom = line[0]
	tx_class = line[1]
	if tx_class != "protein_coding": pass
	element_type = line[2]
	if element_type != "exon": continue	# this is fine because 'exon' is most general
	start = line[3]
	end = line[4]
	strand = line[6]
	tx = Transcript(tx_id,strand,tx_name)
	if tx_id not in txs:
		txs[tx_id] = tx
	exon = Exon(chrom,start,end,strand,exon_no,element_type)
	txs[tx_id].addExon(exon)

for t in txs:
	if args.introns:
		txs[t].defIntrons(of=of_value)	
		txs[t].printIntrons(colour=False)
	elif args.txs:
		txs[t].printTranscript(colour=False)
	elif args.exons:
		txs[t].printExons(colour=False)
	"""
	intron = ""
	for i in txs[t].introns:
		intron = "%s\t%s\t%s\t%s\t%s"%(txs[t].introns[i].chrom,txs[t].introns[i].start,txs[t].introns[i].end,txs[t].introns[i].strand,txs[t].introns[i].exon_no)
		print "%s\t%s\t%s"%(txs[t].name,txs[t].hgnc_name,intron)
	#print"""
	
	"""for e in txs[t].exons:	# this line is used to test whether there are multiple exon definitions per exon designation e.g. exon 1 is non-uniquely duplicated (which is not good!)
		if len(txs[t].exons[e]) > 1: print txs[t].exons[e]
		else: pass"""
	
f.close()
