#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from multiprocessing import Process,Queue

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
	
def find_following_probesets(row,q):
	l = row.strip().split('\t')
	c,st_sp,sd = l[1].split(':')
	st,sp = st_sp.split('-')
	# get the intron
	introns = set()
	cmd = "tabix resources/Homo_sapiens.GRCh37.66.introns.gtf.gz %s:%s-%s" % (c,st,sp) # get the intron according to some gene model
	p = Popen(cmd,stdout=PIPE,shell=True)
	intron_lines = p.communicate()[0].strip()
	if len(intron_lines) == 0: return
	introns = get_introns(intron_lines,sd)
	if len(introns) == 0: return

	# get the exon
	exons = set()
	for g in introns:
		cmd = "grep -P '^%s\t%s\t' resources/Homo_sapiens.GRCh37.66.exons.gene" % (g[0],int(g[1])+1)
		p = Popen(cmd,stdout=PIPE,shell=True)
		exon_lines = p.communicate()[0].strip()
		if len(exon_lines) == 0: continue
		exons = get_exons(exon_lines,sd)
	if len(exons) == 0: return

	# get the probesets
	probesets = set()
	for e in exons:
		cmd = "tabix resources/HuEx-1_0-st-v2.na31.hg19.probeset.gtf.gz %s" % e
		p = Popen(cmd,stdout=PIPE,shell=True)
		probeset_lines = p.communicate()[0].strip()
		if len(probeset_lines) == 0: continue
		probesets = get_probesets(probeset_lines,sd)
	if len(probesets) == 0: return
	q.put("%s\t%s" % (row.strip(),",".join(list(probesets))))
	return
	
f = open("u2_introns_coords.txt")
lines = f.readlines()
q = Queue()
pro_list = list()
c = 0
for row in f:
	if c > 100: break
	while len(pro_list) > 10:
		for p in pro_list:
			if not p.is_alive(): pro_list.remove(p)
	pro = Process(target=find_following_probesets,args=(row,q,))
	pro_list.append(pro)
	pro.start()
	while not q.empty(): print q.get()
	c += 0
f.close()
