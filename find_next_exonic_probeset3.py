#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE

def process_feature(feature):
        feature_dict = dict()
        line = feature.strip().split('\t')
        Annot = [k.strip().strip(';').strip('"') for k in line[8].strip().split(' ')]
        if 'gene_id' in Annot: feature_dict['gene_id'] = Annot[Annot.index('gene_id')+1]
        if 'transcript_id' in Annot: feature_dict['transcript_id'] = Annot[Annot.index('transcript_id')+1]
        if 'exon_number' in Annot: feature_dict['exon_number'] = Annot[Annot.index('exon_number')+1]
        if 'gene_name' in Annot: feature_dict['gene_name'] = Annot[Annot.index('gene_name')+1]
        if 'tx_name' in Annot: feature_dict['tx_name'] = Annot[Annot.index('tx_name')+1]
        return feature_dict
        
def get_introns(intron_lines,sd):
        introns = set()
        for intron in intron_lines.split('\n'):
                if intron.split('\t')[6] != sd: continue
                Intron = process_feature(intron)
                introns.add((Intron['gene_id'],Intron['exon_number']))
        return introns
        
def get_exons(exon_lines,sd):
        exons = set()
        for exon in exon_lines.split('\n'):
                e = exon.split('\t')
                if e[5] != sd: continue
                exons.add("chr%s:%s-%s" % (e[2],e[3],e[4]))
        return exons
        
def get_probesets(probeset_lines,sd):
        probesets = set()
        for probeset in probeset_lines.split('\n'):
                if probeset.split('\t')[6] != sd: continue
                Probeset = process_feature(probeset)
                probesets.add(Probeset['transcript_id'])
        return probesets

dist = 1000

f = open(argv[1])
for row in f:
	if row[0] == 'i': continue
	l = row.strip().split('\t')
	ps = l[1]
	chrom = l[8]
	st = int(l[11])
	sp = int(l[12])
	sd = l[14]
	if l[14] == '+':
		new_st = sp + 1
		new_sp = sp + 1 + dist
	elif l[14] == '-':
		new_st = st - 1 - dist
		new_sp = st - 1
	cmd = "tabix %s %s:%s-%s" % (argv[2],chrom,new_st,new_sp)
	p = Popen(cmd,stdout=PIPE,shell=True)
	result = p.communicate()[0].strip()
	if result != '':
		print ps+"\t"+",".join(get_probesets(result,sd))
f.close()
