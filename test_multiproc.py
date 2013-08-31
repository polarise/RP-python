#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
from multiprocessing import Process,active_children,Queue
from time import sleep

def func(q):
	i = q.get()
	print >> stderr,i
	return
	
f = open("test.out")
q = Queue()
for r in f:
	q.put(r.strip())
f.close()

no_p = 0
while not q.empty():
	if no_p < 10:
		p = Process(target=func,args=(q,))
		p.start()
		p.join()
		no_p += 1
	
	
