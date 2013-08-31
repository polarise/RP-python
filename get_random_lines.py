#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import random
import argparse
import os

parser = argparse.ArgumentParser(description="Script to randomly sample data from a file.")
parser.add_argument('infile',help="input file")
parser.add_argument('-r','--repeat',default=1,type=int,help="number of lines per unit (default: 1)")
parser.add_argument('-n','--num',default=100,type=int,help="number of lines required (default: 100)")

args = parser.parse_args()
r = args.repeat
n = args.num

if n%r != 0:
	raise ValueError,"-r -n value conflict"

f = open(args.infile,'a+')
the_rows = list()
pick = False
k = 0
total_rows = 0
for row in f:
	if total_rows > n: break
	if random.random() < 0.5 and pick == False:
		pick = True
	if pick == True and k < r:
		the_rows.append(row.strip())
		k += 1
	if pick == True and k >= r:
		pick = False		
		k = 0
	if len(the_rows) == r:
		total_rows += len(the_rows)
		for a_row in the_rows:
			print a_row
		the_rows = list()
f.close()
		



