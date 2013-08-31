#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from multiprocessing import Process,Queue

def extract_ps(lines):
	ps = list()
	for line in lines.split('\n'):
		d = line.strip().split('\t')[8].split(' ')[3].lstrip().rstrip()[1:8]
		ps.append(d)
	return ",".join(ps)

def has_exon(lines):
#	print "Exons?"
	for line in lines.split('\n'):
		l = line.split('\t')
		coord = "%s:%s-%s" % (l[0][3:],l[3],l[4])
		cmd = "tabix resources/Homo_sapiens.GRCh37.66.gtf.gz %s" % coord
		p = Popen(cmd,stdout=PIPE,shell=True)
		result = p.communicate()[0].strip()
		if result != '':
			following_ps = extract_ps(lines)
#			print result
			return True,following_ps
		else:
			return False,None

def find_following_probesets(row):
	out_row = list()
	l = row.strip().split('\t')
	out_row.append(l[0])
	c,st_sp,sd = l[1].split(':')
	st,sp = st_sp.split('-')
	i = 0
	next_exon_found = False
	following_ps = None
	while not next_exon_found and i < 1000:
		if sd == '+':
			new_coord = "%s:%s-%s" % (c,int(sp)+75*i,int(sp)+75*(i+1))
		elif sd == '-':
			new_coord = "%s:%s-%s" % (c,int(st)+75*(i+1),int(st)+75*i)
		cmd = "tabix resources/HuEx-1_0-st-v2.na31.hg19.probeset.gtf.gz %s" % new_coord
		p = Popen(cmd,stdout=PIPE,shell=True)
		result = p.communicate()[0].strip()
		if result != '':
			next_exon_found,following_ps = has_exon(result)
		i += 1
	if i == 200:
		print >> stderr,"Number of iterations exceeded for %s" % l[0]
	out_row.append(following_ps)
	if following_ps != None:
		print "\t".join(out_row)
	return

f = open("u12_introns_coords.txt")
pro_list = list()
for row in f:
	while len(pro_list) > 10:
		for p in pro_list:
			if not p.is_alive(): pro_list.remove(p)
	pro = Process(target=find_following_probesets,args=(row,))
	pro_list.append(pro)
	pro.start()
f.close()




