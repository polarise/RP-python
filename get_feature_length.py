#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from subprocess import Popen,PIPE
from multiprocessing import Process,Queue
from key_functions import process_feature
from scipy import mean,array

def average_length(lines,sd):
	lengths = map(int,[process_feature(line)['transcript_id'] for line in lines.split('\n') if line.split('\t')[6] == sd])
	return mean(array(lengths))

def get_length(row,feature,q):
	ps,coords = row.strip().split('\t')
	sd = coords[-1]
	cmd = "tabix resources/Homo_sapiens.GRCh37.66.%ss.gtf.gz %s" % (feature,coords[:-2])
	p = Popen(cmd,stdout=PIPE,shell=True)
	result = p.communicate()[0].strip()
	if result != '': q.put(row.strip()+"\t"+str(round(average_length(result,sd),2)))
	return

def printer(q):
	while not q.empty():
		print q.get()
	return

if __name__ == '__main__':
	f = open("%s_ps_coords.txt" % argv[1])
	q = Queue()
	pro_list = list()
	c = 0
	for row in f:
		if c > 100: break
		while len(pro_list) > 20:
			for p in pro_list:
				if not p.is_alive(): pro_list.remove(p)
		pro = Process(target=get_length,args=(row,argv[1],q,))
		pro_list.append(pro)
		pro.start()
		while not q.empty(): print q.get()
		c += 0
	f.close()
